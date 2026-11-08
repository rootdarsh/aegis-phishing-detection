# 🛡️ AEGIS: Adaptive Evaluation & Guarded Intelligence System
### A Multi-Layer Machine Learning Framework for Cross-Platform Phishing Detection and Explainable Threat Assessment

![Project Status](https://img.shields.io/badge/Status-Prototype%20Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![Chrome Extension](https://img.shields.io/badge/Chrome%20Extension-Manifest%20V3-yellow.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)

---

## 📌 Overview
**AEGIS** is a real-time, explainable cybersecurity tool designed to protect users against malicious URLs and phishing threats directly within the browser. 

Traditional solutions either scan emails post-delivery, act as proprietary black boxes, or require technical expertise. AEGIS solves this by combining **Layer 1 URL Heuristic Analysis (20+ features)** with a **Random Forest Machine Learning Ensemble** to evaluate links on web search engines in real time, injecting color-coded threat badges (🟢 Safe, 🟡 Suspicious, 🔴 Dangerous) alongside plain-English risk explanations.

---

## 🏗️ Architecture

```
[ Google Search / Web Page ]
             │
             ▼
   [ Chrome Extension (Manifest V3) ]
             │ (Async Batch POST /scan-batch)
             ▼
      [ FastAPI Backend ]
       ├── Feature Extraction (20+ Lexical & Structural Metrics)
       ├── Layer 2 Whitelist & Authority Verification
       ├── Random Forest ML Inference (aegis_model.pkl)
       └── SQLite Telemetry Logger (aegis.db)
             │
             ├────────────────────────────────┐
             ▼                                ▼
   [ DOM Injected Badges ]        [ Streamlit Web Dashboard ]
   • 🟢 SAFE                      • Live Scan Telemetry
   • 🟡 CAUTION                   • Real-Time Threat Distribution
   • 🔴 DANGER (Click Intercept)  • Interactive Single-URL Inspector
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Google Chrome Browser

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/rootdarsh/aegis-phishing-detection.git
cd aegis-phishing-detection
pip install -r requirements.txt
```

### 3. Launch Backend & Dashboard
On Windows, simply double click:
```cmd
start_aegis.bat
```
Or start them individually:
```bash
# Terminal 1: FastAPI Backend
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Streamlit Dashboard
cd dashboard
python -m streamlit run app.py
```
- **Backend API Docs:** `http://127.0.0.1:8000/docs`
- **Telemetry Dashboard:** `http://localhost:8501`

### 4. Load Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top-right corner).
3. Click **"Load unpacked"** and select the `extension/` folder from this repository.
4. Perform any Google Search: search results will now be analyzed and tagged in real-time!

---

## 🔬 Model Performance & Feature Engineering

The current model is a **Random Forest Ensemble (100 estimators)** trained on a benchmark dataset of 2,400 samples modeling Alexa Top 1M legitimate URLs vs. PhishTank/OpenPhish attack vectors.

- **Test Accuracy:** > 95%
- **F1-Score:** > 95%
- **Key Features Extracted:**
  - `has_ip`: Detection of raw numerical host addresses
  - `suspicious_word_count`: High-entropy credential keywords (`login`, `verify`, `bank`, `account`)
  - `is_shortened`: Obfuscation via URL redirection services
  - `count_subdomains`: Deep subdomain nesting for brand spoofing
  - `has_https`: Transport layer security validation

---

## 👥 Project Team (Group No. 6 — DESH, VIT Pune)

| Student Name | PRN / GR No. | Designated Role |
|:---|:---:|:---|
| **Dandnaik Shreyash Somnath** | 12612242 | QA, Empirical Testing & Compliance Lead |
| **Dange Sharwal Shailesh** | 12610050 | Backend Engineer (FastAPI Microservice & SQLite) |
| **Darsh Hemantkumar Raut** | 12611013 | ML & Feature Engineer (Model Pipeline & Architecture) |
| **Darade Rohan Rajendra** | 12611258 | Research & Threat Intelligence (Literature & Evasion Study) |
| **Darsh Jain** | 12611575 | Frontend Engineer (Chrome Extension & DOM Injection) |

**Project Guide:** Prof. Vidya Dhanve  
**Course:** Engineering Design & Innovation Project 1 (EDI 1) — Nov 2026
