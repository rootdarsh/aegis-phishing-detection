// AEGIS Content Script - Cross-Platform Precision Link Highlighter
(function () {
  // 1. Never scan or inject badges into your own local development dashboard (localhost / 127.0.0.1)
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
          element: h3,
          anchor: anchor,
          url: href
        });
      }
    } else {
      const links = document.querySelectorAll("a[href]");
      let count = 0;

      for (const a of links) {
        if (count >= 60) break;
        if (a.dataset.aegisProcessed) continue;

        const href = a.href;
        if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
        if (href.startsWith("javascript:") || href.startsWith("#")) continue;
        if (href.includes("localhost") || href.includes("127.0.0.1")) continue;

        const text = a.textContent.trim();
        if (!text || text.length < 2) continue;
        if (a.offsetWidth === 0 && a.offsetHeight === 0) continue;
        if (a.closest("nav, header, footer, [role='navigation']")) continue;

        a.dataset.aegisProcessed = "true";
        targets.push({
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
        renderBadge(item.element, item.anchor, scanCache.get(item.url));
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
              renderBadge(item.element, item.anchor, res);
            }
          }
        }
      } catch (err) {
        console.debug("[AEGIS Shield] Backend API unavailable:", err.message);
      }
    }
  }

  function renderBadge(mountElement, anchorElement, result) {
    if (mountElement.querySelector(".aegis-badge") || 
       (mountElement.nextElementSibling && mountElement.nextElementSibling.classList?.contains("aegis-badge"))) {
      return;
    }

    const badge = document.createElement("span");
    badge.className = `aegis-badge aegis-${result.verdict.toLowerCase()}`;
    
    let icon = "🟢";
    if (result.verdict === "Dangerous") icon = "🔴";
    else if (result.verdict === "Suspicious") icon = "🟡";

    const pill = document.createElement("span");
    pill.className = "aegis-pill";
    pill.innerHTML = `${icon} ${result.verdict.toUpperCase()} (${result.risk_score})`;
    badge.appendChild(pill);

    pill.addEventListener("mouseenter", () => {
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

      const rect = pill.getBoundingClientRect();
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

    pill.addEventListener("mouseleave", () => {
      const tooltip = document.getElementById("aegis-global-tooltip");
      if (tooltip) {
        tooltip.style.opacity = "0";
        tooltip.style.display = "none";
        tooltip.style.visibility = "hidden";
      }
    });

    if (result.verdict === "Dangerous" && anchorElement) {
      anchorElement.addEventListener("click", function (e) {
        const proceed = window.confirm(
          `🚨 AEGIS SECURITY ALERT!\n\nThis link was flagged as HIGH-RISK PHISHING (Risk Score: ${result.risk_score}/100).\n\nDestination: ${result.url}\n\nDo you still wish to proceed?`
        );
        if (!proceed) {
          e.preventDefault();
          e.stopPropagation();
        }
      });
    }

    if (mountElement.tagName === "H3") {
      mountElement.appendChild(badge);
    } else {
      mountElement.insertAdjacentElement("afterend", badge);
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
