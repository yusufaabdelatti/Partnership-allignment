"""
Nursery Pre-Enrollment Assessment System
=========================================
Premium Streamlit app for collecting and scoring parenting-style assessments.
After submission:
  - Parent sees a clean thank-you screen only.
  - A structured PDF report is automatically emailed to the nursery director.

Dimensions scored: Trust, Control, Anxiety, Boundary Respect
"""

import streamlit as st
import os
import smtplib
import tempfile
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nursery Pre-Enrollment Assessment",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────
def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

    :root {
        --sage:      #5A7A5A;
        --sage-lt:   #E8F0E8;
        --sage-mid:  #C4D9C4;
        --cream:     #FAF8F5;
        --warm:      #F5F0E8;
        --charcoal:  #2D2D2D;
        --muted:     #6B7280;
        --border:    #E2DDD8;
        --radius:    14px;
        --shadow:    0 2px 16px rgba(0,0,0,0.07);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: var(--cream) !important;
        color: var(--charcoal) !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 780px !important;
    }

    /* Hero */
    .hero-title {
        font-family: 'DM Serif Display', serif !important;
        font-size: 2.4rem;
        color: var(--charcoal);
        text-align: center;
        margin: 0.25rem 0 0.5rem;
        line-height: 1.2;
    }
    .hero-sub {
        text-align: center;
        color: var(--muted);
        font-size: 1.05rem;
        font-weight: 300;
        max-width: 560px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }

    /* Divider */
    .divider { border: none; border-top: 1.5px solid var(--border); margin: 1.5rem 0; }

    /* Section label */
    .section-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--sage);
        margin-bottom: 0.4rem;
    }

    /* Demographic card */
    .demo-card {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.4rem 1.6rem 1.2rem;
        margin-bottom: 1.4rem;
        box-shadow: var(--shadow);
    }
    .demo-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.1rem;
        color: var(--charcoal);
        margin-bottom: 1rem;
    }

    /* Question card */
    .q-card {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.4rem 1.6rem 1rem;
        margin-bottom: 1.2rem;
        box-shadow: var(--shadow);
    }
    .q-number {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: var(--sage);
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .q-text {
        font-family: 'DM Serif Display', serif;
        font-size: 1.15rem;
        color: var(--charcoal);
        margin-bottom: 0.9rem;
        line-height: 1.45;
    }

    /* Progress */
    .progress-wrap {
        background: var(--sage-mid);
        border-radius: 99px;
        height: 6px;
        margin-bottom: 0.3rem;
        overflow: hidden;
    }
    .progress-fill {
        background: var(--sage);
        height: 100%;
        border-radius: 99px;
        transition: width 0.4s ease;
    }
    .progress-label {
        font-size: 0.8rem;
        color: var(--muted);
        text-align: right;
        margin-bottom: 1.6rem;
    }

    /* Inputs */
    .stTextInput input {
        border-radius: 10px !important;
        border-color: var(--border) !important;
        font-family: 'DM Sans', sans-serif !important;
        background: #fff !important;
    }
    .stTextArea textarea {
        border-radius: 10px !important;
        border-color: var(--border) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        background: #fff !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--sage) !important;
        box-shadow: 0 0 0 2px var(--sage-mid) !important;
    }

    /* Submit button */
    .stButton > button {
        background: var(--sage) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2.5rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #4A6A4A !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(90,122,90,0.3) !important;
    }

    /* Thank you */
    .thankyou-wrap {
        text-align: center;
        padding: 3.5rem 2rem;
        background: #fff;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    .thankyou-icon { font-size: 3.5rem; margin-bottom: 1rem; }
    .thankyou-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: var(--charcoal);
        margin-bottom: 0.75rem;
    }
    .thankyou-body {
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.65;
        max-width: 460px;
        margin: 0 auto;
    }

    /* Info note */
    .info-note {
        background: var(--sage-lt);
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.85rem;
        color: var(--sage);
        margin-bottom: 1rem;
    }
    .info-warn {
        background: #FAE0E0;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.85rem;
        color: #9B3A3A;
        margin-bottom: 1rem;
    }

    /* ── Ranking widget ───────────────────────────────────────────────────── */
    .rank-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 0.5rem;
    }
    .rank-item {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #fff;
        border: 1.5px solid var(--border);
        border-radius: 10px;
        padding: 10px 14px;
        cursor: grab;
        user-select: none;
        transition: box-shadow 0.15s, border-color 0.15s, transform 0.1s;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        color: var(--charcoal);
    }
    .rank-item:active { cursor: grabbing; }
    .rank-item.dragging {
        opacity: 0.5;
        border-color: var(--sage);
        box-shadow: 0 4px 18px rgba(90,122,90,0.22);
    }
    .rank-item.drag-over {
        border-color: var(--sage);
        background: var(--sage-lt);
        transform: scale(1.01);
    }
    .rank-badge {
        min-width: 26px;
        height: 26px;
        border-radius: 50%;
        background: var(--sage);
        color: #fff;
        font-weight: 700;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .rank-drag-hint {
        font-size: 0.75rem;
        color: var(--muted);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* ── Likert scale ─────────────────────────────────────────────────────── */
    .likert-wrap {
        display: flex;
        gap: 0;
        width: 100%;
        margin-top: 0.4rem;
        border-radius: 10px;
        overflow: hidden;
        border: 1.5px solid var(--border);
    }
    .likert-opt {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 12px 6px 10px;
        cursor: pointer;
        border-right: 1px solid var(--border);
        background: #fff;
        transition: background 0.15s;
        text-align: center;
        gap: 6px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.82rem;
        color: var(--muted);
        line-height: 1.3;
    }
    .likert-opt:last-child { border-right: none; }
    .likert-opt.selected {
        background: var(--sage-lt);
        color: var(--sage);
        font-weight: 600;
    }
    .likert-dot {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 2px solid var(--border);
        background: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: border-color 0.15s, background 0.15s;
    }
    .likert-opt.selected .likert-dot {
        border-color: var(--sage);
        background: var(--sage);
    }
    .likert-labels {
        display: flex;
        justify-content: space-between;
        margin-top: 5px;
        padding: 0 2px;
        font-size: 0.72rem;
        color: var(--muted);
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# QUESTION DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────
# Q2 uses type="ranking"; new Q_LIKERT uses type="likert"
# Each MC option carries scores for [trust, control, anxiety, boundary]  1–5

RANKING_OPTIONS_Q2 = [
    "Safety and emotional care",
    "Focus on measurable academic outcomes",
    "Build independence, social skills, and emotional regulation",
    "Follow the family's parenting style",
    "Encourage curiosity, creativity, and play-based learning",
]

LIKERT_OPTIONS = [
    "Very uncomfortable",
    "Uncomfortable",
    "Neutral",
    "Comfortable",
    "Very comfortable",
]

QUESTIONS = [
    {   # Q1
        "id": "q1", "type": "single", "section": "Child Transition",
        "text": "If your child cries daily during the first week of nursery, how would you respond?",
        "options": [
            {"label": "Request continuous updates throughout the day",
             "scores": {"trust": 2, "control": 1, "anxiety": 1, "boundary": 2}},
            {"label": "Drop in unexpectedly to check on them",
             "scores": {"trust": 1, "control": 1, "anxiety": 1, "boundary": 1}},
            {"label": "Follow a structured transition plan and stay committed",
             "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5}},
            {"label": "Consider pausing enrollment until they are ready",
             "scores": {"trust": 3, "control": 3, "anxiety": 2, "boundary": 3}},
        ],
    },
    {   # Q2 — RANKING
        "id": "q2", "type": "ranking", "section": "Role of Nursery",
        "text": "Please rank the following from most to least important to you in a nursery setting.",
        "options": RANKING_OPTIONS_Q2,
    },
    {   # Q3
        "id": "q3", "type": "single", "section": "Communication & Conflict",
        "text": "If you disagreed with a nursery decision, what would you most likely do?",
        "options": [
            {"label": "Expect the decision to be reconsidered immediately",
             "scores": {"trust": 1, "control": 1, "anxiety": 3, "boundary": 1}},
            {"label": "Assume the nursery will adjust without discussion",
             "scores": {"trust": 2, "control": 1, "anxiety": 3, "boundary": 2}},
            {"label": "Request a meeting to understand the reasoning",
             "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5}},
            {"label": "Escalate to management if I feel strongly",
             "scores": {"trust": 3, "control": 2, "anxiety": 3, "boundary": 3}},
        ],
    },
    {   # Q4
        "id": "q4", "type": "single", "section": "Update Expectations",
        "text": "How often would you expect updates from the nursery team?",
        "options": [
            {"label": "Several times throughout the day",
             "scores": {"trust": 1, "control": 1, "anxiety": 1, "boundary": 2}},
            {"label": "A daily summary at pickup",
             "scores": {"trust": 4, "control": 4, "anxiety": 4, "boundary": 4}},
            {"label": "Weekly structured progress updates",
             "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5}},
            {"label": "Only when something important happens",
             "scores": {"trust": 4, "control": 5, "anxiety": 5, "boundary": 5}},
        ],
    },
    {   # Q5
        "id": "q5", "type": "single", "section": "Child's Challenges",
        "text": "When your child faces a challenge at nursery, what response do you prefer from the team?",
        "options": [
            {"label": "Inform me first and wait for my direction",
             "scores": {"trust": 1, "control": 1, "anxiety": 2, "boundary": 1}},
            {"label": "Attempt to help and update me regularly",
             "scores": {"trust": 4, "control": 4, "anxiety": 4, "boundary": 4}},
            {"label": "Apply professional judgment and report in an organised way",
             "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5}},
            {"label": "Minimise reporting to avoid adding to my stress",
             "scores": {"trust": 2, "control": 3, "anxiety": 2, "boundary": 3}},
        ],
    },
    {   # Q6
        "id": "q6", "type": "single", "section": "Independence & Growth",
        "text": "How comfortable are you with your child experiencing temporary frustration as part of learning independence?",
        "options": [
            {"label": "Not comfortable — I prefer they are always immediately supported",
             "scores": {"trust": 2, "control": 1, "anxiety": 1, "boundary": 2}},
            {"label": "Slightly uncomfortable — I need regular reassurance",
             "scores": {"trust": 3, "control": 2, "anxiety": 2, "boundary": 3}},
            {"label": "Comfortable — I understand it is part of growth",
             "scores": {"trust": 5, "control": 4, "anxiety": 5, "boundary": 5}},
            {"label": "Very comfortable — I actively encourage resilience",
             "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5}},
        ],
    },
    {   # Q7 — Separation handling
        "id": "q7", "type": "single", "section": "Child Readiness",
        "text": "How does your child typically respond when separated from you in an unfamiliar setting?",
        "options": [
            {"label": "Becomes very distressed and takes a long time to settle",
             "scores": {"trust": 3, "control": 2, "anxiety": 1, "boundary": 3}},
            {"label": "Initially upset but settles within a reasonable time",
             "scores": {"trust": 4, "control": 4, "anxiety": 4, "boundary": 4}},
            {"label": "Explores independently with occasional check-ins",
             "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5}},
            {"label": "I have not had the opportunity to observe this yet",
             "scores": {"trust": 3, "control": 3, "anxiety": 3, "boundary": 3}},
        ],
    },
    {   # Q8 — Parental self-awareness at drop-off
        "id": "q8", "type": "single", "section": "Parental Self-Awareness",
        "text": "How would you describe your own emotional response during drop-off on difficult days?",
        "options": [
            {"label": "I find it very hard to leave and often linger or return to check",
             "scores": {"trust": 1, "control": 1, "anxiety": 1, "boundary": 1}},
            {"label": "I feel anxious but I commit to leaving and trust the team",
             "scores": {"trust": 4, "control": 4, "anxiety": 3, "boundary": 4}},
            {"label": "I feel confident in the environment and say goodbye calmly",
             "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5}},
            {"label": "I have not experienced a difficult drop-off yet",
             "scores": {"trust": 3, "control": 3, "anxiety": 4, "boundary": 3}},
        ],
    },
    {   # Q9 — NEW: Likert separation comfort
        "id": "q9_likert", "type": "likert", "section": "Separation Readiness",
        "text": "How comfortable are you with your child experiencing temporary distress (e.g., crying or resistance) as part of adapting to nursery separation?",
        "options": LIKERT_OPTIONS,
    },
    {   # Q10 — Short answer (was Q9)
        "id": "q9", "type": "text", "section": "Open Reflection",
        "text": "What is your biggest concern about starting nursery?",
        "placeholder": "Feel free to share openly — this helps us support your child better.",
    },
    {   # Q11 — Short answer (was Q10)
        "id": "q10", "type": "text", "section": "Open Reflection",
        "text": "How do you envision a successful partnership with the nursery team?",
        "placeholder": "There are no right or wrong answers — we value your perspective.",
    },
]

TOTAL_QUESTIONS = len(QUESTIONS)


# ─────────────────────────────────────────────────────────────────────────────
# KEYWORD SCORING
# ─────────────────────────────────────────────────────────────────────────────
ANXIETY_KEYWORDS  = ["worried","scared","fear","anxious","nervous","panic",
                     "unsafe","dangerous","dread","overwhelmed","stress"]
CONTROL_KEYWORDS  = ["control","in charge","my decision","i decide","my way",
                     "my rules","follow my","i know best"]
TRUST_NEGATIVE    = ["don't trust","not sure","uncertain","doubt","skeptical",
                     "can't be sure","how do i know"]
TRUST_POSITIVE    = ["trust","confident","comfortable","believe","faith",
                     "partnership","collaborate","together","open","excited"]
BOUNDARY_NEGATIVE = ["anytime","whenever i want","drop in","check any time",
                     "always available","call me immediately","at all times"]
BOUNDARY_POSITIVE = ["respect","professional","boundaries","structure",
                     "schedule","organised","routine","plan","framework"]


def keyword_adjustment(text: str) -> dict:
    if not text:
        return {"trust": 0, "control": 0, "anxiety": 0, "boundary": 0}
    t = text.lower()
    d = {"trust": 0, "control": 0, "anxiety": 0, "boundary": 0}
    for kw in ANXIETY_KEYWORDS:
        if kw in t:  d["anxiety"]  -= 1; break
    for kw in CONTROL_KEYWORDS:
        if kw in t:  d["control"]  -= 1; d["boundary"] -= 1; break
    for kw in TRUST_NEGATIVE:
        if kw in t:  d["trust"]    -= 1; break
    for kw in TRUST_POSITIVE:
        if kw in t:  d["trust"]    += 1; break
    for kw in BOUNDARY_NEGATIVE:
        if kw in t:  d["boundary"] -= 1; break
    for kw in BOUNDARY_POSITIVE:
        if kw in t:  d["boundary"] += 1; break
    return d


# ─────────────────────────────────────────────────────────────────────────────
# RANKING SCORE MAPPING
# Rank 1 (most important) → highest weight; rank 5 → lowest weight
# Option scores are indexed by their position in RANKING_OPTIONS_Q2
# ─────────────────────────────────────────────────────────────────────────────
# Per-option dimension scores (same structure as MC options)
RANKING_OPTION_SCORES = {
    "Safety and emotional care":
        {"trust": 4, "control": 3, "anxiety": 3, "boundary": 4},
    "Focus on measurable academic outcomes":
        {"trust": 2, "control": 2, "anxiety": 2, "boundary": 2},
    "Build independence, social skills, and emotional regulation":
        {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
    "Follow the family's parenting style":
        {"trust": 2, "control": 1, "anxiety": 2, "boundary": 1},
    "Encourage curiosity, creativity, and play-based learning":
        {"trust": 4, "control": 4, "anxiety": 4, "boundary": 4},
}

# Rank weights: rank 1 = 1.0, rank 2 = 0.75, rank 3 = 0.5, rank 4 = 0.3, rank 5 = 0.15
RANK_WEIGHTS = [1.0, 0.75, 0.5, 0.3, 0.15]

# Max contribution from Q2 (used in normalisation):
# best case: all 5s × sum(weights) = 5 × 2.7 = 13.5 → round to 14
Q2_MAX = 14.0


def score_ranking(ranked_list: list) -> dict:
    """Score a ranked list of option labels. Returns raw dimension scores."""
    totals = {"trust": 0.0, "control": 0.0, "anxiety": 0.0, "boundary": 0.0}
    for rank_idx, label in enumerate(ranked_list):
        w = RANK_WEIGHTS[rank_idx] if rank_idx < len(RANK_WEIGHTS) else 0.1
        opt_scores = RANKING_OPTION_SCORES.get(label, {})
        for dim, val in opt_scores.items():
            totals[dim] += val * w
    # Normalise to 0–5 range to match MC scoring granularity
    return {d: round(v / Q2_MAX * 5, 2) for d, v in totals.items()}


# ─────────────────────────────────────────────────────────────────────────────
# LIKERT SCORE MAPPING
# ─────────────────────────────────────────────────────────────────────────────
LIKERT_SCORES = {
    "Very uncomfortable":  {"trust": 1, "control": 1, "anxiety": 1, "boundary": 1},
    "Uncomfortable":       {"trust": 2, "control": 2, "anxiety": 2, "boundary": 2},
    "Neutral":             {"trust": 3, "control": 3, "anxiety": 3, "boundary": 3},
    "Comfortable":         {"trust": 4, "control": 4, "anxiety": 4, "boundary": 4},
    "Very comfortable":    {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
}


# ─────────────────────────────────────────────────────────────────────────────
# SCORING ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def compute_scores(answers: dict) -> dict:
    """Aggregate MC + ranking + likert + keyword scores."""
    totals = {"trust": 0.0, "control": 0.0, "anxiety": 0.0, "boundary": 0.0}

    for q in QUESTIONS:
        qid = q["id"]

        if q["type"] == "single":
            label = answers.get(qid)
            if label:
                for opt in q["options"]:
                    if opt["label"] == label:
                        for dim, val in opt["scores"].items():
                            totals[dim] += val

        elif q["type"] == "ranking":
            ranked = answers.get(qid)  # list of labels in ranked order
            if ranked and len(ranked) == len(q["options"]):
                for dim, val in score_ranking(ranked).items():
                    totals[dim] += val

        elif q["type"] == "likert":
            label = answers.get(qid)
            if label and label in LIKERT_SCORES:
                for dim, val in LIKERT_SCORES[label].items():
                    totals[dim] += val

    # Keyword adjustments on open text
    for qid in ["q9", "q10"]:
        for dim, delta in keyword_adjustment(answers.get(qid, "")).items():
            totals[dim] += delta

    # Max possible:
    #   MC: 8 questions × 5 = 40
    #   Ranking Q2 normalised to 5-equivalent per dimension → 5
    #   Likert: 5
    #   Keyword bonus: 2
    #   Total: 52
    max_possible = 52.0
    pct = {d: round(min(max(totals[d] / max_possible * 100, 0), 100)) for d in totals}
    return {"raw": {d: round(totals[d], 2) for d in totals}, "pct": pct}


def classify_risk(scores: dict) -> tuple:
    avg = sum(scores["pct"].values()) / len(scores["pct"])
    if avg >= 72:
        return "low",  "High Alignment — Low Risk"
    elif avg >= 48:
        return "mod",  "Moderate Risk — Monitor Closely"
    else:
        return "high", "High Risk — Director Review Recommended"


# ─────────────────────────────────────────────────────────────────────────────
# GROQ REPORT GENERATION
# ─────────────────────────────────────────────────────────────────────────────
def build_prompt(demographics: dict, answers: dict,
                 scores: dict, risk_label: str) -> str:
    mc_lines = []
    for q in QUESTIONS:
        if q["type"] == "single":
            mc_lines.append(
                f"- {q['text']}\n  Answer: {answers.get(q['id'], 'No answer')}"
            )
        elif q["type"] == "ranking":
            ranked = answers.get(q["id"], [])
            ranked_str = " → ".join(
                [f"#{i+1} {lbl}" for i, lbl in enumerate(ranked)]
            ) if ranked else "Not ranked"
            mc_lines.append(f"- {q['text']}\n  Ranking: {ranked_str}")
        elif q["type"] == "likert":
            mc_lines.append(
                f"- {q['text']}\n  Answer: {answers.get(q['id'], 'No answer')}"
            )

    pct = scores["pct"]
    child_age = (f"{demographics.get('child_age_years', 0)} years, "
                 f"{demographics.get('child_age_months', 0)} months")
    prior = "Yes — has prior nursery experience" if demographics.get("prior_nursery") \
            else "No — first nursery experience"

    return f"""You are a senior child development consultant preparing a confidential
pre-enrollment assessment report for a nursery director.

CHILD & FAMILY PROFILE:
- Parent Name:     {demographics.get('parent_name', 'Not provided')}
- Child Name:      {demographics.get('child_name', 'Not provided')}
- Child Age:       {child_age}
- Prior Nursery:   {prior}
- Date:            {datetime.now().strftime('%d %B %Y')}

DIMENSION SCORES (0–100, higher = better aligned):
- Trust in Professionals:  {pct['trust']}%
- Control Orientation:     {pct['control']}%
- Transition Comfort:      {pct['anxiety']}%
- Boundary Respect:        {pct['boundary']}%

OVERALL RISK: {risk_label}

ASSESSMENT ANSWERS:
{chr(10).join(mc_lines)}

OPEN RESPONSES:
- Biggest concern: {answers.get('q9', 'Not provided')}
- Vision of partnership: {answers.get('q10', 'Not provided')}

Write a professional, empathetic, actionable report for the nursery director.
Use EXACTLY these numbered section headings:

1. EXECUTIVE SUMMARY
2. PARENT PROFILE ANALYSIS
3. STRENGTHS & POSITIVE INDICATORS
4. RISK AREAS & CONCERNS
5. CHILD READINESS OBSERVATIONS
6. RECOMMENDED ONBOARDING APPROACH
7. SUGGESTED STAFF ACTIONS

Rules:
- Do NOT quote numeric scores — describe patterns qualitatively.
- Be specific to this family's actual answers, not generic.
- Tone: professional, empathetic, child-focused, non-judgmental.
- Length: 380–450 words total.
- Section 7 must be bullet points starting with •
"""


def generate_report(demographics: dict, answers: dict,
                    scores: dict, risk_label: str) -> str:
    try:
        from groq import Groq
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        resp = client.chat.completions.create(
            model="llama3-70b-8192",
            max_tokens=1000,
            temperature=0.45,
            messages=[
                {"role": "system",
                 "content": ("You are a specialist child development consultant. "
                             "Write concise, professional, empathetic reports for "
                             "nursery directors. Follow the exact structure requested.")},
                {"role": "user", "content": build_prompt(demographics, answers, scores, risk_label)},
            ],
        )
        return resp.choices[0].message.content
    except Exception:
        return _rule_based_report(demographics, answers, scores, risk_label)


def _rule_based_report(demographics, answers, scores, risk_label):
    pct  = scores["pct"]
    avg  = sum(pct.values()) / len(pct)
    parent = demographics.get("parent_name", "This parent")
    child  = demographics.get("child_name",  "the child")

    tl = "strong"  if pct["trust"]   >= 70 else ("moderate" if pct["trust"]   >= 45 else "limited")
    cl = "healthy" if pct["control"] >= 70 else ("some concern" if pct["control"] >= 45 else "elevated concern")
    al = "low"     if pct["anxiety"] >= 70 else ("moderate" if pct["anxiety"] >= 45 else "elevated")
    bl = "strong"  if pct["boundary"]>= 70 else ("developing" if pct["boundary"]>= 45 else "limited")

    pos, risks = [], []
    if pct["trust"]   >= 65: pos.append("Willingness to defer to professional expertise.")
    if pct["anxiety"] >= 65: pos.append("Emotional readiness for the child's transition.")
    if pct["boundary"]>= 65: pos.append("Respect for structured communication channels.")
    if pct["control"] >= 65: pos.append("Understands the nursery's independent professional role.")
    if not pos: pos.append("Expresses genuine care for their child's wellbeing.")

    if pct["trust"]   < 50: risks.append("May struggle to trust team decisions without direct involvement.")
    if pct["anxiety"] < 50: risks.append("Elevated parental anxiety may disrupt the child's settling.")
    if pct["control"] < 50: risks.append("Tendencies toward over-involvement may challenge boundaries.")
    if pct["boundary"]< 50: risks.append("May not readily respect communication structures or visit policies.")
    if not risks: risks.append("No significant concerns identified at this stage.")

    onboard = (
        "Standard transition plan is appropriate with daily pickup summaries in week one."
        if avg >= 72 else
        "An extended settling-in period is recommended with a dedicated key worker and proactive weekly check-ins."
        if avg >= 48 else
        "A pre-enrollment director meeting is strongly recommended before the child's first day "
        "to align expectations on communication, boundaries, and the nursery's professional approach."
    )

    # Describe ranking insight
    ranked = answers.get("q2", [])
    ranking_insight = ""
    if ranked:
        top = ranked[0] if len(ranked) > 0 else ""
        bottom = ranked[-1] if len(ranked) > 0 else ""
        ranking_insight = (
            f" Their nursery priorities place '{top}' first and '{bottom}' last, "
            "which offers insight into their expectations and values."
        )

    # Describe likert insight
    likert_val = answers.get("q9_likert", "")
    likert_insight = ""
    if likert_val:
        if likert_val in ["Very uncomfortable", "Uncomfortable"]:
            likert_insight = " The parent reports low comfort with temporary separation distress, suggesting a need for reassurance and a gradual transition plan."
        elif likert_val == "Neutral":
            likert_insight = " The parent reports a neutral stance toward separation distress, indicating openness to guidance on the transition process."
        else:
            likert_insight = " The parent reports comfort with temporary separation distress, reflecting healthy readiness for the child's independent nursery experience."

    lines = [
        "1. EXECUTIVE SUMMARY",
        f"{parent} presents with an overall risk classification of {risk_label}. Their profile "
        f"reflects {tl} trust in professionals, {al} transition anxiety, and {bl} boundary respect."
        f"{ranking_insight}{likert_insight}",
        "",
        "2. PARENT PROFILE ANALYSIS",
        f"This parent shows a {cl} control orientation and {al} comfort with {child}'s independent "
        f"nursery experience. Communication expectations appear "
        f"{'well calibrated' if pct['boundary'] >= 65 else 'worth clarifying at induction'}.",
        "",
        "3. STRENGTHS & POSITIVE INDICATORS",
        *[f"• {p}" for p in pos],
        "",
        "4. RISK AREAS & CONCERNS",
        *[f"• {r}" for r in risks],
        "",
        "5. CHILD READINESS OBSERVATIONS",
        f"Based on the described separation behaviour and age data, {child} "
        f"{'appears reasonably prepared for the transition' if avg >= 60 else 'may benefit from a gradual settling-in plan with close monitoring in the first weeks'}.",
        "",
        "6. RECOMMENDED ONBOARDING APPROACH",
        onboard,
        "",
        "7. SUGGESTED STAFF ACTIONS",
        "• Assign an experienced key worker and arrange a pre-enrollment introductory visit.",
        "• Share the nursery's communication policy clearly during induction.",
        f"• {'Provide a daily written summary during the first two weeks.' if avg < 65 else 'Offer standard daily verbal updates at pickup.'}",
        "• Flag to the director if drop-off behaviours become disruptive after week two.",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# PDF GENERATION  (reportlab)
# ─────────────────────────────────────────────────────────────────────────────
def build_pdf(demographics: dict, answers: dict,
              scores: dict, risk_label: str, report_text: str) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, HRFlowable, KeepTogether
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from io import BytesIO

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             leftMargin=2.2*cm, rightMargin=2.2*cm,
                             topMargin=2.5*cm, bottomMargin=2.5*cm)

    SAGE       = colors.HexColor("#5A7A5A")
    SAGE_LIGHT = colors.HexColor("#E8F0E8")
    CHARCOAL   = colors.HexColor("#2D2D2D")
    MUTED      = colors.HexColor("#6B7280")
    WARM       = colors.HexColor("#FAF8F5")
    WARM2      = colors.HexColor("#F0EDE8")
    BORDER     = colors.HexColor("#E2DDD8")
    RISK_PALETTE = {
        "low":  (colors.HexColor("#DCF0E3"), colors.HexColor("#3D7A4F")),
        "mod":  (colors.HexColor("#FFF1D6"), colors.HexColor("#B07D2B")),
        "high": (colors.HexColor("#FAE0E0"), colors.HexColor("#9B3A3A")),
    }

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    sTitle   = S("T",  fontName="Helvetica-Bold",    fontSize=18, textColor=CHARCOAL,
                       leading=24, alignment=TA_CENTER, spaceAfter=4)
    sSub     = S("Su", fontName="Helvetica",          fontSize=10, textColor=MUTED,
                       leading=14, alignment=TA_CENTER, spaceAfter=2)
    sSection = S("Se", fontName="Helvetica-Bold",     fontSize=10, textColor=SAGE,
                       leading=14, spaceBefore=12, spaceAfter=4)
    sBody    = S("Bo", fontName="Helvetica",           fontSize=9.5, textColor=CHARCOAL,
                       leading=14, spaceAfter=3)
    sBullet  = S("Bu", fontName="Helvetica",           fontSize=9.5, textColor=CHARCOAL,
                       leading=14, leftIndent=12, spaceAfter=2)
    sSmall   = S("Sm", fontName="Helvetica",           fontSize=8.5, textColor=MUTED,  leading=12)
    sFooter  = S("Fo", fontName="Helvetica-Oblique",   fontSize=7.5, textColor=MUTED,
                       alignment=TA_CENTER)

    def hr(c=SAGE, t=0.8):
        return HRFlowable(width="100%", thickness=t, color=c, spaceAfter=5, spaceBefore=5)
    def sp(h=0.25):
        return Spacer(1, h*cm)

    story = []

    # Title
    story += [
        Paragraph("🌱  Nursery Pre-Enrollment Assessment", sTitle),
        Paragraph("Confidential Staff Report — For Director Use Only", sSub),
        sp(0.3), hr(SAGE, 1.5), sp(0.2),
    ]

    # Demographics table
    child_age_str = (f"{demographics.get('child_age_years',0)} yr  "
                     f"{demographics.get('child_age_months',0)} mo")
    prior_str = ("Yes — has attended nursery before"
                 if demographics.get("prior_nursery")
                 else "No — first nursery experience")
    date_str = datetime.now().strftime("%d %b %Y, %H:%M")

    demo_rows = [
        [Paragraph("<b>Parent Name</b>", sSmall),
         Paragraph(demographics.get("parent_name","—"), sBody),
         Paragraph("<b>Date</b>",        sSmall),
         Paragraph(date_str,             sBody)],
        [Paragraph("<b>Child Name</b>",  sSmall),
         Paragraph(demographics.get("child_name","—"), sBody),
         Paragraph("<b>Child Age</b>",   sSmall),
         Paragraph(child_age_str,        sBody)],
        [Paragraph("<b>Prior Nursery</b>", sSmall),
         Paragraph(prior_str, sBody), "", ""],
    ]
    demo_tbl = Table(demo_rows, colWidths=[3.2*cm, 6.5*cm, 2.5*cm, 4.0*cm])
    demo_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,-1), SAGE_LIGHT),
        ("BACKGROUND",   (2,0),(2,-1), SAGE_LIGHT),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WARM, WARM2, WARM]),
        ("GRID",         (0,0),(-1,-1), 0.4, BORDER),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",  (0,0),(-1,-1), 7),
        ("SPAN",         (1,2),(3,2)),
    ]))
    story += [demo_tbl, sp(0.4)]

    # Risk badge
    risk_level, _ = classify_risk(scores)
    risk_bg, risk_fg = RISK_PALETTE.get(risk_level, RISK_PALETTE["mod"])
    risk_row = [[Paragraph(
        f"<b>  ●  {risk_label}  </b>",
        S("RP", fontName="Helvetica-Bold", fontSize=12,
          textColor=risk_fg, alignment=TA_CENTER)
    )]]
    risk_tbl = Table(risk_row, colWidths=[16.3*cm])
    risk_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), risk_bg),
        ("TOPPADDING",   (0,0),(-1,-1), 9),
        ("BOTTOMPADDING",(0,0),(-1,-1), 9),
    ]))
    story += [risk_tbl, sp(0.4)]

    # Dimension score bars
    story += [hr(), Paragraph("DIMENSION SCORES", sSection)]
    dim_meta = {
        "trust":    ("Trust in Professionals",
                     "Willingness to accept professional decisions without constant verification."),
        "control":  ("Control Orientation",
                     "Degree to which the parent expects direct influence over daily nursery activities."),
        "anxiety":  ("Transition Comfort",
                     "Emotional readiness and comfort with the child's independent nursery experience."),
        "boundary": ("Boundary Respect",
                     "Respect for communication structures, visit policies, and professional limits."),
    }
    for dim, (label, desc) in dim_meta.items():
        v        = scores["pct"][dim]
        filled   = max(v / 100 * 11.5, 0.15)
        empty    = 11.5 - filled
        ind      = "✓" if v >= 70 else ("!" if v >= 45 else "✗")
        ind_col  = (colors.HexColor("#3D7A4F") if v >= 70 else
                    (colors.HexColor("#B07D2B") if v >= 45 else colors.HexColor("#9B3A3A")))
        bar = Table(
            [[Paragraph(f"<b>{label}</b>",
               S("DL", fontName="Helvetica-Bold", fontSize=9, textColor=CHARCOAL)),
              "", "",
              Paragraph(f"<b>{v}%</b>",
               S("DV", fontName="Helvetica-Bold", fontSize=9, textColor=CHARCOAL)),
              Paragraph(f"<b>{ind}</b>",
               S("DI", fontName="Helvetica-Bold", fontSize=10, textColor=ind_col))]],
            colWidths=[4.3*cm, filled*cm, empty*cm, 1.2*cm, 0.8*cm]
        )
        bar.setStyle(TableStyle([
            ("BACKGROUND",   (1,0),(1,0), SAGE),
            ("BACKGROUND",   (2,0),(2,0), SAGE_LIGHT),
            ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
            ("TOPPADDING",   (0,0),(-1,-1), 4),
            ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ]))
        story.append(KeepTogether([bar, Paragraph(desc, sSmall), sp(0.15)]))

    # Assessment answers
    story += [sp(0.2), hr(), Paragraph("ASSESSMENT ANSWERS", sSection)]
    for q in QUESTIONS:
        if q["type"] == "single":
            story.append(Paragraph(f"<b>Q: {q['text']}</b>", sBody))
            story.append(Paragraph(f"→  {answers.get(q['id'], 'No answer')}", sBullet))
            story.append(sp(0.1))
        elif q["type"] == "ranking":
            story.append(Paragraph(f"<b>Q: {q['text']}</b>", sBody))
            ranked = answers.get(q["id"], [])
            for ri, rl in enumerate(ranked):
                story.append(Paragraph(f"#{ri+1}  {rl}", sBullet))
            story.append(sp(0.1))
        elif q["type"] == "likert":
            story.append(Paragraph(f"<b>Q: {q['text']}</b>", sBody))
            story.append(Paragraph(f"→  {answers.get(q['id'], 'No answer')}", sBullet))
            story.append(sp(0.1))

    # Open responses
    story += [hr(), Paragraph("OPEN RESPONSES", sSection)]
    story.append(Paragraph("<b>Biggest concern about starting nursery:</b>", sBody))
    story.append(Paragraph(answers.get("q9","Not provided"), sBullet))
    story += [sp(0.2)]
    story.append(Paragraph("<b>Vision of a successful partnership:</b>", sBody))
    story.append(Paragraph(answers.get("q10","Not provided"), sBullet))

    # Narrative report
    story += [hr(), Paragraph("PROFESSIONAL ASSESSMENT NARRATIVE", sSection)]
    for line in report_text.split("\n"):
        line = line.strip()
        if not line:
            story.append(sp(0.12))
        elif len(line) > 1 and line[0].isdigit() and line[1] in ".":
            story.append(Paragraph(f"<b>{line}</b>",
                S("NH", fontName="Helvetica-Bold", fontSize=10,
                  textColor=SAGE, spaceBefore=8, spaceAfter=2)))
        elif line.startswith("•"):
            story.append(Paragraph(line, sBullet))
        else:
            story.append(Paragraph(line, sBody))

    # Footer
    story += [sp(0.4), hr(MUTED, 0.4),
              Paragraph(
                  f"Auto-generated by the Nursery Pre-Enrollment Assessment System  •  "
                  f"{datetime.now().strftime('%d %B %Y, %H:%M')}  •  Confidential — Staff Use Only",
                  sFooter)]

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────────────────────────────────────
def send_report_email(pdf_bytes: bytes, demographics: dict,
                      risk_label: str) -> bool:
    try:
        sender   = st.secrets["EMAIL_ADDRESS"]
        password = st.secrets["EMAIL_APP_PASSWORD"]
        receiver = st.secrets["EMAIL_ADDRESS"]

        parent  = demographics.get("parent_name", "Unknown Parent")
        child   = demographics.get("child_name",  "Unknown Child")
        ds      = datetime.now().strftime("%d %B %Y")

        msg             = MIMEMultipart()
        msg["From"]     = sender
        msg["To"]       = receiver
        msg["Subject"]  = (
            f"[Enrollment Assessment] {parent} — {child}  |  "
            f"{risk_label}  |  {ds}"
        )

        body = f"""Dear Director,

A new pre-enrollment family assessment has been submitted. Please find the full PDF report attached.

QUICK SUMMARY
─────────────────────────────────────
Parent:              {parent}
Child:               {child}
Child Age:           {demographics.get('child_age_years',0)} yr  {demographics.get('child_age_months',0)} mo
Prior Nursery:       {"Yes" if demographics.get("prior_nursery") else "No"}
Submission Date:     {ds}
Risk Classification: {risk_label}
─────────────────────────────────────

Please review the attached PDF at your earliest convenience.

This message was generated automatically by the Nursery Pre-Enrollment Assessment System.
"""
        msg.attach(MIMEText(body, "plain"))

        filename = (
            f"Assessment_{parent.replace(' ','_')}_"
            f"{child.replace(' ','_')}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )
        part = MIMEBase("application", "octet-stream")
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())

        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def render_header():
    if os.path.exists("logo.png"):
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image("logo.png", use_container_width=True)
    else:
        st.markdown('<div style="text-align:center;font-size:3.5rem;margin-bottom:0.2rem;">🌱</div>',
                    unsafe_allow_html=True)
    st.markdown(
        """
        <h1 class="hero-title">Family Enrollment Reflection</h1>
        <p class="hero-sub">
            This short reflection helps our team understand your family's values
            and expectations — so we can ensure the warmest, most tailored welcome
            for your child.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="divider">', unsafe_allow_html=True)


def render_progress(answered: int, total: int):
    pct = int((answered / total) * 100)
    st.markdown(
        f"""
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{pct}%"></div>
        </div>
        <div class="progress-label">Question {answered} of {total} answered</div>
        """,
        unsafe_allow_html=True,
    )


def render_demographics(demo: dict) -> dict:
    st.markdown('<div class="section-label">About Your Family</div>', unsafe_allow_html=True)
    st.markdown('<div class="demo-card"><div class="demo-title">Please tell us a little about your family</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        parent_name = st.text_input("Parent / Guardian Full Name *",
                                    value=demo.get("parent_name",""),
                                    placeholder="e.g. Sarah Ahmed",
                                    key="dp_name")
    with c2:
        child_name  = st.text_input("Child's Full Name *",
                                    value=demo.get("child_name",""),
                                    placeholder="e.g. Liam",
                                    key="dc_name")

    c3, c4, c5 = st.columns([2, 2, 3])
    with c3:
        age_years  = st.number_input("Child's Age — Years",
                                     min_value=0, max_value=5,
                                     value=demo.get("child_age_years", 0),
                                     step=1, key="da_years")
    with c4:
        age_months = st.selectbox("Months",
                                  options=list(range(0, 12)),
                                  index=demo.get("child_age_months", 0),
                                  key="da_months")
    with c5:
        prior_opts  = ["No — this is their first nursery",
                       "Yes — they have attended before"]
        prior_idx   = 1 if demo.get("prior_nursery") else 0
        prior_raw   = st.selectbox("Has your child attended nursery before? *",
                                   options=prior_opts,
                                   index=prior_idx, key="dp_prior")

    st.markdown('</div>', unsafe_allow_html=True)

    return {
        "parent_name":      parent_name.strip(),
        "child_name":       child_name.strip(),
        "child_age_years":  int(age_years),
        "child_age_months": int(age_months),
        "prior_nursery":    prior_raw.startswith("Yes"),
    }


def render_ranking_question(q: dict, q_num: int, answers: dict):
    """
    Render Q2 ranking question.
    Uses numbered selectboxes as a clean, reliable ranking interface.
    """
    st.markdown(
        f"""
        <div class="q-card">
            <div class="q-number">Question {q_num} &nbsp;·&nbsp; {q["section"]}</div>
            <div class="q-text">{q["text"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = q["options"]
    n = len(options)
    key_prefix = f"rank_{q['id']}"

    # Initialise ranking state: list of n None values
    state_key = f"{key_prefix}_order"
    if state_key not in st.session_state:
        st.session_state[state_key] = [None] * n

    st.markdown(
        '<div class="rank-drag-hint">🔢  Assign each priority a rank — 1 = most important, '
        f'{n} = least important. Each rank must be used exactly once.</div>',
        unsafe_allow_html=True,
    )

    current_order = list(st.session_state[state_key])

    # Build selectboxes — one per option
    new_order = list(current_order)
    for i, opt in enumerate(options):
        col_label, col_select = st.columns([5, 2])
        with col_label:
            rank_val = current_order[i]
            badge_html = (
                f'<span style="display:inline-flex;align-items:center;justify-content:center;'
                f'width:24px;height:24px;border-radius:50%;background:#5A7A5A;color:#fff;'
                f'font-weight:700;font-size:0.78rem;margin-right:8px;">{rank_val}</span>'
                if rank_val else
                '<span style="display:inline-flex;align-items:center;justify-content:center;'
                'width:24px;height:24px;border-radius:50%;background:#E2DDD8;color:#6B7280;'
                'font-weight:700;font-size:0.78rem;margin-right:8px;">—</span>'
            )
            st.markdown(
                f'<div style="display:flex;align-items:center;padding:10px 0 10px 4px;'
                f'font-family:\'DM Sans\',sans-serif;font-size:0.95rem;color:#2D2D2D;">'
                f'{badge_html}{opt}</div>',
                unsafe_allow_html=True,
            )
        with col_select:
            rank_choices = ["—"] + [str(r) for r in range(1, n + 1)]
            current_val = str(current_order[i]) if current_order[i] is not None else "—"
            sel = st.selectbox(
                f"Rank for option {i+1}",
                options=rank_choices,
                index=rank_choices.index(current_val) if current_val in rank_choices else 0,
                key=f"{key_prefix}_sel_{i}",
                label_visibility="collapsed",
            )
            new_order[i] = int(sel) if sel != "—" else None

    st.session_state[state_key] = new_order

    # Validate uniqueness (no duplicate ranks)
    assigned = [r for r in new_order if r is not None]
    has_duplicates = len(assigned) != len(set(assigned))
    all_assigned = len(assigned) == n

    if has_duplicates:
        st.markdown(
            '<div class="info-warn">⚠  Some ranks are assigned more than once — '
            'each rank must be used exactly once.</div>',
            unsafe_allow_html=True,
        )
        return None  # not valid yet

    if all_assigned and not has_duplicates:
        # Build ordered list of labels by their assigned rank
        ranked_pairs = sorted(zip(new_order, options))
        ranked_labels = [lbl for _, lbl in ranked_pairs]
        return ranked_labels

    return None  # incomplete


def render_likert_question(q: dict, q_num: int, answers: dict):
    """Render a horizontal Likert scale using Streamlit radio with custom styling."""
    st.markdown(
        f"""
        <div class="q-card">
            <div class="q-number">Question {q_num} &nbsp;·&nbsp; {q["section"]}</div>
            <div class="q-text">{q["text"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    opts = q["options"]
    cur  = answers.get(q["id"])
    idx  = opts.index(cur) if cur in opts else None

    # Horizontal radio via columns
    cols = st.columns(len(opts))
    selected = None
    for ci, (col, opt) in enumerate(zip(cols, opts)):
        with col:
            is_sel = (cur == opt)
            btn_style = (
                "background:#E8F0E8;border:2px solid #5A7A5A;color:#5A7A5A;font-weight:600;"
                if is_sel else
                "background:#fff;border:1.5px solid #E2DDD8;color:#6B7280;"
            )
            if st.button(
                opt,
                key=f"likert_{q['id']}_{ci}",
                use_container_width=True,
                help=None,
            ):
                selected = opt

    # Endpoint labels
    st.markdown(
        f'<div class="likert-labels">'
        f'<span>← {opts[0]}</span>'
        f'<span>{opts[-1]} →</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if selected:
        return selected
    return cur  # return previously stored value if no new click


def render_question_card(q: dict, q_num: int, answers: dict):
    if q["type"] == "ranking":
        return render_ranking_question(q, q_num, answers)
    elif q["type"] == "likert":
        return render_likert_question(q, q_num, answers)

    # Standard single / text
    st.markdown(
        f"""
        <div class="q-card">
            <div class="q-number">Question {q_num} &nbsp;·&nbsp; {q["section"]}</div>
            <div class="q-text">{q["text"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if q["type"] == "single":
        opts = [o["label"] for o in q["options"]]
        cur  = answers.get(q["id"])
        idx  = opts.index(cur) if cur in opts else None
        return st.radio(f"_q{q['id']}_", opts, index=idx,
                        key=f"r_{q['id']}", label_visibility="collapsed")
    elif q["type"] == "text":
        return st.text_area(f"_q{q['id']}_",
                            value=answers.get(q["id"],""),
                            placeholder=q.get("placeholder",""),
                            key=f"t_{q['id']}", label_visibility="collapsed",
                            height=110)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    inject_styles()

    for k, v in {"submitted": False, "answers": {},
                 "demographics": {}, "scores": None,
                 "access_granted": False}.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ── ACCESS CODE GATE ──────────────────────────────────────────────────────
    if not st.session_state.access_granted:
        if os.path.exists("logo.png"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2: st.image("logo.png", use_container_width=True)
        st.markdown("""
        <h1 class="hero-title">Family Enrollment Reflection</h1>
        <p class="hero-sub">Please enter the access code provided by the nursery team.</p>
        """, unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            code = st.text_input("Access code", type="password",
                                 placeholder="Enter access code",
                                 label_visibility="collapsed")
            if st.button("Enter", use_container_width=True):
                valid_codes = [c.strip() for c in st.secrets.get("ACCESS_CODE", "").split(",")]
                if code.strip() in valid_codes:
                    st.session_state.access_granted = True
                    st.rerun()
                else:
                    st.markdown("""<div class="info-warn">
                        ⚠ Incorrect access code. Please check with the nursery team and try again.
                    </div>""", unsafe_allow_html=True)
        return

    # ── THANK-YOU SCREEN ──────────────────────────────────────────────────────
    if st.session_state.submitted:
        if os.path.exists("logo.png"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.image("logo.png", use_container_width=True)
        else:
            st.markdown('<div style="text-align:center;font-size:3.5rem;">🌱</div>',
                        unsafe_allow_html=True)

        child = st.session_state.demographics.get("child_name", "your child")
        st.markdown(
            f"""
            <div class="thankyou-wrap">
                <div class="thankyou-icon">🌿</div>
                <div class="thankyou-title">Thank You for Sharing</div>
                <div class="thankyou-body">
                    We have received your responses and our team will review them
                    carefully before <b>{child}</b>'s enrollment.<br><br>
                    A member of our team will be in touch shortly to discuss
                    next steps and answer any questions you may have.<br><br>
                    We look forward to welcoming your family into our community.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── FORM ──────────────────────────────────────────────────────────────────
    render_header()

    st.markdown(
        '<div class="info-note">ℹ  This reflection takes approximately 4–6 minutes. '
        'All responses are handled with complete confidentiality.</div>',
        unsafe_allow_html=True,
    )

    st.session_state.demographics = render_demographics(st.session_state.demographics)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Progress counting
    answered_mc   = sum(1 for q in QUESTIONS
                        if q["type"] == "single" and st.session_state.answers.get(q["id"]))
    answered_text = sum(1 for q in QUESTIONS
                        if q["type"] == "text" and st.session_state.answers.get(q["id"],"").strip())
    answered_rank = sum(1 for q in QUESTIONS
                        if q["type"] == "ranking" and
                        isinstance(st.session_state.answers.get(q["id"]), list) and
                        len(st.session_state.answers[q["id"]]) == len(q["options"]))
    answered_likert = sum(1 for q in QUESTIONS
                          if q["type"] == "likert" and st.session_state.answers.get(q["id"]))

    render_progress(answered_mc + answered_text + answered_rank + answered_likert, TOTAL_QUESTIONS)

    # Questions
    cur_section = None
    for i, q in enumerate(QUESTIONS, 1):
        if q["section"] != cur_section:
            cur_section = q["section"]
            st.markdown(f'<div class="section-label">{cur_section}</div>',
                        unsafe_allow_html=True)
        ans = render_question_card(q, i, st.session_state.answers)
        if ans is not None:
            st.session_state.answers[q["id"]] = ans
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Validation
    demo           = st.session_state.demographics
    missing_demo   = not demo.get("parent_name") or not demo.get("child_name")
    unanswered_mc  = [q for q in QUESTIONS
                      if q["type"] == "single" and not st.session_state.answers.get(q["id"])]
    unanswered_rank = [q for q in QUESTIONS
                       if q["type"] == "ranking" and (
                           not isinstance(st.session_state.answers.get(q["id"]), list) or
                           len(st.session_state.answers.get(q["id"], [])) != len(q["options"])
                       )]
    unanswered_likert = [q for q in QUESTIONS
                         if q["type"] == "likert" and not st.session_state.answers.get(q["id"])]

    all_unanswered = unanswered_mc + unanswered_rank + unanswered_likert

    if missing_demo:
        st.markdown('<div class="info-warn">⚠  Please enter the parent name and child name before submitting.</div>',
                    unsafe_allow_html=True)
    elif all_unanswered:
        st.markdown(
            f'<div class="info-warn">⚠  Please complete all {len(all_unanswered)} remaining '
            f'question(s) before submitting.</div>',
            unsafe_allow_html=True,
        )

    submitted = st.button("Submit Reflection →",
                           disabled=(missing_demo or bool(all_unanswered)),
                           key="submit_btn")

    if submitted and not missing_demo and not all_unanswered:
        with st.spinner("Submitting your responses…"):
            scores      = compute_scores(st.session_state.answers)
            _, risk_lbl = classify_risk(scores)
            report_text = generate_report(demo, st.session_state.answers, scores, risk_lbl)
            pdf_bytes   = build_pdf(demo, st.session_state.answers, scores, risk_lbl, report_text)
            send_report_email(pdf_bytes, demo, risk_lbl)

        st.session_state.scores    = scores
        st.session_state.submitted = True
        st.rerun()


if __name__ == "__main__":
    main()
