// AEGIS Content Script - Cross-Platform Precision Link & Media Highlighter
(function () {
  // Never run on local development dashboard
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    return;
  }

  const API_URL = "http://127.0.0.1:8000/scan-batch";
  const scanCache = new Map();

  function getOrCreateGlobalTooltip() {
    let tooltip = document.getElementById("aegis-global-tooltip");
    if (!tooltip) {
      tooltip = document.createElement("div");
      tooltip.id = "aegis-global-tooltip";
      tooltip.className = "aegis-floating-card";
      document.body.appendChild(tooltip);
    }
    return tooltip;
  }

  function isGoogleSearch() {
    const host = window.location.hostname;
    const path = window.location.pathname;
    return (host.includes("google.") && !host.startsWith("play.") && !host.startsWith("docs.") && !host.startsWith("drive.")) 
           && (path.startsWith("/search") || path === "/");
  }

  function getEligibleTargets() {
    const targets = [];
    
    if (isGoogleSearch()) {
      // 1. Target standard Google Search Result headings
      const headings = document.querySelectorAll("#search h3, #rso h3, div.g h3, div[data-sokoban-container] h3");
      for (const h3 of headings) {
        if (h3.dataset.aegisProcessed) continue;

        const anchor = h3.closest("a");
        if (!anchor || !anchor.href) continue;

        const href = anchor.href;
        if (!href.startsWith("http://") && !href.startsWith("https://")) continue;
        if (href.includes("localhost") || href.includes("127.0.0.1")) continue;

        h3.dataset.aegisProcessed = "true";
        targets.push({
          type: "heading",
          element: h3,
          anchor: anchor,
          url: href
        });
      }

      // 2. Target Google Media / Video / Image Thumbnail Cards
      const mediaCards = document.querySelectorAll(
        "div[data-snc] a, g-inner-card a, div.isv-r a, div.x9P4oc a, a:has(> div > img), a:has(> img)"
      );
      for (const card of mediaCards) {
        if (card.dataset.aegisProcessed) continue;

        const href = card.href;
        if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
        if (href.includes("google.com/search") || href.includes("localhost")) continue;

        // Ensure card has a rendered visual thumbnail
        const img = card.querySelector("img, video, [role='img']");
        if (!img || (card.offsetWidth < 60 && card.offsetHeight < 60)) continue;

        card.dataset.aegisProcessed = "true";
        targets.push({
          type: "media_card",
          element: card,
          anchor: card,
          url: href
        });
      }
    } else {
      // 3. On ANY other website (YouTube, Wikipedia, portals, blogs)
      const links = document.querySelectorAll("a[href]");
      let count = 0;

      for (const a of links) {
        if (count >= 60) break;
        if (a.dataset.aegisProcessed) continue;

        const href = a.href;
        if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
        if (href.startsWith("javascript:") || href.startsWith("#")) continue;
        if (href.includes("localhost") || href.includes("127.0.0.1")) continue;
        if (href.includes("#") && href.split("#")[0] === window.location.href.split("#")[0]) continue;

        const text = a.textContent.trim();
        const hasImg = a.querySelector("img, video");
        if (!text && !hasImg) continue;
        if (a.offsetWidth === 0 && a.offsetHeight === 0) continue;
        if (a.closest("nav, header, footer, [role='navigation']")) continue;

        a.dataset.aegisProcessed = "true";
        targets.push({
          type: hasImg && (a.offsetWidth > 100 || a.offsetHeight > 80) ? "media_card" : "inline_link",
          element: a,
          anchor: a,
          url: href
        });
        count++;
      }
    }

    return targets;
  }

  async function scanPageLinks() {
    const targets = getEligibleTargets();
    if (targets.length === 0) return;

    const urlMap = new Map();
    const urlsToFetch = [];

    for (const item of targets) {
      if (scanCache.has(item.url)) {
        applyHighlight(item, scanCache.get(item.url));
      } else {
        if (!urlMap.has(item.url)) {
          urlMap.set(item.url, []);
          urlsToFetch.push(item.url);
        }
        urlMap.get(item.url).push(item);
      }
    }

    if (urlsToFetch.length === 0) return;

    const chunkSize = 25;
    for (let i = 0; i < urlsToFetch.length; i += chunkSize) {
      const chunk = urlsToFetch.slice(i, i + chunkSize);
      try {
        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ urls: chunk, source: "chrome_extension" })
        });

        if (!response.ok) continue;

        const data = await response.json();
        if (data && data.results) {
          for (const res of data.results) {
            scanCache.set(res.url, res);
            const items = urlMap.get(res.url) || [];
            for (const item of items) {
              applyHighlight(item, res);
            }
          }
        }
      } catch (err) {
        console.debug("[AEGIS Shield] Backend API unavailable:", err.message);
      }
    }
  }

  function attachTooltipEvents(interactiveElement, result) {
    interactiveElement.addEventListener("mouseenter", () => {
      const tooltip = getOrCreateGlobalTooltip();
      tooltip.innerHTML = `
        <div class="aegis-tooltip-title">🛡️ AEGIS Threat Assessment</div>
        <div class="aegis-tooltip-verdict">
          <strong>Verdict:</strong> ${result.verdict} &nbsp;|&nbsp; <strong>Risk:</strong> ${result.risk_score}/100
        </div>
        <div class="aegis-tooltip-reasons">
          <strong>Detected Factors:</strong>
          <ul>
            ${(result.reasons || []).map(r => `<li>${r}</li>`).join("")}
          </ul>
        </div>
      `;

      tooltip.style.display = "block";
      tooltip.style.visibility = "visible";

      const rect = interactiveElement.getBoundingClientRect();
      const tipRect = tooltip.getBoundingClientRect();

      let top = rect.top + window.scrollY - tipRect.height - 10;
      let left = rect.left + window.scrollX + (rect.width / 2) - (tipRect.width / 2);

      if (rect.top - tipRect.height - 15 < 0) {
        top = rect.bottom + window.scrollY + 10;
        tooltip.classList.add("arrow-top");
        tooltip.classList.remove("arrow-bottom");
      } else {
        tooltip.classList.add("arrow-bottom");
        tooltip.classList.remove("arrow-top");
      }

      if (left < 15) left = 15;
      if (left + tipRect.width > window.innerWidth - 15) {
        left = window.innerWidth - tipRect.width - 15;
      }

      tooltip.style.top = `${top}px`;
      tooltip.style.left = `${left}px`;
      tooltip.style.opacity = "1";
    });

    interactiveElement.addEventListener("mouseleave", () => {
      const tooltip = document.getElementById("aegis-global-tooltip");
      if (tooltip) {
        tooltip.style.opacity = "0";
        tooltip.style.display = "none";
        tooltip.style.visibility = "hidden";
      }
    });
  }

  function applyHighlight(item, result) {
    const verdictClass = result.verdict.toLowerCase();

    // 1. MEDIA & VIDEO THUMBNAIL CARDS: Glowing Border Lining + Corner Shield
    if (item.type === "media_card") {
      item.element.classList.add("aegis-media-frame", `aegis-frame-${verdictClass}`);

      // Inject small corner security badge if not already present
      if (!item.element.querySelector(".aegis-corner-chip")) {
        const cornerChip = document.createElement("span");
        cornerChip.className = `aegis-corner-chip aegis-chip-${verdictClass}`;
        let icon = "🛡️";
        if (result.verdict === "Dangerous") icon = "🚨";
        else if (result.verdict === "Suspicious") icon = "⚠️";
        cornerChip.innerHTML = `${icon} ${result.verdict.toUpperCase()}`;
        
        attachTooltipEvents(cornerChip, result);
        item.element.style.position = item.element.style.position || "relative";
        item.element.appendChild(cornerChip);
      }
      return;
    }

    // 2. GOOGLE SEARCH HEADING: Full Badges
    if (item.type === "heading") {
      if (item.element.querySelector(".aegis-badge")) return;

      const badge = document.createElement("span");
      badge.className = `aegis-badge aegis-${verdictClass}`;
      let icon = "🟢";
      if (result.verdict === "Dangerous") icon = "🔴";
      else if (result.verdict === "Suspicious") icon = "🟡";

      const pill = document.createElement("span");
      pill.className = "aegis-pill";
      pill.innerHTML = `${icon} ${result.verdict.toUpperCase()} (${result.risk_score})`;
      badge.appendChild(pill);

      attachTooltipEvents(pill, result);
      item.element.appendChild(badge);
      return;
    }

    // 3. INLINE GENERAL WEBPAGE LINKS (e.g. YouTube "Learn More"): Discrete Micro-Shield
    if (item.type === "inline_link") {
      if (item.element.nextElementSibling?.classList?.contains("aegis-micro-badge")) return;

      item.element.classList.add("aegis-inline-link", `aegis-link-${verdictClass}`);

      const micro = document.createElement("span");
      micro.className = `aegis-micro-badge aegis-micro-${verdictClass}`;
      micro.title = `AEGIS: ${result.verdict} (${result.risk_score}/100)`;
      micro.innerHTML = result.verdict === "Safe" ? "🛡️" : (result.verdict === "Suspicious" ? "⚠️" : "🚨");

      attachTooltipEvents(micro, result);
      item.element.insertAdjacentElement("afterend", micro);
    }
  }

  setTimeout(scanPageLinks, 700);

  let debounceTimer;
  const observer = new MutationObserver(() => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(scanPageLinks, 1200);
  });

  observer.observe(document.body, { childList: true, subtree: true });
})();
