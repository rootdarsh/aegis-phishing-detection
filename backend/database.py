import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "aegis.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            verdict TEXT NOT NULL,
            reasons TEXT,
            features TEXT,
            source TEXT DEFAULT 'chrome_extension',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_scan(url: str, risk_score: int, verdict: str, reasons: list[str], features: dict, source: str = "chrome_extension"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans (url, risk_score, verdict, reasons, features, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        url,
        risk_score,
        verdict,
        json.dumps(reasons),
        json.dumps(features),
        source
    ))
    conn.commit()
    conn.close()

def get_recent_scans(limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, url, risk_score, verdict, reasons, source, created_at
        FROM scans
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    for row in rows:
        if row.get("reasons"):
            try:
                row["reasons"] = json.loads(row["reasons"])
            except Exception:
                pass
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE verdict = 'Safe'")
    safe = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE verdict = 'Suspicious'")
    suspicious = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE verdict = 'Dangerous'")
    dangerous = cursor.fetchone()[0]

    conn.close()
    return {
        "total_scans": total,
        "safe_count": safe,
        "suspicious_count": suspicious,
        "dangerous_count": dangerous
    }

if __name__ == "__main__":
    init_db()
    print("AEGIS database initialized successfully at", DB_PATH)
