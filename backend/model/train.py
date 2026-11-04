import os
import sys
import json
import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

# Add backend directory to sys.path so we can import feature_extractor
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(BACKEND_DIR)

from feature_extractor import extract_features_from_url, FEATURE_NAMES

def generate_training_data():
    """
    Constructs a rich representative dataset of legitimate and phishing URLs
    simulating Alexa Top 1M vs PhishTank/OpenPhish attack vectors.
    """
    random.seed(42)
    np.random.seed(42)

    legit_domains = [
        "google.com", "youtube.com", "wikipedia.org", "github.com", "amazon.com",
        "microsoft.com", "apple.com", "linkedin.com", "reddit.com", "twitter.com",
        "vit.edu", "acm.org", "ieee.org", "stackoverflow.com", "medium.com",
        "nytimes.com", "bbc.com", "cnn.com", "netflix.com", "spotify.com",
        "cloudflare.com", "gitlab.com", "dropbox.com", "adobe.com", "quora.com",
        "coursera.org", "mit.edu", "stanford.edu", "kaggle.com", "python.org"
    ]

    legit_paths = [
        "", "/", "/about", "/contact-us", "/products", "/services", "/search?q=machine+learning",
        "/docs/guide/v2", "/article/2026/cybersecurity-overview", "/blog/post/how-to-code",
        "/watch?v=dQw4w9WgXcQ", "/wiki/Computer_science", "/repos/open-source/project",
        "/browse/category/electronics", "/dashboard/overview", "/explore?tab=popular"
    ]

    phish_targets = ["paypal", "chase", "wellsfargo", "netflix", "apple-id", "microsoft", "google-account", "facebook", "binance", "metamask", "steam"]
    phish_subdomains = ["secure-login", "account-verification", "update-billing", "auth-portal", "helpdesk-security", "verify-id", "wallet-recovery"]
    phish_tlds = [".xyz", ".top", ".tk", ".ml", ".cf", ".club", ".info", ".site", ".online", ".work"]
    shorteners = ["bit.ly", "tinyurl.com", "is.gd", "t.co", "cutt.ly"]

    urls = []
    labels = []  # 0 = Safe, 1 = Phishing

    # Generate 1,200 legitimate URLs
    for _ in range(1200):
        domain = random.choice(legit_domains)
        path = random.choice(legit_paths)
        scheme = "https://" if random.random() > 0.05 else "http://"
        if random.random() > 0.5:
            param = f"?ref=nav&id={random.randint(100, 99999)}&lang=en"
            urls.append(f"{scheme}{domain}{path}{param}")
        else:
            urls.append(f"{scheme}{domain}{path}")
        labels.append(0)

    # Generate 1,200 Phishing URLs covering 6 distinct evasion archetypes
    for _ in range(1200):
        archetype = random.choice([
            "ip_based", "subdomain_spoof", "typosquatting", "keyword_stuffing", "shortener", "punycode"
        ])

        if archetype == "ip_based":
            # Raw numerical IP with suspicious path
            ip = f"{random.randint(11, 215)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            kw = random.choice(["login", "verify-bank", "account-update", "confirm-identity"])
            urls.append(f"http://{ip}:{random.choice([8080, 80, 3000, 8888])}/{kw}/auth?session={random.randint(10000, 99999)}")

        elif archetype == "subdomain_spoof":
            target = random.choice(phish_targets)
            sub = random.choice(phish_subdomains)
            tld = random.choice(phish_tlds)
            urls.append(f"http://{sub}.{target}-security-check{tld}/signin?redirect=true")

        elif archetype == "typosquatting":
            target = random.choice(["gooogle", "micros0ft", "paypa1", "app1e", "netfl1x", "amaz0n"])
            urls.append(f"http://www.{target}-verify{random.choice(phish_tlds)}/login.php?client_id={random.randint(1000, 9999)}")

        elif archetype == "keyword_stuffing":
            domain = f"{random.choice(phish_targets)}-{random.choice(phish_subdomains)}"
            urls.append(f"http://{domain}.com/portal/login/secure/verify/update-password-confirm")

        elif archetype == "shortener":
            short = random.choice(shorteners)
            slug = f"{random.choice(['win', 'free', 'gift', 'login', 'cash'])}{random.randint(100, 9999)}"
            urls.append(f"http://{short}/{slug}")

        elif archetype == "punycode":
            urls.append(f"http://xn--gogle-{random.randint(10, 99)}a.com/login/auth")

        labels.append(1)

    return urls, labels

def train_and_evaluate():
    print("[1/5] Synthesizing and curating benchmark URL dataset...")
    urls, labels = generate_training_data()

    print(f"[2/5] Extracting 20 features for {len(urls)} URLs...")
    feature_rows = []
    for u in urls:
        f = extract_features_from_url(u)
        feature_rows.append([f[name] for name in FEATURE_NAMES])

    X = np.array(feature_rows)
    y = np.array(labels)

    # Save curated dataset for project documentation
    df = pd.DataFrame(X, columns=FEATURE_NAMES)
    df["url"] = urls
    df["label"] = y
    dataset_path = os.path.join(CURRENT_DIR, "aegis_dataset.csv")
    df.to_csv(dataset_path, index=False)
    print(f"       Saved dataset with {len(df)} samples to {dataset_path}")

    # Stratified split 80% train / 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("[3/5] Training Random Forest Classifier on %d samples..." % len(X_train), flush=True)
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=16,
        min_samples_split=4,
        random_state=42,
        n_jobs=1
    )
    clf.fit(X_train, y_train)

    print("[4/5] Evaluating performance on held-out test set...")
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()

    print(f"\n================ AEGIS MODEL EVALUATION METRICS ================")
    print(f"  * Accuracy  : {acc * 100:.2f}%")
    print(f"  * Precision : {prec * 100:.2f}%")
    print(f"  * Recall    : {rec * 100:.2f}%")
    print(f"  * F1-Score  : {f1 * 100:.2f}%")
    print(f"  * Confusion Matrix: {cm}")
    print(f"===============================================================\n")

    # Feature Importance ranking
    importances = dict(zip(FEATURE_NAMES, [round(float(v), 4) for v in clf.feature_importances_]))
    sorted_features = sorted(importances.items(), key=lambda item: item[1], reverse=True)

    metrics = {
        "model_type": "Random Forest Classifier (Ensemble)",
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "confusion_matrix": cm,
        "feature_importances": dict(sorted_features)
    }

    metrics_path = os.path.join(CURRENT_DIR, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"       Saved metrics to {metrics_path}")

    model_path = os.path.join(CURRENT_DIR, "aegis_model.pkl")
    joblib.dump(clf, model_path)
    print(f"[5/5] Trained model artifact exported to {model_path}")
    print("Training pipeline completed successfully!\n")

if __name__ == "__main__":
    train_and_evaluate()
