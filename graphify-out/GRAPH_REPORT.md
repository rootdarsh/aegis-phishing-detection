# Graph Report - aegis  (2026-11-08)

## Corpus Check
- Corpus is ~19,816 words - fits in a single context window. You may not need a graph.

## Summary
- 120 nodes · 182 edges · 8 communities (6 shown, 2 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: 1,250 input · 680 output

## Community Hubs (Navigation)
- FastAPI Backend & Database
- ML Training & Streamlit Dashboard
- Chrome Extension Configuration
- Heuristic & Brand Feature Extraction
- Presentation Deck Generator
- Academic PDF Report Generator
- DOM Injection & Content Script

## God Nodes (most connected - your core abstractions)
1. `analyze_url()` - 8 edges
2. `detect_brand_impersonation()` - 7 edges
3. `extract_features_from_url()` - 7 edges
4. `train_and_evaluate()` - 7 edges
5. `log_scan()` - 6 edges
6. `get_recent_scans()` - 5 edges
7. `levenshtein_distance()` - 5 edges
8. `is_trusted_authority()` - 5 edges
9. `scan_single()` - 5 edges
10. `scan_batch()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Algorithmic Brand Impersonation Hunter` --implements--> `detect_brand_impersonation()`  [EXTRACTED]
  reports/AEGIS_Detailed_Progress_Report.pdf → backend/feature_extractor.py
- `20 Structural Lexical Features Specification` --implements--> `extract_features_from_url()`  [EXTRACTED]
  reports/AEGIS_Detailed_Progress_Report.pdf → backend/feature_extractor.py
- `AEGIS Security Shield Branding Assets` --conceptually_related_to--> `Chrome Extension Popup User Interface`  [INFERRED]
  extension/icons/icon_128.png → extension/popup.html
- `analyze_url()` --calls--> `detect_brand_impersonation()`  [EXTRACTED]
  backend/main.py → backend/feature_extractor.py
- `analyze_url()` --calls--> `extract_features_from_url()`  [EXTRACTED]
  backend/main.py → backend/feature_extractor.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **AEGIS Cross-Platform Multi-Tier Architecture** — backend_main, dashboard_app, backend_feature_extractor [EXTRACTED 0.95]
- **Brand Typosquatting & Impersonation Pipeline** — backend_feature_extractor_levenshtein_distance, backend_feature_extractor_normalize_homoglyphs, backend_feature_extractor_detect_brand_impersonation [EXTRACTED 0.95]

## Communities (8 total, 2 thin omitted)

### Community 0 - "FastAPI Backend & Database"
Cohesion: 0.13
Nodes (17): get_recent_scans(), get_stats(), init_db(), log_scan(), get_heuristic_reasons(), is_trusted_authority(), analyze_url(), BatchScanRequest (+9 more)

### Community 1 - "ML Training & Streamlit Dashboard"
Cohesion: 0.15
Nodes (4): generate_training_data(), train_and_evaluate(), AEGIS Project Overview & Specifications, Adversarial Mutation Playground Engine

### Community 2 - "Chrome Extension Configuration"
Cohesion: 0.11
Nodes (18): action, default_icon, default_popup, default_title, content_scripts, 128, 16, 48 (+10 more)

### Community 3 - "Heuristic & Brand Feature Extraction"
Cohesion: 0.18
Nodes (8): detect_brand_impersonation(), extract_features_from_url(), levenshtein_distance(), normalize_homoglyphs(), AEGIS Multi-Layer Defense Architecture, AEGIS Mid-Semester Progress Review Report, Algorithmic Brand Impersonation Hunter, 20 Structural Lexical Features Specification

### Community 4 - "Presentation Deck Generator"
Cohesion: 0.18
Nodes (4): add_header(), build_presentation(), create_card(), set_dark_background()

### Community 6 - "DOM Injection & Content Script"
Cohesion: 0.36
Nodes (8): applyHighlight(), attachTooltipEvents(), getEligibleTargets(), getOrCreateGlobalTooltip(), isGoogleSearch(), scanPageLinks(), AEGIS Security Shield Branding Assets, Chrome Extension Popup User Interface

## Knowledge Gaps
- **7 isolated node(s):** `AEGIS Multi-Layer Defense Architecture`, `AEGIS Technical Dependencies Specification`, `AEGIS Mid-Semester Progress Review Report`, `Algorithmic Brand Impersonation Hunter`, `Adversarial Mutation Playground Engine` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 59 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `detect_brand_impersonation()` connect `Heuristic & Brand Feature Extraction` to `FastAPI Backend & Database`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **What connects `AEGIS Multi-Layer Defense Architecture`, `AEGIS Technical Dependencies Specification`, `AEGIS Mid-Semester Progress Review Report` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FastAPI Backend & Database` be split into smaller, more focused modules?**
  _Cohesion score 0.12873563218390804 - nodes in this community are weakly interconnected._
- **Why does `extract_features_from_url()` connect `Heuristic & Brand Feature Extraction` to `FastAPI Backend & Database`, `ML Training & Streamlit Dashboard`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Should `ML Training & Streamlit Dashboard` be split into smaller, more focused modules?**
  _Cohesion score 0.14619883040935672 - nodes in this community are weakly interconnected._
- **Should `Chrome Extension Configuration` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._