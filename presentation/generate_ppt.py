"""
AEGIS - Engineering Design & Innovation Project 1 (EDI 1)
High-Tech Industrial Cyber-Defense Presentation Generator (13 Slides)
Department of Engineering Sciences and Humanities (DESH)
Vishwakarma Institute of Technology (VIT Pune)

Version 3: Polished Typography, Non-Overflowing Header Layouts,
Enhanced Text Readability, and Cleaned Team Role Designations.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# --- Industrial Cyber-Defense Theme Palette ---
COLOR_BG_DARK = RGBColor(7, 13, 24)         # #070D18 Deep Midnight Slate Canvas
COLOR_CARD_DARK = RGBColor(15, 25, 44)      # #0F192C High-Tech Navy Card
COLOR_CARD_ALT = RGBColor(20, 34, 58)       # #14223A Alternating Row Tone
COLOR_BORDER_SUBTLE = RGBColor(31, 48, 78)  # #1F304E Subtle Slate Border
COLOR_BORDER_GLOW = RGBColor(0, 180, 216)   # #00B4D8 Glowing Cyan Border

# Vibrant Abstract Accents (Restrained for Corporate/Industrial Deck)
COLOR_NEON_CYAN = RGBColor(0, 229, 255)     # #00E5FF Primary Electric Blue
COLOR_NEON_GREEN = RGBColor(0, 245, 155)    # #00F59B Vibrant Emerald (Safe / Success)
COLOR_NEON_ORANGE = RGBColor(255, 170, 0)   # #FFAA00 High-Voltage Amber (Warning / Insights)
COLOR_NEON_RED = RGBColor(255, 75, 110)     # #FF4B6E Crimson Laser (Danger / Evasion)
COLOR_NEON_PURPLE = RGBColor(168, 85, 247)  # #A855F7 Electric Violet (Deep Tech / ML)

# High-Contrast Typography Colors
COLOR_TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC Pure Crisp Heading White
COLOR_TEXT_SLATE = RGBColor(203, 213, 225)  # #CBD5E1 High-Legibility Body Text (Light Slate)
COLOR_TEXT_DIM = RGBColor(148, 163, 184)    # #94A3B8 Secondary Explanatory Text

FONT_FAMILY = "Segoe UI"

def set_dark_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG_DARK

def add_header(slide, title_text, category_pill=None, slide_num=None):
    """Draws a sleek, industrial-grade header with non-overflowing dynamic pill and title."""
    # Top neon accent line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.06))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = COLOR_NEON_CYAN
    top_line.line.fill.background()

    # Category Pill Tag (Dynamically sized to completely prevent text overflow)
    if category_pill:
        clean_pill = f"  //  {category_pill.upper()}  //"
        # Dynamic width based on character count (prevents heading clipping)
        pill_w = min(Inches(7.2), max(Inches(3.2), Inches(len(clean_pill) * 0.082)))
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.18), pill_w, Inches(0.28))
        pill.fill.solid()
        pill.fill.fore_color.rgb = COLOR_CARD_DARK
        pill.line.color.rgb = COLOR_BORDER_SUBTLE
        pill.line.width = Pt(1)
        tf_p = pill.text_frame
        tf_p.word_wrap = False
        tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_p.margin_left = Inches(0.1)
        tf_p.margin_right = Inches(0.1)
        tf_p.margin_top = 0
        tf_p.margin_bottom = 0
        p_pill = tf_p.paragraphs[0]
        p_pill.text = clean_pill
        p_pill.font.name = FONT_FAMILY
        p_pill.font.size = Pt(8.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = COLOR_NEON_CYAN

    # Main Slide Title (Generous width and controlled font size to prevent multi-line collision)
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.50), Inches(9.8), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_FAMILY
    p_t.font.size = Pt(17.5)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TEXT_WHITE

    # Right-hand Metadata / Counter
    counter_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.32), Inches(2.233), Inches(0.5))
    tf_c = counter_box.text_frame
    tf_c.word_wrap = False
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.alignment = PP_ALIGN.RIGHT
    p_c.text = f"CSE-AI-B | Group 06" if slide_num is None else f"VIT PUNE  •  Slide {slide_num:02d}/13"
    p_c.font.name = FONT_FAMILY
    p_c.font.size = Pt(9.5)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_NEON_CYAN

    p_c_sub = tf_c.add_paragraph()
    p_c_sub.alignment = PP_ALIGN.RIGHT
    p_c_sub.text = "EDI 1 Mid-Semester Review"
    p_c_sub.font.name = FONT_FAMILY
    p_c_sub.font.size = Pt(8)
    p_c_sub.font.color.rgb = COLOR_TEXT_DIM

    # Sleek Divider Line (Placed at 1.22 inches, comfortably below the title)
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.22), Inches(12.133), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_BORDER_SUBTLE
    div.line.fill.background()

def create_card(slide, left, top, width, height, accent_color=None, bg_color=COLOR_CARD_DARK, border_color=COLOR_BORDER_SUBTLE):
    """Creates a high-contrast container with optional neon top border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)

    if accent_color:
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.06))
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent_color
        strip.line.fill.background()

    return card

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: OFFICIAL COLLEGE NOTICE TITLE SLIDE
    # (Notice Template Compliant, High-Tech Industrial Styling, Leader Tag Removed)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_dark_background(s1)

    # Outer decorative frame
    outer_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.3), Inches(12.533), Inches(6.9))
    outer_box.fill.background()
    outer_box.line.color.rgb = COLOR_BORDER_GLOW
    outer_box.line.width = Pt(2)

    # Top Header Banner
    header_box = s1.shapes.add_textbox(Inches(0.6), Inches(0.42), Inches(12.133), Inches(0.4))
    tf_h = header_box.text_frame
    p_h = tf_h.paragraphs[0]
    p_h.alignment = PP_ALIGN.CENTER
    p_h.text = "ENGINEERING DESIGN AND INNOVATION PROJECT 1 (EDI1)- PPT FOR MID SEMESTER REVIEW -  NOVEMBER 2026"
    p_h.font.name = FONT_FAMILY
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = COLOR_NEON_CYAN

    # Title Box (Notice Specification)
    title_rect = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(1.6))
    title_rect.fill.solid()
    title_rect.fill.fore_color.rgb = COLOR_CARD_DARK
    title_rect.line.color.rgb = COLOR_NEON_CYAN
    title_rect.line.width = Pt(1.5)
    tf_tr = title_rect.text_frame
    tf_tr.word_wrap = True
    tf_tr.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_lbl = tf_tr.paragraphs[0]
    p_lbl.alignment = PP_ALIGN.CENTER
    p_lbl.text = "EDI PROJECT 1_TITLE :-"
    p_lbl.font.name = FONT_FAMILY
    p_lbl.font.size = Pt(12)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_NEON_CYAN

    p_proj = tf_tr.add_paragraph()
    p_proj.alignment = PP_ALIGN.CENTER
    p_proj.text = "AEGIS: A Multi-Layer Machine Learning Framework for Cross-Platform\nPhishing Detection and Explainable Threat Assessment"
    p_proj.font.name = FONT_FAMILY
    p_proj.font.size = Pt(16.5)
    p_proj.font.bold = True
    p_proj.font.color.rgb = COLOR_TEXT_WHITE

    # Metadata Row
    meta_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.55), Inches(11.733), Inches(0.4))
    tf_meta = meta_box.text_frame
    p_meta = tf_meta.paragraphs[0]
    p_meta.alignment = PP_ALIGN.CENTER
    p_meta.text = "Div:- CSE-AI-B          EDIP1_GROUP No :- 06          Day:- Monday          Date:- 16/11/2026"
    p_meta.font.name = FONT_FAMILY
    p_meta.font.size = Pt(12.5)
    p_meta.font.bold = True
    p_meta.font.color.rgb = COLOR_NEON_GREEN

    # Left Box: Presented By (Clean list without any leader designation)
    pres_rect = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.05), Inches(6.8), Inches(2.8))
    pres_rect.fill.solid()
    pres_rect.fill.fore_color.rgb = COLOR_CARD_DARK
    pres_rect.line.color.rgb = COLOR_BORDER_SUBTLE
    pres_rect.line.width = Pt(1.5)
    tf_pres = pres_rect.text_frame
    tf_pres.word_wrap = True
    tf_pres.vertical_anchor = MSO_ANCHOR.TOP

    p_pres_h = tf_pres.paragraphs[0]
    p_pres_h.text = "Presented by"
    p_pres_h.font.name = FONT_FAMILY
    p_pres_h.font.size = Pt(12)
    p_pres_h.font.bold = True
    p_pres_h.font.color.rgb = COLOR_NEON_CYAN

    students = [
        ("1) Dandnaik Shreyash Somnath", "PRN: 12612242", "Roll: 225"),
        ("2) Dange Sharwal Shailesh",     "PRN: 12610050", "Roll: 226"),
        ("3) Darade Rohan Rajendra",      "PRN: 12611258", "Roll: 227"),
        ("4) Darsh Hemantkumar Raut",     "PRN: 12611013", "Roll: 228"),
        ("5) Darsh Jain",                 "PRN: 12611575", "Roll: 229")
    ]
    for name, prn, roll in students:
        p_s = tf_pres.add_paragraph()
        p_s.text = f"{name}  ({prn})  •  {roll}"
        p_s.font.name = FONT_FAMILY
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = COLOR_TEXT_WHITE
        p_s.font.bold = False

    # Right Box: Project Guide
    guide_rect = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.8), Inches(3.05), Inches(4.733), Inches(2.8))
    guide_rect.fill.solid()
    guide_rect.fill.fore_color.rgb = COLOR_CARD_DARK
    guide_rect.line.color.rgb = COLOR_BORDER_SUBTLE
    guide_rect.line.width = Pt(1.5)
    tf_guide = guide_rect.text_frame
    tf_guide.word_wrap = True
    tf_guide.vertical_anchor = MSO_ANCHOR.TOP

    p_guide_h = tf_guide.paragraphs[0]
    p_guide_h.text = "Project Guide"
    p_guide_h.font.name = FONT_FAMILY
    p_guide_h.font.size = Pt(12)
    p_guide_h.font.bold = True
    p_guide_h.font.color.rgb = COLOR_NEON_CYAN

    p_guide_n = tf_guide.add_paragraph()
    p_guide_n.text = "\nProf. Vidya Dhanve"
    p_guide_n.font.name = FONT_FAMILY
    p_guide_n.font.size = Pt(15)
    p_guide_n.font.bold = True
    p_guide_n.font.color.rgb = COLOR_TEXT_WHITE

    p_guide_d = tf_guide.add_paragraph()
    p_guide_d.text = "Assistant Professor\nDepartment of Engineering Sciences & Humanities\nVishwakarma Institute of Technology, Pune"
    p_guide_d.font.name = FONT_FAMILY
    p_guide_d.font.size = Pt(10.5)
    p_guide_d.font.color.rgb = COLOR_TEXT_DIM

    # Bottom Footer
    foot_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.75))
    tf_foot = foot_box.text_frame
    p_f1 = tf_foot.paragraphs[0]
    p_f1.alignment = PP_ALIGN.CENTER
    p_f1.text = "DEPARTMENT OF ENGINEERING SCIENCES AND HUMANITIES (DESH)"
    p_f1.font.name = FONT_FAMILY
    p_f1.font.size = Pt(12)
    p_f1.font.bold = True
    p_f1.font.color.rgb = COLOR_TEXT_WHITE

    p_f2 = tf_foot.add_paragraph()
    p_f2.alignment = PP_ALIGN.CENTER
    p_f2.text = "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE"
    p_f2.font.name = FONT_FAMILY
    p_f2.font.size = Pt(13)
    p_f2.font.bold = True
    p_f2.font.color.rgb = COLOR_NEON_CYAN

    # =========================================================================
    # SLIDE 2: KEYPOINTS (Official Notice Slide 2 Agenda)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_dark_background(s2)
    add_header(s2, "KEYPOINTS", "Executive Presentation Agenda", 2)

    kp_data = [
        ("01", "Introduction to EDI Project Topic", "Global cyber threat landscape, 3.4B malicious links/day, zero-day evasion tactics, and flaws of current perimeter defenses.", COLOR_NEON_CYAN),
        ("02", "Objectives of the Project", "Quantitative engineering targets: >=95% accuracy, sub-20ms latency, calibrated 0 - 100 threat scoring, and unified API.", COLOR_NEON_CYAN),
        ("03", "Literature Review (8 IEEE Papers)", "Comprehensive survey of 8 state-of-the-art IEEE papers (2024 - 2026) formatted in the mandatory 7-column tabular structure.", COLOR_NEON_PURPLE),
        ("04", "Materials and Components Used", "Dataset curation (2,400 benchmark samples), runtime specifications, Manifest V3 sandbox, and SQLite transactional schema.", COLOR_NEON_PURPLE),
        ("05", "Tools and Software Used", "Python 3.14, FastAPI asynchronous ASGI, Uvicorn, scikit-learn, Streamlit, and Rubric 5 technical Viva defense focus.", COLOR_NEON_ORANGE),
        ("06", "Methodology Implemented", "7-layer inspection pipeline, 20 lexical features, Random Forest classifier, and Brand Impersonation Hunter.", COLOR_NEON_ORANGE),
        ("07", "Progress Made So Far", "100% operational prototype: trained ML model (100% test accuracy), live API, Chrome extension, and dashboard.", COLOR_NEON_GREEN),
        ("08", "Present Status of the Project", "Live working status, Form FF 180 Page 3 completion, and empirical validation ready for review.", COLOR_NEON_GREEN)
    ]

    card_w = Inches(5.9)
    card_h = Inches(1.24)
    for idx, (num, title, desc, acc_col) in enumerate(kp_data):
        row = idx % 4
        col = idx // 4
        cx = Inches(0.6) if col == 0 else Inches(6.833)
        cy = Inches(1.35) + row * Inches(1.40)

        create_card(s2, cx, cy, card_w, card_h, accent_color=acc_col)

        # Number badge
        badge = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.18), cy + Inches(0.18), Inches(0.65), Inches(0.85))
        badge.fill.solid()
        badge.fill.fore_color.rgb = COLOR_CARD_ALT
        badge.line.color.rgb = acc_col
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        p_b.text = num
        p_b.font.name = FONT_FAMILY
        p_b.font.size = Pt(15)
        p_b.font.bold = True
        p_b.font.color.rgb = acc_col

        # Text Details
        tb = s2.shapes.add_textbox(cx + Inches(0.95), cy + Inches(0.10), card_w - Inches(1.1), card_h - Inches(0.18))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = f"{int(num)}. {title}"
        p_t.font.name = FONT_FAMILY
        p_t.font.size = Pt(12.5)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_FAMILY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = COLOR_TEXT_SLATE
        p_d.space_before = Pt(3)

    # =========================================================================
    # SLIDE 3: POINT 3 — LITERATURE REVIEW (PART 1: PAPERS 1 TO 4)
    # Exact Notice Format: 7 Columns with Legible Font Sizes
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_dark_background(s3)
    add_header(s3, "3. Literature Review: State-of-the-Art Research (Part 1/2)", "Rubric 2: Literature Review - 10 Marks", 3)

    col_widths = [Inches(0.55), Inches(2.5), Inches(1.65), Inches(1.35), Inches(1.05), Inches(2.65), Inches(2.383)]
    num_rows = 5
    table_shape = s3.shapes.add_table(num_rows, 7, Inches(0.6), Inches(1.35), Inches(12.133), Inches(5.6))
    tbl = table_shape.table

    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    headers_text = [
        "Sr.\nNo",
        "Title of Research Paper",
        "Authors",
        "Name of Journal /\nConference",
        "Date of Pub.\n(Month/Year)",
        "Brief Summary of Work\n(2/3 lines technical depth)",
        "Remarks (Key Findings /\nIMP Technology / Tools Used)"
    ]

    for col_idx, h_text in enumerate(headers_text):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD_ALT
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_CYAN

    papers_part1 = [
        (
            "1",
            "Enhancing Online Safety: Phishing URL Detection Using Machine Learning and Explainable AI",
            "B. V. Pavani,\nD. Mahitha,\nB. U. Maheswari",
            "IEEE ICCCNT",
            "Jul 2024",
            "Benchmarked 10 ML classifiers on URL datasets; applied SHAP and LIME algorithms to interpret Gini impurity tree splits and provide transparent decision attribution.",
            "Proved Random Forest achieved top precision (>96.4%); established empirical proof that explainable threat factors are required over opaque black-box AI."
        ),
        (
            "2",
            "Evaluating the Impact of Feature Engineering in Phishing URL Detection",
            "Y. A. Kustiawan,\nK. I. Ghauth",
            "IEEE Access",
            "Feb 2025",
            "Conducted extensive latency-accuracy trade-off evaluations comparing URL lexical attributes against heavy DOM HTML parsing and external reputation lookups.",
            "Demonstrated that lexical features yield >90% precision with <1ms CPU latency, proving ideal for zero-latency inline browser DOM interception."
        ),
        (
            "3",
            "PhishOFE: A Novel Machine Learning Framework for Real-Time Phishing Detection",
            "Y. A. Kustiawan,\nK. I. Ghauth",
            "IEEE Access",
            "Aug 2025",
            "Engineered an optimized dimensional reduction pipeline that eliminates redundant lexical noise while maximizing throughput on high-velocity web traffic streams.",
            "CatBoost reached 99.45% accuracy; highlighted the necessity of client-side feature hashing and caching to prevent web page rendering stalls."
        ),
        (
            "4",
            "Explainable Machine Learning Framework for Phishing URL Detection with a Realistic Large-Scale Dataset",
            "E. Ozcelik,\nF. Elsilk,\nM. Osmanoglu",
            "IEEE ICHORA",
            "May 2026",
            "Evaluated explainable decision boundaries across 579,920 real-world URLs, mapping anomalous feature distributions directly to modern attacker evasion tactics.",
            "Identified that raw IP presence, subdomain depth, and shortener redirection contribute >60% of predictive splits; directly inspired AEGIS feature weights."
        )
    ]

    for row_idx, data in enumerate(papers_part1, start=1):
        for col_idx, text in enumerate(data):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_DARK if row_idx % 2 == 1 else COLOR_CARD_ALT
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_TEXT_WHITE
            if col_idx in [0, 3, 4]:
                p.alignment = PP_ALIGN.CENTER
                if col_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_NEON_CYAN
            elif col_idx == 1:
                p.font.bold = True

    # =========================================================================
    # SLIDE 4: POINT 3 — LITERATURE REVIEW (PART 2: PAPERS 5 TO 8 & SYNTHESIS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_dark_background(s4)
    add_header(s4, "3. Literature Review: Papers 5 to 8 & Research Gap Synthesis", "Rubric 2: Literature Review - 10 Marks", 4)

    # Top Table: Papers 5 to 8
    table_shape2 = s4.shapes.add_table(5, 7, Inches(0.6), Inches(1.32), Inches(12.133), Inches(3.6))
    tbl2 = table_shape2.table

    for i, w in enumerate(col_widths):
        tbl2.columns[i].width = w

    for col_idx, h_text in enumerate(headers_text):
        cell = tbl2.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD_ALT
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_CYAN

    papers_part2 = [
        (
            "5",
            "Phishing Website Detection Using Deep Learning Models",
            "U. Zara,\nK. Ayyub,\nH. U. Khan et al.",
            "IEEE Access",
            "Oct 2024",
            "Evaluated character-level CNN and BiLSTM neural networks to parse raw character sequences without requiring manual feature extraction pipelines.",
            "High accuracy (97.8%) but high GPU inference latency (>180ms) makes pure deep learning unsuitable for instant, zero-lag browser DOM injection."
        ),
        (
            "6",
            "DEPHIDES: Deep Learning Based Phishing Detection System",
            "O. K. Sahingoz,\nE. Buber,\nE. Kugu",
            "IEEE Access",
            "Jan 2024",
            "Architected a hybrid defense engine combining word-level character embeddings with gradient boosted trees to intercept evasive phishing campaigns.",
            "Confirmed hybrid architectures combining heuristic filtering with tree ensembles provide 34% better zero-day resilience than static blacklists."
        ),
        (
            "7",
            "Enhancing Malicious URL Detection: A Novel Framework Leveraging Priority Coefficient",
            "A. S. Rafsanjani,\nN. B. Kamaruddin et al.",
            "IEEE Access",
            "Jun 2024",
            "Formulated a multi-tiered filtering mechanism assigning weighted priority coefficients to lexical flags before invoking deep model inspection.",
            "Directly inspired AEGIS's tiered multi-layer architecture: Layer 1 lexical heuristics filter obvious cases instantly before invoking ML inference."
        ),
        (
            "8",
            "Decoding Phishing Evasion: Analyzing Attacker Strategies to Circumvent Detection",
            "A. Ghafoor,\nM. A. Shah,\nC. Maple",
            "IEEE Access",
            "May 2025",
            "Systematically surveyed modern attacker evasion tactics including homoglyphs, Punycode tricks, open redirects, and subdomain cloaking.",
            "Proved necessity of combining brand impersonation hunting (Levenshtein + homoglyph normalization) with machine learning."
        )
    ]

    for row_idx, data in enumerate(papers_part2, start=1):
        for col_idx, text in enumerate(data):
            cell = tbl2.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_DARK if row_idx % 2 == 1 else COLOR_CARD_ALT
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_TEXT_WHITE
            if col_idx in [0, 3, 4]:
                p.alignment = PP_ALIGN.CENTER
                if col_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_NEON_CYAN
            elif col_idx == 1:
                p.font.bold = True

    # Bottom Synthesis Card: Research Gaps & AEGIS Contributions
    create_card(s4, Inches(0.6), Inches(5.1), Inches(12.133), Inches(1.85), accent_color=COLOR_NEON_PURPLE)
    tb_syn = s4.shapes.add_textbox(Inches(0.8), Inches(5.18), Inches(11.733), Inches(1.68))
    tf_syn = tb_syn.text_frame
    tf_syn.word_wrap = True

    p = tf_syn.paragraphs[0]
    p.text = "RESEARCH GAPS IDENTIFIED & ARCHITECTURAL CONTRIBUTIONS OF AEGIS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_PURPLE

    synth_points = [
        "Gap 1 (Inference Latency): Deep Learning models (Zara 2024) exceed 180ms, causing browser freezing. -> AEGIS solves this using 20 lexical features with Random Forest achieving <0.8ms inference.",
        "Gap 2 (Zero-Day Typosquatting): Attackers craft lookalikes ('paypa1.com') that bypass standard ML. -> AEGIS implements an active Brand Impersonation Hunter combining visual homoglyphs and Levenshtein distance.",
        "Gap 3 (Black-Box AI): Classifiers output raw probabilities without explanation. -> AEGIS decodes decision splits into plain-English reasons displayed via interactive floating browser tooltips."
    ]
    for pt in synth_points:
        p = tf_syn.add_paragraph()
        p.text = "▸ " + pt
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 5: POINT 1 — INTRODUCTION TO THE EDI PROJECT TOPIC
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_dark_background(s5)
    add_header(s5, "1. Introduction to the EDI Project Topic & Threat Landscape", "Rubric 1: Problem Statement & Domain Context", 5)

    w_card = Inches(3.85)
    h_card = Inches(5.6)
    gap = Inches(0.28)
    left_start = Inches(0.6)

    # Card 1: The Escalating Threat
    create_card(s5, left_start, Inches(1.35), w_card, h_card, accent_color=COLOR_NEON_RED)
    tb1 = s5.shapes.add_textbox(left_start + Inches(0.2), Inches(1.5), w_card - Inches(0.4), h_card - Inches(0.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "THE ESCALATING THREAT"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_RED

    p = tf1.add_paragraph()
    p.text = "Modern Phishing & Evasion Tactics"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    c1_bullets = [
        ("Global Threat Volume", "Over 3.4 billion phishing emails and malicious URLs generated globally every single day."),
        ("Transient Domain Lifespans", "60%+ of attack domains survive for less than 4 hours, completing credential theft campaigns before traditional crawlers index them."),
        ("Deceptive Typosquatting", "Cybercriminals exploit visual homoglyphs ('paypa1.com', 'g00gle.com') and brand-in-subdomain nesting ('paypal.com.verify-user.tk')."),
        ("Cognitive Human Vulnerability", "85%+ of non-technical users fail to spot subtle character-level manipulations in search links or messaging apps.")
    ]
    for title, desc in c1_bullets:
        p = tf1.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.space_before = Pt(8)

        run = p.add_run()
        run.text = desc
        run.font.name = FONT_FAMILY
        run.font.size = Pt(10)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_SLATE

    # Card 2: Industry Bottlenecks
    create_card(s5, left_start + w_card + gap, Inches(1.35), w_card, h_card, accent_color=COLOR_NEON_ORANGE)
    tb2 = s5.shapes.add_textbox(left_start + w_card + gap + Inches(0.2), Inches(1.5), w_card - Inches(0.4), h_card - Inches(0.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "INDUSTRY DEFENSE FAILURES"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_ORANGE

    p = tf2.add_paragraph()
    p.text = "Why Existing Tools Fall Short"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    c2_bullets = [
        ("Lagging Centralized Blacklists", "Google Safe Browsing and commercial feeds suffer from 24 - 48 hour indexing latency on newly minted zero-day domains."),
        ("Post-Click Interception Shields", "Traditional antivirus tools only trigger after link navigation begins, risking drive-by malware and instant session token logging."),
        ("Opaque 'Black-Box' Classifiers", "Modern ML systems output arbitrary risk labels without explaining why a domain is untrustworthy, missing crucial education."),
        ("Prohibitive Latency Overhead", "Heavy neural networks (CNN/LSTM) introduce >180ms latency, causing browser UI freeze and high drop-off rates.")
    ]
    for title, desc in c2_bullets:
        p = tf2.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.space_before = Pt(8)

        run = p.add_run()
        run.text = desc
        run.font.name = FONT_FAMILY
        run.font.size = Pt(10)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_SLATE

    # Card 3: The AEGIS Solution
    create_card(s5, left_start + (w_card + gap) * 2, Inches(1.35), w_card, h_card, accent_color=COLOR_NEON_GREEN)
    tb3 = s5.shapes.add_textbox(left_start + (w_card + gap) * 2 + Inches(0.2), Inches(1.5), w_card - Inches(0.4), h_card - Inches(0.3))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "THE PROPOSED INNOVATION"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_GREEN

    p = tf3.add_paragraph()
    p.text = "AEGIS Proactive Hybrid Defense"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    c3_bullets = [
        ("Proactive Pre-Click Defense", "Evaluates and badges links directly inside the browser DOM before the user ever initiates a navigation click."),
        ("Multi-Tier Hybrid Architecture", "Combines Layer 1 lexical parsing, Layer 2 homoglyph brand hunting, and Layer 3 Random Forest classification."),
        ("Sub-Millisecond Inference", "Executes in <0.8ms on CPU, delivering end-to-end batch scanning in <15ms with zero perceived browser lag."),
        ("Explainable Threat Assessment", "Translates decision tree splits into natural-language threat bullets (e.g., 'Unregistered IP with credential token').")
    ]
    for title, desc in c3_bullets:
        p = tf3.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.space_before = Pt(8)

        run = p.add_run()
        run.text = desc
        run.font.name = FONT_FAMILY
        run.font.size = Pt(10)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 6: POINT 2 — OBJECTIVES OF THE PROJECT
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_dark_background(s6)
    add_header(s6, "2. Objectives of the Project Activity", "Rubric 4: Project Objectives - 10 Marks", 6)

    gw = Inches(5.9)
    gh = Inches(2.65)
    gx0 = Inches(0.6)
    gx1 = Inches(6.833)
    gy0 = Inches(1.35)
    gy1 = Inches(4.25)

    objectives = [
        (
            gx0, gy0,
            "OBJECTIVE 1: HIGH-ACCURACY THREAT CLASSIFICATION",
            "Machine Learning Detection Pipeline",
            [
                ("Ensemble Classifier Benchmark", "Engineer an ensemble ML classifier achieving >= 95% detection accuracy and F1-score across balanced benchmark datasets."),
                ("Zero-Day Robustness", "Ensure robust generalization against both traditional credential harvesting and advanced obfuscated zero-day attack vectors."),
                ("Sub-20ms Latency Target", "Maintain inference execution latency under 20 ms per URL batch to guarantee seamless inline browser integration without slowing web browsing.")
            ],
            COLOR_NEON_CYAN
        ),
        (
            gx1, gy0,
            "OBJECTIVE 2: TRANSPARENT EXPLAINABILITY & THREAT SCORING",
            "Human-Centric Explainable AI (XAI)",
            [
                ("Calibrated Risk Score", "Produce a calibrated Risk Score (0 to 100) that maps directly into intuitive risk verdicts: SAFE (0 - 29), SUSPICIOUS (30 - 69), and DANGER (70 - 100)."),
                ("Decision Boundary Translation", "Translate complex machine learning decision-tree feature weights into plain-English threat factors displayed via interactive tooltips."),
                ("User Education", "Educate and alert the user by detailing why a URL is flagged (e.g., excessive subdomain nesting, high character entropy, IP-in-URL).")
            ],
            COLOR_NEON_PURPLE
        ),
        (
            gx0, gy1,
            "OBJECTIVE 3: ZERO-DAY BRAND IMPERSONATION HUNTER",
            "Algorithmic Typosquatting Defense",
            [
                ("Algorithmic Protection", "Develop an algorithmic brand protection module combining Levenshtein Edit Distance and visual homoglyph substitution mappings."),
                ("High-Profile Brand Defense", "Detect deceptive lookalike domains mimicking high-value institutional and financial brands (Google, PayPal, Microsoft, SBI, Netflix)."),
                ("Blacklist Independence", "Eliminate reliance on lagging third-party blacklists by instantly identifying unauthorized impersonations on synthetic domains.")
            ],
            COLOR_NEON_ORANGE
        ),
        (
            gx1, gy1,
            "OBJECTIVE 4: UNIFIED CROSS-PLATFORM ARCHITECTURE",
            "Scalable Microservice & Client Integration",
            [
                ("Asynchronous Microservice", "Construct an asynchronous RESTful microservice API using FastAPI to serve multiple client platforms from a single centralized engine."),
                ("Chrome Extension (Manifest V3)", "Implement a lightweight Chrome Extension (Manifest V3) that injects non-blocking risk indicators into Google Search results and web pages."),
                ("Interactive Telemetry Portal", "Deploy an interactive Streamlit administrative dashboard featuring real-time scan telemetry and an Adversarial Mutation Playground.")
            ],
            COLOR_NEON_GREEN
        )
    ]

    for x, y, tag, title, bullets, accent_col in objectives:
        create_card(s6, x, y, gw, gh, accent_color=accent_col)

        tb = s6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), gw - Inches(0.4), gh - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tag
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = accent_col

        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE

        for b_title, b_desc in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b_title}: "
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_WHITE
            p.space_before = Pt(3)

            run = p.add_run()
            run.text = b_desc
            run.font.name = FONT_FAMILY
            run.font.size = Pt(9.5)
            run.font.bold = False
            run.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 7: POINT 4 — MATERIALS AND COMPONENTS USED (DEEP DIVE)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_dark_background(s7)
    add_header(s7, "4. Materials and Components Used: Technical Specifications", "Point 4: Engineering Materials, Datasets & Infrastructure", 7)

    col_w4 = Inches(2.83)
    col_gap4 = Inches(0.25)
    col_top = Inches(1.35)
    col_h7 = Inches(5.6)

    materials_spec = [
        (
            "CURATED BENCHMARK DATASET",
            "2,400 Verified Samples",
            COLOR_NEON_CYAN,
            [
                ("1,200 Legitimate URLs", "Curated from Alexa Top 1M and Tranco list; covers global banking, enterprise SaaS, e-commerce, and university portals (vit.edu, google.com, sbi.co.in)."),
                ("1,200 Phishing Attacks", "Curated from PhishTank verified active feeds, OpenPhish repository, and adversarial evasive samples modeling credential harvesting."),
                ("Stratified 80/20 Split", "1,920 URLs allocated for training and 480 held-out test URLs; class distribution balanced 50:50 across train and test partitions."),
                ("Feature Matrix Storage", "Exported as structured tabular matrix aegis_dataset.csv (334 KB) with 20 normalized lexical dimensions.")
            ]
        ),
        (
            "HARDWARE & RUNTIME SPECS",
            "Deterministic Execution",
            COLOR_NEON_PURPLE,
            [
                ("Host Processor", "Intel/AMD x86_64 architecture operating on Windows 11; sub-second CPU training duration (~1.8 seconds)."),
                ("Python Runtime", "Python 3.14.5 64-bit; leverages optimized bytecode compilation and streamlined C-extensions for regex and string math."),
                ("Single-Threaded Tuning", "Enforced n_jobs=1 in RandomForestClassifier to eliminate Windows multiprocessing spawn deadlocks on Python 3.14."),
                ("Serialized Persistence", "Trained model weights serialized via Joblib into aegis_model.pkl (172 KB) enabling cold-start inference in <12 ms.")
            ]
        ),
        (
            "BROWSER CLIENT COMPONENTS",
            "Manifest V3 Sandbox",
            COLOR_NEON_ORANGE,
            [
                ("Chrome Manifest V3", "Declarative extension architecture; background service workers; strict Content Security Policy (CSP); zero arbitrary remote code execution."),
                ("MutationObserver API", "DOM event-driven observer monitoring #search container for dynamically inserted links and infinite scroll events."),
                ("Memory Isolation", "Zero persistent memory leaks; content script scopes variables inside IIFE; link states tracked via local Set data structures."),
                ("CSS Component Layer", "Isolation of #aegis-global-tooltip attached directly to document.body with z-index: 2147483647 preventing host page interference.")
            ]
        ),
        (
            "DATABASE PERSISTENCE LAYER",
            "SQLite ACID Storage",
            COLOR_NEON_GREEN,
            [
                ("Transactional Database", "Embedded SQLite 3 (backend/aegis.db, 405 KB) requiring zero external database server administration."),
                ("Audit Schema Design", "scans table storing id, url, url_hash, risk_score, verdict, latency_ms, reasons_json, and timestamp."),
                ("High-Speed Indexing", "B-Tree index on url_hash (SHA-256) and timestamp delivering sub-5ms query response on 100,000+ historical records."),
                ("Thread-Safe Locking", "Python sqlite3 context management enforcing WAL (Write-Ahead Logging) mode for concurrent read/write transactions.")
            ]
        )
    ]

    for idx, (head, subhead, col_accent, items) in enumerate(materials_spec):
        cx = Inches(0.6) + idx * (col_w4 + col_gap4)
        create_card(s7, cx, col_top, col_w4, col_h7, accent_color=col_accent)

        tb = s7.shapes.add_textbox(cx + Inches(0.15), col_top + Inches(0.12), col_w4 - Inches(0.3), col_h7 - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = head
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col_accent

        p = tf.add_paragraph()
        p.text = subhead
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE

        for title, detail in items:
            p = tf.add_paragraph()
            p.text = "▸ " + title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_WHITE
            p.space_before = Pt(8)

            p_sub = tf.add_paragraph()
            p_sub.text = detail
            p_sub.font.name = FONT_FAMILY
            p_sub.font.size = Pt(9)
            p_sub.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 8: POINT 5 — TOOLS AND SOFTWARE USED (RUBRIC 5 DEEP DIVE)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_dark_background(s8)
    add_header(s8, "5. Tools and Software Used: Software Architecture & Viva Defense", "Rubric 5: Viva on Domain, Tools & Technology - 10 Marks", 8)

    sw_top = Inches(1.35)
    sw_h = Inches(3.7)
    sw_w = Inches(2.83)

    software_pillars = [
        (
            "BACKEND MICROSERVICE",
            "FastAPI & Uvicorn",
            COLOR_NEON_CYAN,
            [
                ("FastAPI 0.162.0", "Asynchronous ASGI framework leveraging Python's async/await event loop for non-blocking concurrent request handling."),
                ("Uvicorn 0.54.0", "High-performance ASGI production web server handling concurrent HTTP connections."),
                ("Pydantic v2", "Strict schema validation and type enforcement for single (/scan) and batch (/scan-batch) payloads.")
            ]
        ),
        (
            "ML & DATA SCIENCE",
            "Scikit-Learn & Math",
            COLOR_NEON_PURPLE,
            [
                ("scikit-learn 1.9.1", "Implements RandomForestClassifier with Gini impurity splitting, tree pruning, and stratified k-fold splits."),
                ("NumPy & Pandas", "Vectorized array calculations, feature normalization, and dataset manipulation."),
                ("Joblib 1.6.0", "Optimized serialization of trained tree ensemble weights (aegis_model.pkl).")
            ]
        ),
        (
            "CLIENT DOM & EXTENSION",
            "JavaScript & Manifest V3",
            COLOR_NEON_ORANGE,
            [
                ("JavaScript (ES6+)", "Asynchronous fetch API, Promise-based batching, and error-resilient DOM traversal."),
                ("MutationObserver API", "Observes dynamic DOM mutations on Google Search, intercepting lazy-loaded links."),
                ("CSS3 / Flexbox", "Frosted-glass UI with backdrop blur; rigid height locks (18px) preventing flex distortion.")
            ]
        ),
        (
            "ANALYTICS & TOOLING",
            "Streamlit & Git",
            COLOR_NEON_GREEN,
            [
                ("Streamlit 1.66.1", "Reactive Python web dashboard; session-state caching; interactive Adversarial Playground."),
                ("Git & GitHub", "Distributed version control, branch management, and collaborative code auditing."),
                ("VS Code & Postman", "IDE development environment and automated REST API validation suite.")
            ]
        )
    ]

    for idx, (head, subhead, col_accent, items) in enumerate(software_pillars):
        cx = Inches(0.6) + idx * (sw_w + col_gap4)
        create_card(s8, cx, sw_top, sw_w, sw_h, accent_color=col_accent)

        tb = s8.shapes.add_textbox(cx + Inches(0.15), sw_top + Inches(0.1), sw_w - Inches(0.3), sw_h - Inches(0.18))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = head
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col_accent

        p = tf.add_paragraph()
        p.text = subhead
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE

        for title, detail in items:
            p = tf.add_paragraph()
            p.text = "▸ " + title
            p.font.name = FONT_FAMILY
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_WHITE
            p.space_before = Pt(6)

            p_sub = tf.add_paragraph()
            p_sub.text = detail
            p_sub.font.name = FONT_FAMILY
            p_sub.font.size = Pt(8.5)
            p_sub.font.color.rgb = COLOR_TEXT_SLATE

    # Bottom Viva Exam Focus Box
    create_card(s8, Inches(0.6), Inches(5.2), Inches(12.133), Inches(1.8), accent_color=COLOR_NEON_CYAN)
    tb_v = s8.shapes.add_textbox(Inches(0.8), Inches(5.28), Inches(11.733), Inches(1.6))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True

    p = tf_v.paragraphs[0]
    p.text = "RUBRIC 5 VIVA EXAMINATION PREPARATION: CORE DOMAIN & TECHNICAL SKILLSETS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_CYAN

    viva_qa = [
        ("Q1: Why choose Random Forest over Deep Neural Networks?", "URLs are short tabular lexical sequences. Random Forest evaluates in sub-milliseconds on CPU, avoids overfitting on small sets, and provides interpretable Gini feature importances."),
        ("Q2: How does FastAPI handle concurrent browser link batches?", "FastAPI utilizes an asynchronous event loop (async def) running on Uvicorn ASGI, processing concurrent batch requests without blocking database threads."),
        ("Q3: What is the computational complexity of the Brand Impersonation Hunter?", "Levenshtein distance dynamic programming runs in O(M x N) where M and N are string lengths (<25 chars), executing in <0.1ms per domain comparison.")
    ]
    for q, a in viva_qa:
        p = tf_v.add_paragraph()
        p.text = f"• {q} -> "
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.space_before = Pt(3)

        run = p.add_run()
        run.text = a
        run.font.name = FONT_FAMILY
        run.font.size = Pt(9)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 9: POINT 6 — METHODOLOGY: ARCHITECTURE & 7-LAYER PIPELINE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_dark_background(s9)
    add_header(s9, "6. Methodology: Architecture & 7-Layer Defense Pipeline", "Point 6: Designing, Algorithm Development & Implementation", 9)

    tw = Inches(2.83)
    th = Inches(1.9)
    t_gap = Inches(0.25)
    t_top = Inches(1.35)

    tiers = [
        ("TIER 1: CLIENT ENGINE", "Chrome Extension V3", "Observes DOM via MutationObserver. Extracts hyperlinks, hashes unique targets, and transmits async payloads.", COLOR_NEON_CYAN),
        ("TIER 2: API GATEWAY", "FastAPI Microservice", "Asynchronous REST gateway receiving /scan and /scan-batch requests. Validates URL syntax and orchestrates pipeline execution.", COLOR_NEON_PURPLE),
        ("TIER 3: DETECTION CORE", "Multi-Layer Engine", "Coordinates Layer 1 lexical parsing, Layer 2 authority whitelists, homoglyph hunting, and Layer 3 Random Forest inference.", COLOR_NEON_ORANGE),
        ("TIER 4: TELEMETRY & PERSIST", "SQLite & Streamlit", "Maintains an ACID-compliant scan history database (aegis.db) powering the real-time threat dashboard.", COLOR_NEON_GREEN)
    ]

    for idx, (t_title, t_sub, t_desc, t_col) in enumerate(tiers):
        tx = Inches(0.6) + idx * (tw + t_gap)
        create_card(s9, tx, t_top, tw, th, accent_color=t_col)

        tb = s9.shapes.add_textbox(tx + Inches(0.15), t_top + Inches(0.1), tw - Inches(0.3), th - Inches(0.18))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = t_title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = t_col

        p = tf.add_paragraph()
        p.text = t_sub
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE

        p = tf.add_paragraph()
        p.text = t_desc
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_SLATE
        p.space_before = Pt(4)

    # Bottom Pipeline Breakdown
    create_card(s9, Inches(0.6), Inches(3.45), Inches(12.133), Inches(3.55), accent_color=COLOR_NEON_CYAN)
    tb_p = s9.shapes.add_textbox(Inches(0.8), Inches(3.55), Inches(11.733), Inches(3.3))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    p.text = "THE 7-LAYER DEFENSE PIPELINE BREAKDOWN (MID-SEM STATUS: LAYERS 1 - 4 FULLY OPERATIONAL)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_CYAN

    layers_info = [
        ("Layer 1: Structural Lexical Extractor", "Implemented (<0.5 ms)", "Parses 20 syntactic attributes from raw URL characters without requiring DNS resolution or network roundtrips.", COLOR_NEON_GREEN),
        ("Layer 2: Authority Whitelist & Brand Hunter", "Implemented (<1.0 ms)", "Passes verified domains (google.com, vit.edu). Evaluates unauthorized domains via homoglyphs and Levenshtein distance against top targeted brands.", COLOR_NEON_GREEN),
        ("Layer 3: Random Forest Machine Learning Ensemble", "Implemented (<0.8 ms)", "100 decision trees evaluate the feature vector to generate a baseline phishing probability score (0.0 to 1.0) based on weighted Gini impurity splits.", COLOR_NEON_GREEN),
        ("Layer 4: Explainability & Threat Scorer", "Implemented (<0.2 ms)", "Calibrates Risk Score (0 - 100) and maps decision tree splits into human-readable bullet points displayed in interactive browser tooltips.", COLOR_NEON_GREEN),
        ("Layer 5: WHOIS Domain Age & Registrar Analysis", "Phase 2 Scope", "Queries RDAP/WHOIS protocols to inspect domain registration timestamps; heavily penalizes newly registered domains (<30 days old).", COLOR_NEON_ORANGE),
        ("Layer 6: SSL/TLS Certificate Chain Validation", "Phase 2 Scope", "Validates SSL certificate issuer authority, validity periods, and certificate chains, flagging suspicious zero-cost certificates abused on lookalikes.", COLOR_NEON_ORANGE),
        ("Layer 7: Redirect Crawler & Dynamic Sandboxing", "Phase 2 Scope", "Unfurls shortened URLs (bit.ly, t.co) to evaluate final landing endpoints and computes perceptual hashes of landing page logos.", COLOR_NEON_ORANGE)
    ]

    for title, status, desc, col in layers_info:
        p = tf_p.add_paragraph()
        p.text = f"• {title}  [{status}]: "
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_before = Pt(3)

        run = p.add_run()
        run.text = desc
        run.font.name = FONT_FAMILY
        run.font.size = Pt(9.5)
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 10: POINT 6 — METHODOLOGY: 20 LEXICAL FEATURES & ML PERFORMANCE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_dark_background(s10)
    add_header(s10, "6. Methodology: Feature Engineering & Random Forest Performance", "Point 6: 20 Lexical Features, Model Training & Empirical Metrics", 10)

    hw = Inches(5.9)
    hh = Inches(5.6)
    hy = Inches(1.35)

    # Left Card: 20 Lexical Features
    create_card(s10, Inches(0.6), hy, hw, hh, accent_color=COLOR_NEON_CYAN)
    tb_f = s10.shapes.add_textbox(Inches(0.8), hy + Inches(0.12), hw - Inches(0.4), hh - Inches(0.25))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True

    p = tf_f.paragraphs[0]
    p.text = "FEATURE ENGINEERING"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_CYAN

    p = tf_f.add_paragraph()
    p.text = "20 Extracted Lexical Structural Features"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    feat_groups = [
        ("Length Metrics (4 Features)", "url_length, domain_length, path_length, count_subdomains. Detects abnormally long URLs and deep subdomain nesting (>2 subdomains)."),
        ("Structural Delimiters (8 Features)", "count_dots (.), count_hyphens (-), count_slashes (/), count_underscores (_), count_at (@), count_question (?), count_equal (=), count_digits. Captures delimiter stuffing and parameter spoofing."),
        ("Security Indicators (4 Features)", "has_ip (detects raw IPv4 regex bypasses), is_shortened (flags bit.ly, tinyurl, t.co), has_https (transport security flag), digit_ratio (identifies algorithmic DGA domain generation)."),
        ("Information Theory & Keywords (4 Features)", "shannon_entropy (measures character randomness to catch DGA domains), suspicious_word_count (detects 'login', 'verify', 'update', 'account', 'secure', 'banking' tokens).")
    ]

    for grp_t, grp_d in feat_groups:
        p = tf_f.add_paragraph()
        p.text = "▸ " + grp_t
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_CYAN
        p.space_before = Pt(8)

        p_desc = tf_f.add_paragraph()
        p_desc.text = grp_d
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = COLOR_TEXT_SLATE

    # Right Card: ML Training & Empirical Performance
    create_card(s10, Inches(6.833), hy, hw, hh, accent_color=COLOR_NEON_GREEN)
    tb_ml = s10.shapes.add_textbox(Inches(7.033), hy + Inches(0.12), hw - Inches(0.4), hh - Inches(0.25))
    tf_ml = tb_ml.text_frame
    tf_ml.word_wrap = True

    p = tf_ml.paragraphs[0]
    p.text = "MODEL TRAINING & EMPIRICAL METRICS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_GREEN

    p = tf_ml.add_paragraph()
    p.text = "Random Forest Classifier Architecture"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    ml_highlights = [
        ("Ensemble Architecture", "RandomForestClassifier with 100 decision trees, Gini impurity splitting criterion, max_depth=15 to prevent overfitting, and deterministic random_state=42."),
        ("Training & Validation Split", "Stratified 80/20 split on 2,400 benchmark samples (1,920 training samples, 480 held-out test samples with balanced 50:50 distribution)."),
        ("Empirical Validation Results", "• Test Accuracy: 100.0% (Zero classification errors on test partition)\n• Precision: 1.0000  •  Recall: 1.0000  •  F1-Score: 1.0000\n• Confusion Matrix: [[TN=240, FP=0], [FN=0, TP=240]]"),
        ("Inference Speed Benchmark", "• CPU Feature Extraction: < 0.5 ms per URL\n• Model Evaluation: < 0.8 ms per URL\n• End-to-End API Roundtrip: < 15 ms for complete link batch"),
        ("Top Feature Importances", "has_https (30.47%), suspicious_word_count (19.41%), domain_length (12.15%), digit_ratio (6.52%), query_length (6.12%), count_hyphens (3.87%).")
    ]

    for title, desc in ml_highlights:
        p = tf_ml.add_paragraph()
        p.text = "▸ " + title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_GREEN
        p.space_before = Pt(6)

        p_desc = tf_ml.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 11: KEY INNOVATIONS — BRAND HUNTER & ADVERSARIAL PLAYGROUND
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_dark_background(s11)
    add_header(s11, "Key Innovations & Competitive Differentiation", "Closing Industry Blindspots: Typosquatting & Live Attack Mutation", 11)

    iw = Inches(5.9)
    ih = Inches(5.6)
    iy = Inches(1.35)

    # Card 1: Brand Impersonation Hunter
    create_card(s11, Inches(0.6), iy, iw, ih, accent_color=COLOR_NEON_CYAN)
    tb_b = s11.shapes.add_textbox(Inches(0.8), iy + Inches(0.12), iw - Inches(0.4), ih - Inches(0.25))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    p.text = "INNOVATION 1"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_CYAN

    p = tf_b.add_paragraph()
    p.text = "Real-Time Brand Impersonation Hunter"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    b_points = [
        ("The Industry Blindspot", "Attackers craft lookalike domains (e.g., 'paypa1.com', 'g00gle.com', 'arnazon.com') whose character lengths and dot counts look completely legitimate to standard ML classifiers."),
        ("Visual Homoglyph Canonicalization", "AEGIS maps deceptive visual character substitutions into standard Latin characters before comparison: '0'->'o', '1'->'l', '3'->'e', '4'->'a', '5'->'s', '8'->'b', '@'->'a', 'vv'->'w', 'rn'->'m'."),
        ("Levenshtein Edit Distance Algorithm", "Computes the minimal single-character edits (insertions, deletions, substitutions) required to transform the domain stem into a protected brand keyword (PayPal, Google, SBI, Microsoft, Apple, Amazon, VIT)."),
        ("Zero-Day Protection Without Blacklists", "If normalized edit distance is 1 or 2 on an unauthorized domain -> AEGIS immediately triggers a +55 Risk Score Penalty and flags DANGER (Brand Impersonation Detected) before external blacklists ever index it.")
    ]

    for title, desc in b_points:
        p = tf_b.add_paragraph()
        p.text = "▸ " + title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_CYAN
        p.space_before = Pt(8)

        p_desc = tf_b.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = COLOR_TEXT_SLATE

    # Card 2: Adversarial Mutation Playground
    create_card(s11, Inches(6.833), iy, iw, ih, accent_color=COLOR_NEON_ORANGE)
    tb_a = s11.shapes.add_textbox(Inches(7.033), iy + Inches(0.12), iw - Inches(0.4), ih - Inches(0.25))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True

    p = tf_a.paragraphs[0]
    p.text = "INNOVATION 2"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_ORANGE

    p = tf_a.add_paragraph()
    p.text = "Interactive Adversarial Mutation Playground"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    a_points = [
        ("The Academic Presentation Dilemma", "Most student projects present static screenshots with no mechanism for evaluators to test how the system reacts to active evasion tactics."),
        ("Interactive Sandbox in Dashboard", "AEGIS features a dedicated 'Adversarial Playground' tab in the live Streamlit dashboard allowing users and evaluators to mutate safe URLs on the fly."),
        ("Real-World Evasion Vectors Tested", "• Subdomain Spoofing: 'paypal.com.security-verify.tk'\n• Homoglyph Typosquatting: 'paypa1.com/login'\n• Raw Hex/IP Cloaking: '192.168.1.10/auth'\n• Delimiter & Keyword Stuffing: 'google.com-account-update'"),
        ("Live Side-by-Side Verification", "Instantly visualizes the baseline URL vs. mutated URL: risk score jump, delta feature importances, and exact explainability reasons triggered.")
    ]

    for title, desc in a_points:
        p = tf_a.add_paragraph()
        p.text = "▸ " + title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_ORANGE
        p.space_before = Pt(8)

        p_desc = tf_a.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(9.5)
        p_desc.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 12: POINTS 7 & 8 — PROGRESS MADE SO FAR & PRESENT STATUS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_dark_background(s12)
    add_header(s12, "7 & 8. Progress Made So Far & Present Status of the Project", "Points 7 & 8: Working Deliverables & Form FF 180 Page 3 Status", 12)

    pw = Inches(5.9)
    ph = Inches(5.6)
    py = Inches(1.35)

    # Left Card: Completed Engineering Deliverables
    create_card(s12, Inches(0.6), py, pw, ph, accent_color=COLOR_NEON_GREEN)
    tb_p = s12.shapes.add_textbox(Inches(0.8), py + Inches(0.12), pw - Inches(0.4), ph - Inches(0.25))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    p.text = "PROGRESS REVIEW 1 (MIDSEM MILESTONE)"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_GREEN

    p = tf_p.add_paragraph()
    p.text = "Completed & Verified Components"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    progress_items = [
        ("Layer 1 Feature Extraction Engine", "Operational with 20 lexical features; executed in sub-millisecond CPU speed with complete unit test verification."),
        ("Machine Learning Classifier Trained", "Random Forest ensemble trained on 2,400 benchmark samples; achieved 100% test accuracy and F1-score with serialized persistence."),
        ("FastAPI Asynchronous Microservice", "Fully functional backend running on 127.0.0.1:8000 handling single (/scan) and batch (/scan-batch) asynchronous requests."),
        ("Chrome Extension (Manifest V3)", "Installed in Chrome Developer Mode; successfully inspects Google Search results, rendering color-coded risk chips and floating tooltips."),
        ("Streamlit Telemetry Web Dashboard", "Operational on localhost:8501 showing real-time scan statistics, historical audit table, and the Adversarial Mutation Playground."),
        ("ISO Form FF 180 Page 3 Documentation", "Progress Review 1 report fully compiled with tasks completed, ongoing, and future scope, ready for Guide sign-off.")
    ]

    for title, desc in progress_items:
        p = tf_p.add_paragraph()
        p.text = "✔ " + title
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_GREEN
        p.space_before = Pt(5)

        p_desc = tf_p.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(9)
        p_desc.font.color.rgb = COLOR_TEXT_SLATE

    # Right Card: Present Status & Empirical Metrics
    create_card(s12, Inches(6.833), py, pw, ph, accent_color=COLOR_NEON_CYAN)
    tb_s = s12.shapes.add_textbox(Inches(7.033), py + Inches(0.12), pw - Inches(0.4), ph - Inches(0.25))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    p.text = "PRESENT STATUS & SYSTEM METRICS"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_CYAN

    p = tf_s.add_paragraph()
    p.text = "Live Working Benchmark Metrics"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_WHITE

    stat_boxes = [
        ("100.0%", "MODEL TEST ACCURACY", "Zero classification errors on 480 held-out test URLs"),
        ("< 15 ms", "INFERENCE LATENCY", "Complete API roundtrip response for inline browser batch"),
        ("20", "LEXICAL FEATURES", "Structural, delimiter, heuristic, and entropy metrics"),
        ("100%", "WORKING PROTOTYPE", "Extension, API, ML model, and Dashboard all operational")
    ]

    for m_val, m_lbl, m_sub in stat_boxes:
        p = tf_s.add_paragraph()
        p.text = f"{m_val} — {m_lbl}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_CYAN
        p.space_before = Pt(7)

        p_desc = tf_s.add_paragraph()
        p_desc.text = m_sub
        p_desc.font.name = FONT_FAMILY
        p_desc.font.size = Pt(9)
        p_desc.font.color.rgb = COLOR_TEXT_SLATE

    p_stat = tf_s.add_paragraph()
    p_stat.text = "Active Live Demonstration Status:"
    p_stat.font.name = FONT_FAMILY
    p_stat.font.size = Pt(10.5)
    p_stat.font.bold = True
    p_stat.font.color.rgb = COLOR_TEXT_WHITE
    p_stat.space_before = Pt(10)

    p_stat_d = tf_s.add_paragraph()
    p_stat_d.text = "The live system can be demonstrated instantly via start_aegis.bat during the review. Evaluators can perform live Google searches or test custom adversarial inputs on the fly."
    p_stat_d.font.name = FONT_FAMILY
    p_stat_d.font.size = Pt(9)
    p_stat_d.font.color.rgb = COLOR_TEXT_SLATE

    # =========================================================================
    # SLIDE 13: GROUP FORMATION, RESPONSIBILITY (RUBRIC 3) & CONCLUSION
    # (Cleaned: Leader Tag Removed for Darsh Raut, Perfectly Sized Table)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_dark_background(s13)
    add_header(s13, "Group Formation, Individual Responsibilities & Conclusion", "Rubric 3: Individual Responsibility - 10 Marks", 13)

    col_w13 = [Inches(0.55), Inches(2.2), Inches(0.85), Inches(1.05), Inches(3.7), Inches(3.783)]
    table_shape13 = s13.shapes.add_table(6, 6, Inches(0.6), Inches(1.3), Inches(12.133), Inches(4.0))
    tbl13 = table_shape13.table

    for i, w in enumerate(col_w13):
        tbl13.columns[i].width = w

    headers13 = [
        "Sr.\nNo",
        "Student Name",
        "Roll\nNo",
        "PRN No.",
        "Designated Individual Responsibility\n(Engineering Tasks & Modules Owned)",
        "Viva Examination Focus Area\n(Technical Domain & Skillsets)"
    ]

    for col_idx, h_text in enumerate(headers13):
        cell = tbl13.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD_ALT
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_NEON_CYAN

    # Member data with zero leader tags
    team_data = [
        (
            "1",
            "Dandnaik Shreyash Somnath",
            "225",
            "12612242",
            "Browser Security & DOM Engineering Lead:\n• Built Chrome Extension Manifest V3 background service worker.\n• Implemented MutationObserver DOM link extraction.\n• Developed floating explainable risk tooltips and styling.",
            "Manifest V3 architecture, service workers, DOM mutation handling, client-side security policies, and performance optimization."
        ),
        (
            "2",
            "Dange Sharwal Shailesh",
            "226",
            "12610050",
            "Threat Telemetry & Dashboard Analytics Lead:\n• Designed and implemented Streamlit analytics web portal.\n• Engineered real-time scan telemetry graphs and risk graphs.\n• Integrated live SQLite database transaction monitors.",
            "Reactive web application architecture, telemetry data visualization, statistical risk distributions, and database indexing."
        ),
        (
            "3",
            "Darade Rohan Rajendra",
            "227",
            "12611258",
            "Lexical Heuristics & Threat Intelligence Lead:\n• Researched modern phishing evasion tactics in IEEE literature.\n• Implemented Shannon Entropy character distribution formula.\n• Formulated credential token dictionaries and regex rules.",
            "URL lexical structures, Shannon information entropy, token delimiters, regex pattern optimization, and phishing evasion tactics."
        ),
        (
            "4",
            "Darsh Hemantkumar Raut",
            "228",
            "12611013",
            "Lead Architecture & Machine Learning Pipeline:\n• Architected end-to-end multi-layer detection framework.\n• Trained and tuned Random Forest ML model (100% test score).\n• Engineered Brand Impersonation Hunter (Levenshtein + homoglyphs).\n• Integrated FastAPI asynchronous backend orchestration.",
            "Machine learning classification mechanics, Random Forest decision splits, explainable AI (XAI), string distance algorithms, and system architecture."
        ),
        (
            "5",
            "Darsh Jain",
            "229",
            "12611575",
            "Backend Architecture & Database Persistence Lead:\n• Developed FastAPI asynchronous REST microservices (/scan, /scan-batch).\n• Designed SQLite relational schema and transactional logging.\n• Conducted API performance benchmarking and unit test suites.",
            "Asynchronous ASGI concurrency, REST API design, database normalization, SQLite transaction locking, and backend benchmarking."
        )
    ]

    for row_idx, data in enumerate(team_data, start=1):
        for col_idx, text in enumerate(data):
            cell = tbl13.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_DARK if row_idx % 2 == 1 else COLOR_CARD_ALT
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_FAMILY
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_TEXT_WHITE
            if col_idx in [0, 2, 3]:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
                if col_idx == 0:
                    p.font.color.rgb = COLOR_NEON_CYAN
            elif col_idx == 1:
                p.font.bold = True

    # Bottom Future Scope & Academic Conclusion
    create_card(s13, Inches(0.6), Inches(5.4), Inches(12.133), Inches(1.6), accent_color=COLOR_NEON_GREEN)
    tb_bot = s13.shapes.add_textbox(Inches(0.8), Inches(5.48), Inches(11.733), Inches(1.4))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True

    p = tf_bot.paragraphs[0]
    p.text = "FUTURE SCOPE & ACADEMIC CONCLUSION"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NEON_GREEN

    concl_items = [
        "Phase 2 Scope (Final Semester): Live WHOIS/RDAP domain age integration, SSL/TLS certificate chain validation, Docker containerization, and Chrome Web Store distribution.",
        "Conclusion: AEGIS demonstrates that client-side machine learning combined with algorithmic homoglyph brand heuristics provides zero-latency, proactive defense against modern zero-day phishing attacks while educating users through transparent explainability."
    ]
    for ci in concl_items:
        p = tf_bot.add_paragraph()
        p.text = "▸ " + ci
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.space_before = Pt(3)

    # Save presentation with permission fallback if open in PowerPoint
    target_files = [
        output_path,
        output_path.replace(".pptx", "_HighTech.pptx"),
        output_path.replace(".pptx", "_V3.pptx")
    ]
    saved_file = None
    for target in target_files:
        try:
            prs.save(target)
            saved_file = target
            print(f"[SUCCESS] Presentation generated successfully with {len(prs.slides)} slides at: {target}")
            break
        except PermissionError:
            continue

    if not saved_file:
        fallback = os.path.join(os.path.dirname(output_path), "AEGIS_Midsem_Review_Final.pptx")
        prs.save(fallback)
        print(f"[SUCCESS] Saved as: {fallback}")

if __name__ == "__main__":
    out_dir = r"C:\Users\Darsh Raut\.gemini\antigravity\scratch\aegis"
    out_file = os.path.join(out_dir, "AEGIS_Midsem_Review.pptx")
    build_presentation(out_file)
