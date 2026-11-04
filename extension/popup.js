const API_BASE = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", async () => {
  const statusEl = document.getElementById("backend-status");
  const urlEl = document.getElementById("active-url");
  const scanBtn = document.getElementById("btn-scan");
  const resultBox = document.getElementById("result-box");
  const verdictEl = document.getElementById("result-verdict");
  const scoreEl = document.getElementById("result-score");
  const reasonsEl = document.getElementById("result-reasons");

  // Check backend health
  try {
    const res = await fetch(`${API_BASE}/`);
    if (res.ok) {
      statusEl.textContent = "🟢 Online (Port 8000)";
      statusEl.style.color = "#16a34a";
    } else {
      statusEl.textContent = "🔴 Server Error";
      statusEl.style.color = "#dc2626";
    }
  } catch (e) {
    statusEl.textContent = "🔴 Offline";
    statusEl.style.color = "#dc2626";
  }

  // Get active tab URL
  let currentTabUrl = "";
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url) {
      currentTabUrl = tab.url;
      urlEl.textContent = currentTabUrl;
    } else {
      urlEl.textContent = "Unable to read active tab URL";
    }
  } catch (err) {
    urlEl.textContent = "Permission error reading URL";
  }

  // Scan current tab on click
  scanBtn.addEventListener("click", async () => {
    if (!currentTabUrl || !currentTabUrl.startsWith("http")) {
      alert("Cannot scan local or internal browser pages.");
      return;
    }

    scanBtn.textContent = "Analyzing...";
    scanBtn.disabled = true;

    try {
      const resp = await fetch(`${API_BASE}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: currentTabUrl, source: "chrome_extension_popup" })
      });

      if (resp.ok) {
        const data = await resp.json();
        resultBox.style.display = "block";
        resultBox.className = `result-card result-${data.verdict.toLowerCase()}`;
        verdictEl.textContent = `Verdict: ${data.verdict.toUpperCase()}`;
        scoreEl.textContent = `Threat Risk Score: ${data.risk_score} / 100`;

        const reasonsHtml = (data.reasons || [])
          .map(r => `• ${r}`)
          .join("<br>");
        reasonsEl.innerHTML = `<strong>Factors:</strong><br>${reasonsHtml}`;
      } else {
        alert("Failed to analyze URL.");
      }
    } catch (e) {
      alert("Could not connect to AEGIS API at 127.0.0.1:8000");
    } finally {
      scanBtn.textContent = "🔍 Scan Page Security";
      scanBtn.disabled = false;
    }
  });
});
