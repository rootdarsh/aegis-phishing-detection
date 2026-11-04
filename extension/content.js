// AEGIS Content Script - Surgical Precision Link & Media Highlighter
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
      // 1. Regular Google Search Results (ONLY the main <h3> heading links)
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

      // 2. Video & Image Carousel Thumbnails ONLY (Shorts, YouTube videos, Image grid)
      // Must contain a real visual thumbnail (width >= 80px), NOT a tiny 16px favicon!
      const allAnchors = document.querySelectorAll(
        "div[data-snc] a, g-inner-card a, div.isv-r a, div.x9P4oc a, div[jsname] a"
      );
      for (const a of allAnchors) {
        if (a.dataset.aegisProcessed) continue;
        // Never tag if it's already an <h3> result
        if (a.querySelector("h3") || a.closest("h3")) continue;

        const href = a.href;
        if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
        if (href.includes("google.com/search") || href.includes("localhost")) continue;

        const img = a.querySelector("img, video");
        if (!img) continue;

        const rect = img.getBoundingClientRect();
        // Ignore favicons and tiny site logos (which are 16x16 or 24x24)
        if (rect.width < 75 || rect.height < 60) continue;

        a.dataset.aegisProcessed = "true";
        targets.push({
          type: "thumbnail",
          element: img, // Directly highlight the image thumbnail
          anchor: a,
          url: href
        });
      }
    } else {
      // 3. Regular External Webpages (YouTube, Wikipedia, Blogs)
      // Discrete micro-shield for body text links
      const links = document.querySelectorAll("a[href]");
      let count = 0;

      for (const a of links) {
        if (count >= 50) break;
        if (a.dataset.aegisProcessed) continue;

        const href = a.href;
        if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
        if (href.startsWith("javascript:") || href.startsWith("#")) continue;
        if (href.includes("localhost") || href.includes("127.0.0.1")) continue;
        if (href.includes("#") && href.split("#")[0] === window.location.href.split("#")[0]) continue;

        const text = a.textContent.trim();
        if (!text || text.length < 2) continue;
        if (a.offsetWidth === 0 && a.offsetHeight === 0) continue;
        if (a.closest("nav, header, footer, [role='navigation']")) continue;

        a.dataset.aegisProcessed = "true";
        targets.push({
          type: "inline_link",
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
        console.debug("[AEGIS Shield] Backend offline:", err.message);
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

    // 1. VIDEO & IMAGE THUMBNAILS: Clean Lining directly on the image
    if (item.type === "thumbnail") {
      item.element.classList.add("aegis-thumb-lining", `aegis-thumb-${verdictClass}`);
      attachTooltipEvents(item.element, result);
      return;
    }

    // 2. GOOGLE SEARCH RESULT HEADING: Clean Pill Badge next to title text
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

    // 3. INLINE LINKS ON GENERAL WEBSITES (e.g. YouTube): Discreet 13px Shield Icon
    if (item.type === "inline_link") {
      if (item.element.nextElementSibling?.classList?.contains("aegis-inline-shield")) return;

      const shield = document.createElement("span");
      shield.className = `aegis-inline-shield aegis-shield-${verdictClass}`;
      shield.innerHTML = result.verdict === "Safe" ? "🛡️" : (result.verdict === "Suspicious" ? "⚠️" : "🚨");

      attachTooltipEvents(shield, result);
      item.element.insertAdjacentElement("afterend", shield);
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
