// AEGIS Content Script - Real-Time Search & Webpage Link Scanner
const API_URL = "http://127.0.0.1:8000/scan-batch";

// Cache analyzed URLs to prevent redundant network requests
const scanCache = new Map();

function getEligibleLinks() {
  const links = document.querySelectorAll("a[href]");
  const eligible = [];
  
  for (const a of links) {
    // Avoid double tagging
    if (a.dataset.aegisScanned) continue;
    
    const href = a.href;
    if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
    
    // Skip internal navigation / google search auxiliary links
    if (href.includes("google.com/search") || href.includes("google.com/url?")) continue;
    if (href.startsWith("javascript:") || href.startsWith("#")) continue;

    eligible.push({ element: a, url: href });
    a.dataset.aegisScanned = "true";
  }
  return eligible;
}

async function scanPageLinks() {
  const eligible = getEligibleLinks();
  if (eligible.length === 0) return;

  const urlMap = new Map();
  const urlsToFetch = [];

  for (const item of eligible) {
    if (scanCache.has(item.url)) {
      renderBadge(item.element, scanCache.get(item.url));
    } else {
      if (!urlMap.has(item.url)) {
        urlMap.set(item.url, []);
        urlsToFetch.push(item.url);
      }
      urlMap.get(item.url).push(item.element);
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
          const elements = urlMap.get(res.url) || [];
          for (const el of elements) {
            renderBadge(el, res);
          }
        }
      }
    } catch (err) {
      // Backend may be offline or starting up; silently log
      console.debug("[AEGIS Shield] Backend API unavailable:", err.message);
    }
  }
}

function renderBadge(element, result) {
  // Check if already tagged
  if (element.nextElementSibling && element.nextElementSibling.classList.contains("aegis-badge")) {
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
      <div class="aegis-tooltip-verdict"><strong>Status:</strong> ${result.verdict} (Risk: ${result.risk_score}/100)</div>
      <div class="aegis-tooltip-reasons">
        <strong>Detected Factors:</strong>
        <ul>
          ${(result.reasons || []).map(r => `<li>${r}</li>`).join("")}
        </ul>
      </div>
    </div>
  `;

  // Attach safe click interception for dangerous phishing links
  if (result.verdict === "Dangerous") {
    element.addEventListener("click", function (e) {
      const confirmNav = window.confirm(
        `🚨 AEGIS SECURITY WARNING!\n\nThis link was flagged as DANGEROUS PHISHING (Risk Score: ${result.risk_score}/100).\n\nDestination: ${result.url}\n\nDo you really want to proceed to this untrusted website?`
      );
      if (!confirmNav) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
  }

  // Insert badge right after link
  element.insertAdjacentElement("afterend", badge);
}

// Initial scan upon page load
setTimeout(scanPageLinks, 1000);

// Observer to handle dynamically loaded search results (infinite scroll / AJAX)
let debounceTimer;
const observer = new MutationObserver(() => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(scanPageLinks, 1500);
});

observer.observe(document.body, { childList: true, subtree: true });
