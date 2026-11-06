import re
import urllib.parse

# Core phishing indicators
SUSPICIOUS_KEYWORDS = [
    r"\blogin\b", r"\bverify\b", r"\bupdate\b", r"\bbank\b", 
    r"\baccount\b", r"\bsignin\b", r"\bconfirm\b", r"\bpassword\b", 
    r"\bwallet\b", r"\bfree-bonus\b", r"\bclaim-reward\b", r"\bbilling\b",
    r"\bauthenticate\b"
]

SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", 
    "buff.ly", "adf.ly", "tiny.cc", "lnkd.in", "cutt.ly", "rb.gy"
}

# High-trust authoritative domains (AEGIS Layer 2 Whitelist)
TRUSTED_DOMAINS = {
    "google.com", "google.co.in", "youtube.com", "wikipedia.org", "github.com",
    "microsoft.com", "apple.com", "amazon.com", "amazon.in", "linkedin.com",
    "vit.edu", "stackoverflow.com", "reddit.com", "twitter.com", "x.com",
    "netflix.com", "spotify.com", "medium.com", "cloudflare.com", "python.org",
    "paypal.com", "facebook.com", "instagram.com", "binance.com", "sbi.co.in"
}

# Targeted Brands for Active Impersonation & Typosquatting Hunter
TARGET_BRANDS = {
    "paypal": "paypal.com",
    "google": "google.com",
    "microsoft": "microsoft.com",
    "apple": "apple.com",
    "amazon": "amazon.com",
    "netflix": "netflix.com",
    "instagram": "instagram.com",
    "facebook": "facebook.com",
    "binance": "binance.com",
    "vit": "vit.edu",
    "sbi": "sbi.co.in",
    "hdfc": "hdfcbank.com",
    "github": "github.com"
}

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def normalize_homoglyphs(text: str) -> str:
    """Normalizes visual character substitutions (e.g. paypa1 -> paypal, micros0ft -> microsoft)."""
    substitutions = {
        '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', 
        '8': 'b', '@': 'a', 'vv': 'w', 'rn': 'm', 'cl': 'd'
    }
    t = text.lower()
    for k, v in substitutions.items():
        t = t.replace(k, v)
    return t

def detect_brand_impersonation(domain: str, url: str) -> dict:
    """
    Active Brand Impersonation & Typosquatting Hunter.
    Compares the URL against top targeted global & financial brands.
    """
    domain = domain.lower().split(":")[0]
    
    # Check if domain itself is the genuine official brand host
    for brand, official in TARGET_BRANDS.items():
        if domain == official or domain.endswith("." + official):
            return {"is_impersonation": False}

    # Extract core domain label (strip common TLDs)
    domain_parts = domain.split(".")
    core_label = domain_parts[0] if len(domain_parts) <= 2 else domain_parts[-2]
    normalized_core = normalize_homoglyphs(core_label)
    normalized_full = normalize_homoglyphs(domain)

    for brand, official in TARGET_BRANDS.items():
        # Case A: Visual Typosquatting (Levenshtein distance 1 or 2)
        dist = levenshtein_distance(normalized_core, brand)
        if 1 <= dist <= 2 and len(brand) >= 4:
            return {
                "is_impersonation": True,
                "spoofed_brand": brand.capitalize(),
                "official_domain": official,
                "technique": f"Visual Typosquatting (Distance: {dist})",
                "penalty": 55
            }

        # Case B: Brand Squatting in Hostname (e.g. paypal-security-portal.top or verify-apple.com)
        if brand in normalized_full and not domain.endswith("." + official):
            return {
                "is_impersonation": True,
                "spoofed_brand": brand.capitalize(),
                "official_domain": official,
                "technique": "Unauthorized Brand Squatting in Domain",
                "penalty": 50
            }

    return {"is_impersonation": False}

IP_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)

FEATURE_NAMES = [
    "url_length",
    "domain_length",
    "has_ip",
    "count_dots",
    "count_hyphens",
    "count_at",
    "count_question",
    "count_percent",
    "count_equal",
    "count_slash",
    "count_digits",
    "digit_ratio",
    "has_https",
    "count_subdomains",
    "is_shortened",
    "suspicious_word_count",
    "has_punycode",
    "path_length",
    "query_length",
    "has_double_slash_in_path"
]

