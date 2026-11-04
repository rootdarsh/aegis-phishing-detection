// AEGIS Content Script - Precision Link Highlighter & Threat Assessment
const API_URL = "http://127.0.0.1:8000/scan-batch";
const scanCache = new Map();

function isGoogleSearch() {
  return window.location.hostname.includes("google.");
}

function getEligibleTargets() {
  const targets = [];
  
  if (isGoogleSearch()) {
    // Specifically target Google Search Result headings (<h3> inside an <a>)
    // This strictly excludes search boxes, Google profile icons, reviews, and navbar tools
    const headings = document.querySelectorAll("#search h3, #rso h3, div.g h3, div[data-sokoban-container] h3");
    
    for (const h3 of headings) {
      if (h3.dataset.aegisProcessed) continue;

      const anchor = h3.closest("a");
      if (!anchor || !anchor.href) continue;

      const href = anchor.href;
      // Filter out internal Google links
      if (!href.startsWith("http://") && !href.startsWith("https://")) continue;
      if (href.includes("google.com/") || href.includes("google.co.in/")) continue;

      h3.dataset.aegisProcessed = "true";
      targets.push({
        element: h3,
        anchor: anchor,
        url: href
      });
    }
  } else {
    // On general non-Google webpages: target main body links only (exclude navigation bars/headers/footers)
    const links = document.querySelectorAll("main a[href], article a[href], #content a[href], .content a[href], p a[href]");
    for (const a of links) {
      if (a.dataset.aegisProcessed) continue;
      const href = a.href;
      if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
      if (href.startsWith("javascript:") || href.startsWith("#")) continue;

      a.dataset.aegisProcessed = "true";
      targets.push({
        element: a,
        anchor: a,
        url: href
      });
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

  // Batch process in chunks of 25 URLs
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
      console.debug("[AEGIS Shield] Backend offline or busy:", err.message);
    }
  }
}

function renderBadge(mountElement, anchorElement, result) {
  // Avoid duplicate injection
  if (mountElement.querySelector(".aegis-badge") || 
     (mountElement.nextElementSibling && mountElement.nextElementSibling.classList?.contains("aegis-badge"))) {
    return;
  }

  const badge = document.createElement("span");
  badge.className = `aegis-badge aegis-${result.verdict.toLowerCase()}`;
  
  let icon = "🟢";
  if (result.verdict === "Dangerous") icon = "🔴";
  else if (result.verdict === "Suspicious") icon = "🟡";

  badge.innerHTML = `
    <span class="aegis-pill">
      ${icon} ${result.verdict.toUpperCase()} (${result.risk_score})
    </span>
    <div class="aegis-tooltip">
      <div class="aegis-tooltip-title">🛡️ AEGIS Threat Assessment</div>
      <div class="aegis-tooltip-verdict"><strong>Verdict:</strong> ${result.verdict} | <strong>Risk:</strong> ${result.risk_score}/100</div>
      <div class="aegis-tooltip-reasons">
        <strong>Reasons:</strong>
        <ul>
          ${(result.reasons || []).map(r => `<li>${r}</li>`).join("")}
        </ul>
      </div>
    </div>
  `;

  // Intercept clicks on Dangerous Phishing links
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

  // If mountElement is an H3, append the badge cleanly right after the title text
  if (mountElement.tagName === "H3") {
    mountElement.appendChild(badge);
  } else {
    mountElement.insertAdjacentElement("afterend", badge);
  }
}

// Initial scan
setTimeout(scanPageLinks, 600);

// Observer for dynamically loaded search results (infinite scroll)
let debounceTimer;
const observer = new MutationObserver(() => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(scanPageLinks, 1000);
});

observer.observe(document.body, { childList: true, subtree: true });
