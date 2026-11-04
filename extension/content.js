// AEGIS Content Script - Cross-Platform Precision Link Highlighter
const API_URL = "http://127.0.0.1:8000/scan-batch";
const scanCache = new Map();

function isGoogleSearch() {
  const host = window.location.hostname;
  const path = window.location.pathname;
  // Strictly match Google Web Search (google.com/search), NOT play.google.com, docs.google.com, etc.
  return (host.includes("google.") && !host.startsWith("play.") && !host.startsWith("docs.") && !host.startsWith("drive.")) 
         && (path.startsWith("/search") || path === "/");
}

function getEligibleTargets() {
  const targets = [];
  
  if (isGoogleSearch()) {
    // 1. On Google Web Search: Target the main result headings
    const headings = document.querySelectorAll("#search h3, #rso h3, div.g h3, div[data-sokoban-container] h3");
    for (const h3 of headings) {
      if (h3.dataset.aegisProcessed) continue;

      const anchor = h3.closest("a");
      if (!anchor || !anchor.href) continue;

      const href = anchor.href;
      if (!href.startsWith("http://") && !href.startsWith("https://")) continue;

      h3.dataset.aegisProcessed = "true";
      targets.push({
        element: h3,
        anchor: anchor,
        url: href
      });
    }
  } else {
    // 2. On ANY other website (play.google.com, Wikipedia, blogs, portals, news)
    // Scan real textual links on the page (cap at 60 links per scan to keep it lightning fast)
    const links = document.querySelectorAll("a[href]");
    let count = 0;

    for (const a of links) {
      if (count >= 60) break;
      if (a.dataset.aegisProcessed) continue;

      const href = a.href;
      if (!href || (!href.startsWith("http://") && !href.startsWith("https://"))) continue;
      if (href.startsWith("javascript:") || href.startsWith("#")) continue;

      // Ensure link has visible text and is rendered on the screen
      const text = a.textContent.trim();
      if (!text || text.length < 2) continue;
      if (a.offsetWidth === 0 && a.offsetHeight === 0) continue;

      // Avoid tagging header navigation or search bars if possible
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

  // Process in batches of 25 URLs
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
  // Avoid duplicate tags
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
      <div class="aegis-tooltip-verdict">
        <strong>Verdict:</strong> ${result.verdict} &nbsp;|&nbsp; <strong>Risk:</strong> ${result.risk_score}/100
      </div>
      <div class="aegis-tooltip-reasons">
        <strong>Detected Factors:</strong>
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

  // If inside an H3 on Google, append at the end of the heading text
  if (mountElement.tagName === "H3") {
    mountElement.appendChild(badge);
  } else {
    // On regular websites, insert cleanly right after the link
    mountElement.insertAdjacentElement("afterend", badge);
  }
}

// Initial scan
setTimeout(scanPageLinks, 700);

// Observer for infinite scrolling and dynamically loaded content
let debounceTimer;
const observer = new MutationObserver(() => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(scanPageLinks, 1200);
});

observer.observe(document.body, { childList: true, subtree: true });