def extract_features_from_url(url: str) -> dict:
    url_str = str(url).strip()
    if not url_str.startswith(("http://", "https://")):
        url_with_scheme = "http://" + url_str
    else:
        url_with_scheme = url_str

    try:
        parsed = urllib.parse.urlparse(url_with_scheme)
    except Exception:
        parsed = urllib.parse.urlparse("http://" + url_str)

    domain = parsed.netloc.split(":")[0].lower()
    path = parsed.path
    query = parsed.query

    has_ip = 1 if IP_PATTERN.match(domain) else 0
    count_dots = url_str.count(".")
    count_hyphens = url_str.count("-")
    count_at = url_str.count("@")
    count_question = url_str.count("?")
    count_percent = url_str.count("%")
    count_equal = url_str.count("=")
    count_slash = url_str.count("/")
    digits = sum(c.isdigit() for c in url_str)
    url_len = max(len(url_str), 1)
    digit_ratio = round(digits / url_len, 4)
    has_https = 1 if url_str.lower().startswith("https://") else 0

    subdomains = [s for s in domain.split(".") if s]
    # Deduct 2 for SLD and TLD (e.g. google.com -> 0 subdomains; mail.google.com -> 1 subdomain)
    count_subdomains = max(0, len(subdomains) - 2)

    is_shortened = 1 if domain in SHORTENER_DOMAINS else 0

    lower_url = url_str.lower()
    suspicious_word_count = sum(1 for kw_pattern in SUSPICIOUS_KEYWORDS if re.search(kw_pattern, lower_url))

    has_punycode = 1 if "xn--" in domain else 0
    path_len = len(path)
    query_len = len(query)
    has_double_slash = 1 if "//" in path else 0

    return {
        "url_length": len(url_str),
        "domain_length": len(domain),
        "has_ip": has_ip,
        "count_dots": count_dots,
        "count_hyphens": count_hyphens,
        "count_at": count_at,
        "count_question": count_question,
        "count_percent": count_percent,
        "count_equal": count_equal,
        "count_slash": count_slash,
        "count_digits": digits,
        "digit_ratio": digit_ratio,
        "has_https": has_https,
        "count_subdomains": count_subdomains,
        "is_shortened": is_shortened,
        "suspicious_word_count": suspicious_word_count,
        "has_punycode": has_punycode,
        "path_length": path_len,
        "query_length": query_len,
        "has_double_slash_in_path": has_double_slash
    }

def is_trusted_authority(domain: str) -> bool:
    """Check if domain is an established trusted authority or educational domain."""
    domain = domain.lower().split(":")[0]
    for td in TRUSTED_DOMAINS:
        if domain == td or domain.endswith("." + td):
            return True
    if domain.endswith(".edu") or domain.endswith(".gov") or domain.endswith(".ac.in") or domain.endswith(".edu.in"):
        return True
    return False

def get_heuristic_reasons(features: dict, url: str) -> list[str]:
    reasons = []
    parsed = urllib.parse.urlparse(url if "://" in url else "http://" + url)
    domain = parsed.netloc.split(":")[0]

    if is_trusted_authority(domain):
        reasons.append("Domain is recognized as a verified, high-reputation authoritative host.")
        return reasons

    if features.get("has_ip"):
        reasons.append("URL uses a raw numerical IP address instead of an authenticated domain name.")
    if features.get("is_shortened"):
        reasons.append("URL uses a redirection shortener which hides destination endpoints.")
    if features.get("count_at", 0) > 0:
        reasons.append("Contains '@' symbol frequently abused to mask the true destination host.")
    if features.get("has_punycode"):
        reasons.append("Uses Punycode (xn--) which indicates potential Internationalized Homograph attack.")
    if features.get("count_subdomains", 0) >= 3:
        reasons.append(f"Abnormally high subdomain hierarchy ({features['count_subdomains']} subdomains).")
    if features.get("suspicious_word_count", 0) >= 2:
        reasons.append("High concentration of credential/authentication keywords in URL path.")
    if features.get("has_double_slash_in_path"):
        reasons.append("Double slash '//' detected inside URI path (redirect evasion).")
    if not features.get("has_https"):
        reasons.append("Lacks HTTPS transport layer security (cleartext transmission).")
    if features.get("url_length", 0) > 85:
        reasons.append("Anomalous URL length exceeding 85 characters.")
    
    if not reasons:
        reasons.append("Structural lexical features match normal legitimate browsing patterns.")
    return reasons
