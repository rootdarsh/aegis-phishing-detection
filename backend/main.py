import os
import sys
import json
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from feature_extractor import (
    extract_features_from_url, 
    get_heuristic_reasons, 
    is_trusted_authority, 
    detect_brand_impersonation,
    FEATURE_NAMES
)
from database import init_db, log_scan, get_recent_scans, get_stats

app = FastAPI(
    title="AEGIS Phishing Detection API",
    description="Multi-Layer Machine Learning Framework for Real-time Phishing Detection",
    version="1.0.0"
)

# Enable CORS for Chrome Extension and Streamlit Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model loader
MODEL_PATH = os.path.join(CURRENT_DIR, "model", "aegis_model.pkl")
clf_model = None

@app.on_event("startup")
def startup_event():
    init_db()
    load_model()

def load_model():
    global clf_model
    if os.path.exists(MODEL_PATH):
        try:
            clf_model = joblib.load(MODEL_PATH)
            print("[AEGIS API] Successfully loaded ML model.")
        except Exception as e:
            print(f"[AEGIS API] Failed to load model: {e}")
    else:
        print("[AEGIS API] Model artifact not found. Will use heuristic scoring fallback.")

class ScanRequest(BaseModel):
    url: str
    source: str = "chrome_extension"

class BatchScanRequest(BaseModel):
    urls: list[str]
    source: str = "chrome_extension"

def analyze_url(url: str) -> dict:
    global clf_model
    if clf_model is None:
        load_model()

    features = extract_features_from_url(url)
    reasons = get_heuristic_reasons(features, url)

    # Layer 2 Check: Trusted Authority
    import urllib.parse
    parsed = urllib.parse.urlparse(url if "://" in url else "http://" + url)
    domain = parsed.netloc.split(":")[0]

    if is_trusted_authority(domain):
        risk_score = 8
        verdict = "Safe"
        color = "#38a169"
        badge_text = "SAFE"
        return {
            "url": url,
            "risk_score": risk_score,
            "verdict": verdict,
            "badge_text": badge_text,
            "color": color,
            "impersonation": {"is_impersonation": False},
            "reasons": reasons,
            "features": features
        }

    # If ML model is loaded, compute probability
    if clf_model is not None:
        feature_vector = np.array([[features[name] for name in FEATURE_NAMES]])
        phish_prob = float(clf_model.predict_proba(feature_vector)[0][1])
        risk_score = int(round(phish_prob * 100))
    else:
        heuristic_score = (
            features.get("has_ip", 0) * 45 +
            features.get("is_shortened", 0) * 35 +
            features.get("count_at", 0) * 30 +
            min(features.get("suspicious_word_count", 0) * 20, 40) +
            (15 if not features.get("has_https") else 0)
        )
        risk_score = min(max(heuristic_score, 5), 98)

    # Active Brand Impersonation Hunter
    impersonation = detect_brand_impersonation(domain, url)
    if impersonation.get("is_impersonation"):
        risk_score = max(risk_score, 88)
        reasons.insert(
            0, 
            f"🚨 BRAND IMPERSONATION: Visual spoofing targeting '{impersonation['spoofed_brand']}' ({impersonation['technique']}; genuine: {impersonation['official_domain']})."
        )

    # Risk classification thresholds
    if risk_score >= 65:
        verdict = "Dangerous"
        color = "#e53e3e"  # Red
        badge_text = "DANGER"
    elif risk_score >= 35:
        verdict = "Suspicious"
        color = "#dd6b20"  # Orange/Yellow
        badge_text = "CAUTION"
    else:
        verdict = "Safe"
        color = "#38a169"  # Green
        badge_text = "SAFE"

    return {
        "url": url,
        "risk_score": risk_score,
        "verdict": verdict,
        "badge_text": badge_text,
        "color": color,
        "impersonation": impersonation,
        "reasons": reasons,
        "features": features
    }

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AEGIS Phishing Detection API",
        "model_loaded": clf_model is not None,
        "endpoints": ["/scan", "/scan-batch", "/history", "/stats"]
    }

@app.post("/scan")
def scan_single(req: ScanRequest):
    if not req.url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
    
    result = analyze_url(req.url)
    
    # Log to SQLite
    try:
        log_scan(
            url=result["url"],
            risk_score=result["risk_score"],
            verdict=result["verdict"],
            reasons=result["reasons"],
            features=result["features"],
            source=req.source
        )
    except Exception as e:
        print(f"[AEGIS DB Error] {e}")

    return result

@app.post("/scan-batch")
def scan_batch(req: BatchScanRequest):
    results = []
    # Cap batch at 40 URLs per call for performance
    target_urls = req.urls[:40]
    for url in target_urls:
        if not url or not url.startswith(("http://", "https://")):
            continue
        res = analyze_url(url)
        results.append(res)
        try:
            log_scan(
                url=res["url"],
                risk_score=res["risk_score"],
                verdict=res["verdict"],
                reasons=res["reasons"],
                features=res["features"],
                source=req.source
            )
        except Exception:
            pass

    return {"results": results, "count": len(results)}

@app.get("/history")
def history(limit: int = 50):
    return {"scans": get_recent_scans(limit)}

@app.get("/stats")
def stats():
    return get_stats()
