"""
Nursery Pre-Enrollment Assessment System
=========================================
A premium Streamlit application for collecting and scoring parenting style
assessments to help nursery staff identify alignment before enrollment.

Dimensions scored: Trust, Control, Anxiety, Boundary Respect
"""

import streamlit as st
import json
import re
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
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

    /* ── Root tokens ── */
    :root {
        --sage:     #5A7A5A;
        --sage-lt:  #E8F0E8;
        --sage-mid: #C4D9C4;
        --cream:    #FAF8F5;
        --warm:     #F5F0E8;
        --charcoal: #2D2D2D;
        --muted:    #6B7280;
        --border:   #E2DDD8;
        --risk-low:    #3D7A4F;
        --risk-mid:    #B07D2B;
        --risk-high:   #9B3A3A;
        --radius:   14px;
        --shadow:   0 2px 16px rgba(0,0,0,0.07);
    }

    /* ── Base resets ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        background-color: var(--cream) !important;
        color: var(--charcoal) !important;
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 780px !important;
    }

    /* ── Logo area ── */
    .logo-wrap {
        display: flex;
        justify-content: center;
        margin-bottom: 0.5rem;
    }

    /* ── Hero header ── */
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

    /* ── Divider ── */
    .divider {
        border: none;
        border-top: 1.5px solid var(--border);
        margin: 1.5rem 0;
    }

    /* ── Section label ── */
    .section-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--sage);
        margin-bottom: 0.4rem;
    }

    /* ── Question card ── */
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

    /* ── Progress bar ── */
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

    /* ── Radio / checkbox overrides ── */
    .stRadio > label, .stCheckbox > label {
        font-size: 0.96rem !important;
    }
    .stRadio [data-testid="stMarkdownContainer"] p,
    .stCheckbox [data-testid="stMarkdownContainer"] p {
        font-size: 0.96rem !important;
    }

    /* ── Text area ── */
    .stTextArea textarea {
        border-radius: 10px !important;
        border-color: var(--border) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        background: #fff !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--sage) !important;
        box-shadow: 0 0 0 2px var(--sage-mid) !important;
    }

    /* ── Submit button ── */
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
        cursor: pointer !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #4A6A4A !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(90,122,90,0.3) !important;
    }

    /* ── Thank you screen ── */
    .thankyou-wrap {
        text-align: center;
        padding: 3rem 2rem;
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
        max-width: 440px;
        margin: 0 auto;
    }

    /* ── Admin panel ── */
    .admin-header {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: var(--charcoal);
        margin-bottom: 0.25rem;
    }
    .admin-meta {
        font-size: 0.85rem;
        color: var(--muted);
        margin-bottom: 1.5rem;
    }

    /* ── Score bar ── */
    .score-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.85rem;
    }
    .score-dim {
        font-weight: 600;
        font-size: 0.9rem;
        width: 140px;
        flex-shrink: 0;
    }
    .score-bar-bg {
        flex: 1;
        background: var(--sage-lt);
        border-radius: 99px;
        height: 10px;
        overflow: hidden;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 99px;
    }
    .score-val {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--charcoal);
        width: 36px;
        text-align: right;
        flex-shrink: 0;
    }

    /* ── Risk badge ── */
    .risk-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 99px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.03em;
        margin-bottom: 1rem;
    }
    .risk-low  { background: #DCF0E3; color: var(--risk-low); }
    .risk-mod  { background: #FFF1D6; color: var(--risk-mid); }
    .risk-high { background: #FAE0E0; color: var(--risk-high); }

    /* ── Report block ── */
    .report-block {
        background: var(--warm);
        border-left: 4px solid var(--sage);
        border-radius: 0 10px 10px 0;
        padding: 1.2rem 1.4rem;
        margin-top: 1rem;
        font-size: 0.96rem;
        line-height: 1.7;
        color: var(--charcoal);
    }

    /* ── Dimension detail card ── */
    .dim-card {
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
    }
    .dim-card-title {
        font-weight: 600;
        font-size: 0.92rem;
        color: var(--charcoal);
        margin-bottom: 0.3rem;
    }
    .dim-card-body {
        font-size: 0.88rem;
        color: var(--muted);
        line-height: 1.6;
    }

    /* ── Export area ── */
    .stDownloadButton > button {
        background: transparent !important;
        border: 2px solid var(--sage) !important;
        color: var(--sage) !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.2s !important;
    }
    .stDownloadButton > button:hover {
        background: var(--sage-lt) !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: var(--charcoal) !important;
        background: var(--warm) !important;
        border-radius: 10px !important;
    }

    /* ── Tooltip / info ── */
    .info-note {
        background: var(--sage-lt);
        border-radius: 8px;
        padding: 0.7rem 1rem;
        font-size: 0.85rem;
        color: var(--sage);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# QUESTION DEFINITIONS
# Each option carries scores for [Trust, Control, Anxiety, BoundaryRespect]
# Scale: 1 (concerning) → 5 (aligned)
# ─────────────────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": "q1",
        "type": "single",
        "section": "Child Transition",
        "text": "If your child cries daily during the first week of nursery, how would you respond?",
        "options": [
            {
                "label": "Request continuous updates throughout the day",
                "scores": {"trust": 2, "control": 1, "anxiety": 1, "boundary": 2},
            },
            {
                "label": "Drop in unexpectedly to check on them",
                "scores": {"trust": 1, "control": 1, "anxiety": 1, "boundary": 1},
            },
            {
                "label": "Follow a structured transition plan and stay committed",
                "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
            },
            {
                "label": "Consider pausing enrollment until they're ready",
                "scores": {"trust": 3, "control": 3, "anxiety": 2, "boundary": 3},
            },
        ],
    },
    {
        "id": "q2",
        "type": "single",
        "section": "Role of Nursery",
        "text": "In your view, what is the primary role of a nursery?",
        "options": [
            {
                "label": "Safety and emotional care above all",
                "scores": {"trust": 4, "control": 3, "anxiety": 3, "boundary": 4},
            },
            {
                "label": "Achieving measurable academic milestones",
                "scores": {"trust": 3, "control": 2, "anxiety": 3, "boundary": 2},
            },
            {
                "label": "Building independence, social skills, and emotional regulation",
                "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
            },
            {
                "label": "Extending and reflecting the family's parenting style",
                "scores": {"trust": 2, "control": 1, "anxiety": 3, "boundary": 2},
            },
        ],
    },
    {
        "id": "q3",
        "type": "single",
        "section": "Communication & Conflict",
        "text": "If you disagreed with a nursery decision, what would you most likely do?",
        "options": [
            {
                "label": "Expect the decision to be reconsidered immediately",
                "scores": {"trust": 1, "control": 1, "anxiety": 3, "boundary": 1},
            },
            {
                "label": "Assume the nursery will adjust without discussion",
                "scores": {"trust": 2, "control": 1, "anxiety": 3, "boundary": 2},
            },
            {
                "label": "Request a meeting to understand the reasoning",
                "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
            },
            {
                "label": "Escalate to management if I feel strongly",
                "scores": {"trust": 3, "control": 2, "anxiety": 3, "boundary": 3},
            },
        ],
    },
    {
        "id": "q4",
        "type": "single",
        "section": "Update Expectations",
        "text": "How often would you expect updates from the nursery team?",
        "options": [
            {
                "label": "Several times throughout the day",
                "scores": {"trust": 1, "control": 1, "anxiety": 1, "boundary": 2},
            },
            {
                "label": "A daily summary at pickup",
                "scores": {"trust": 4, "control": 4, "anxiety": 4, "boundary": 4},
            },
            {
                "label": "Weekly structured progress updates",
                "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
            },
            {
                "label": "Only when something important happens",
                "scores": {"trust": 4, "control": 5, "anxiety": 5, "boundary": 5},
            },
        ],
    },
    {
        "id": "q5",
        "type": "single",
        "section": "Child's Challenges",
        "text": "When your child faces a challenge at nursery, what response do you prefer from the team?",
        "options": [
            {
                "label": "Inform me first and wait for my direction",
                "scores": {"trust": 1, "control": 1, "anxiety": 2, "boundary": 1},
            },
            {
                "label": "Attempt to help and update me regularly",
                "scores": {"trust": 4, "control": 4, "anxiety": 4, "boundary": 4},
            },
            {
                "label": "Apply professional judgment and report in an organized way",
                "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
            },
            {
                "label": "Minimize reporting to avoid adding to my stress",
                "scores": {"trust": 2, "control": 3, "anxiety": 2, "boundary": 3},
            },
        ],
    },
    {
        "id": "q6",
        "type": "single",
        "section": "Independence & Growth",
        "text": "How comfortable are you with your child experiencing temporary frustration as part of learning independence?",
        "options": [
            {
                "label": "Not comfortable — I prefer they're always supported",
                "scores": {"trust": 2, "control": 1, "anxiety": 1, "boundary": 2},
            },
            {
                "label": "Slightly uncomfortable — I need to be reassured",
                "scores": {"trust": 3, "control": 2, "anxiety": 2, "boundary": 3},
            },
            {
                "label": "Comfortable — I understand it's part of growth",
                "scores": {"trust": 5, "control": 4, "anxiety": 5, "boundary": 5},
            },
            {
                "label": "Very comfortable — I actively encourage resilience",
                "scores": {"trust": 5, "control": 5, "anxiety": 5, "boundary": 5},
            },
        ],
    },
    {
        "id": "q7",
        "type": "text",
        "section": "Open Reflection",
        "text": "What is your biggest concern about starting nursery?",
        "placeholder": "Feel free to share openly — this helps us support your child better.",
    },
    {
        "id": "q8",
        "type": "text",
        "section": "Open Reflection",
        "text": "How do you envision a successful partnership with the nursery team?",
        "placeholder": "There are no right or wrong answers — we value your perspective.",
    },
]

TOTAL_QUESTIONS = len(QUESTIONS)

# ─────────────────────────────────────────────────────────────────────────────
# KEYWORD SCORING — subtle adjustments from short-answer responses
# ─────────────────────────────────────────────────────────────────────────────
ANXIETY_KEYWORDS     = ["worried", "scared", "fear", "anxious", "nervous", "panic", "unsafe", "dangerous", "terrible", "hate", "dread"]
CONTROL_KEYWORDS     = ["control", "in charge", "my decision", "i decide", "my way", "my rules", "follow my", "i know best"]
TRUST_NEGATIVE       = ["don't trust", "not sure", "uncertain", "doubt", "skeptical", "can't be sure", "how do i know"]
TRUST_POSITIVE       = ["trust", "confident", "comfortable", "believe", "faith", "partnership", "collaborate", "together", "open"]
BOUNDARY_NEGATIVE    = ["anytime", "whenever i want", "drop in", "check any time", "always available", "call me immediately"]
BOUNDARY_POSITIVE    = ["respect", "professional", "boundaries", "structure", "schedule", "organized", "routine", "plan"]


def keyword_adjustment(text: str) -> dict:
    """
    Analyse short-answer text and return score adjustments.
    Returns a dict with deltas for each dimension (-1, 0, +1 only).
    """
    if not text:
        return {"trust": 0, "control": 0, "anxiety": 0, "boundary": 0}

    t = text.lower()
    delta = {"trust": 0, "control": 0, "anxiety": 0, "boundary": 0}

    for kw in ANXIETY_KEYWORDS:
        if kw in t:
            delta["anxiety"] -= 1
            break
    for kw in CONTROL_KEYWORDS:
        if kw in t:
            delta["control"] -= 1
            delta["boundary"] -= 1
            break
    for kw in TRUST_NEGATIVE:
        if kw in t:
            delta["trust"] -= 1
            break
    for kw in TRUST_POSITIVE:
        if kw in t:
            delta["trust"] += 1
            break
    for kw in BOUNDARY_NEGATIVE:
        if kw in t:
            delta["boundary"] -= 1
            break
    for kw in BOUNDARY_POSITIVE:
        if kw in t:
            delta["boundary"] += 1
            break

    return delta


# ─────────────────────────────────────────────────────────────────────────────
# SCORING ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def compute_scores(answers: dict) -> dict:
    """
    Aggregate all MC scores + keyword adjustments into per-dimension totals.
    Returns raw totals and normalised percentages (0–100).
    """
    totals = {"trust": 0, "control": 0, "anxiety": 0, "boundary": 0}
    mc_counts = {"trust": 0, "control": 0, "anxiety": 0, "boundary": 0}

    # MC / radio questions (q1–q6)
    for q in QUESTIONS:
        if q["type"] == "single":
            answer_label = answers.get(q["id"])
            if answer_label:
                for opt in q["options"]:
                    if opt["label"] == answer_label:
                        for dim, val in opt["scores"].items():
                            totals[dim] += val
                            mc_counts[dim] += 1

    # Keyword adjustments from q7 & q8
    for qid in ["q7", "q8"]:
        text = answers.get(qid, "")
        delta = keyword_adjustment(text)
        for dim in totals:
            totals[dim] += delta[dim]

    # Max possible per dimension = 6 questions × 5 = 30, plus up to +2 keyword bonus
    max_possible = 32
    percentages = {
        dim: round(min(max(totals[dim] / max_possible * 100, 0), 100))
        for dim in totals
    }

    return {"raw": totals, "pct": percentages}


def classify_risk(scores: dict) -> tuple:
    """
    Returns (risk_level, label, badge_class) based on average alignment score.
    """
    avg = sum(scores["pct"].values()) / len(scores["pct"])

    if avg >= 72:
        return "low", "High Alignment — Low Risk", "risk-low"
    elif avg >= 48:
        return "mod", "Moderate Risk", "risk-mod"
    else:
        return "high", "High Risk — Needs Attention", "risk-high"


# ─────────────────────────────────────────────────────────────────────────────
# REPORT GENERATOR  (uses Anthropic API via st.secrets)
# ─────────────────────────────────────────────────────────────────────────────
def build_prompt(answers: dict, scores: dict, risk_label: str) -> str:
    """Construct the admin report prompt."""
    mc_summary = []
    for q in QUESTIONS:
        if q["type"] == "single":
            mc_summary.append(f"- {q['text']}: {answers.get(q['id'], 'No answer')}")

    text_q7 = answers.get("q7", "No answer provided")
    text_q8 = answers.get("q8", "No answer provided")

    pct = scores["pct"]

    return f"""You are a specialist child development consultant reviewing a nursery pre-enrollment parenting assessment.

ASSESSMENT DATA:
Dimension Scores (0–100 scale):
- Trust in Professionals: {pct['trust']}
- Control Orientation:     {pct['control']}  (higher = more aligned, lower = over-controlling)
- Anxiety Level:           {pct['anxiety']}  (higher = lower anxiety / more comfortable)
- Boundary Respect:        {pct['boundary']}

Overall Risk Classification: {risk_label}

Multiple-Choice Answers:
{chr(10).join(mc_summary)}

Short-Answer Q7 (Biggest concern): {text_q7}
Short-Answer Q8 (Vision of partnership): {text_q8}

YOUR TASK:
Write a professional, empathetic admin summary (250–320 words) for nursery staff.
Structure it as:
1. Parent Profile Overview (2–3 sentences)
2. Strengths / Positives
3. Potential Risk Areas or Concerns
4. Recommended Onboarding Approach
5. Suggested Staff Actions (2–3 bullet points)

Tone: professional, non-judgmental, constructive, child-focused.
Do NOT use jargon. Write as if advising a senior nursery director.
Do NOT reveal numeric scores in the text — describe patterns qualitatively.
"""


def generate_report(answers: dict, scores: dict, risk_label: str) -> str:
    """
    Call Groq API to generate the admin narrative report.
    API key is loaded exclusively from st.secrets["GROQ_API_KEY"].
    Falls back to a rule-based summary if the key is unavailable or the call fails.
    """
    try:
        from groq import Groq

        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)

        prompt = build_prompt(answers, scores, risk_label)

        chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",   # Fast, high-quality Groq model
            max_tokens=800,
            temperature=0.5,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a specialist child development consultant. "
                        "Write professional, empathetic reports for nursery staff. "
                        "Be concise, constructive, and non-judgmental."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return chat_completion.choices[0].message.content

    except Exception:
        # Graceful fallback — rule-based narrative (no API key required)
        return generate_rule_based_report(answers, scores, risk_label)


def generate_rule_based_report(answers: dict, scores: dict, risk_label: str) -> str:
    """
    Fallback report generated without the API.
    Uses score thresholds to compose a structured narrative.
    """
    pct = scores["pct"]
    avg = sum(pct.values()) / len(pct)

    trust_label   = "strong" if pct["trust"] >= 70 else ("moderate" if pct["trust"] >= 45 else "limited")
    control_label = "healthy" if pct["control"] >= 70 else ("some concern" if pct["control"] >= 45 else "high concern")
    anxiety_label = "low" if pct["anxiety"] >= 70 else ("moderate" if pct["anxiety"] >= 45 else "elevated")
    boundary_label = "strong" if pct["boundary"] >= 70 else ("developing" if pct["boundary"] >= 45 else "limited")

    report = f"""Parent Profile Overview:
This family presents with {trust_label} trust in professional caregivers and {anxiety_label} transition-related anxiety. Their orientation toward control is categorised as {control_label}, and their respect for professional boundaries appears {boundary_label}. The overall enrollment risk is assessed as: {risk_label}.

Strengths & Positives:
"""
    positives = []
    if pct["trust"] >= 65:
        positives.append("Demonstrates a willingness to defer to professional expertise.")
    if pct["anxiety"] >= 65:
        positives.append("Shows emotional readiness for their child's transition to nursery.")
    if pct["boundary"] >= 65:
        positives.append("Respects structured communication and professional boundaries.")
    if pct["control"] >= 65:
        positives.append("Understands the nursery's independent role in child development.")
    if not positives:
        positives.append("Expresses genuine concern for their child's wellbeing and comfort.")
    report += "\n".join(f"• {p}" for p in positives)

    report += "\n\nPotential Risk Areas:\n"
    risks = []
    if pct["trust"] < 50:
        risks.append("May struggle to trust team decisions without direct involvement.")
    if pct["anxiety"] < 50:
        risks.append("Elevated parental anxiety could disrupt the child's settling process.")
    if pct["control"] < 50:
        risks.append("Tendencies toward over-involvement may challenge professional boundaries.")
    if pct["boundary"] < 50:
        risks.append("May not readily respect the nursery's communication structures.")
    if not risks:
        risks.append("No significant risk areas identified at this stage.")
    report += "\n".join(f"• {r}" for r in risks)

    report += f"""

Recommended Onboarding Approach:
{'A standard transition plan is appropriate. Maintain regular communication through daily summaries.' if avg >= 72 else 
 'Consider an extended settling-in period with proactive check-ins and a dedicated key worker relationship.' if avg >= 48 else 
 'A tailored onboarding meeting with the nursery director is strongly recommended before enrollment confirmation. Discuss communication expectations, boundary-setting, and the nursery\'s professional approach explicitly.'}

Suggested Staff Actions:
• Assign an experienced key worker and schedule a pre-enrollment introductory meeting.
• Share the nursery's communication policy clearly at induction.
• {'Monitor settling-in progress closely and provide structured weekly feedback.' if avg < 60 else 'Follow standard settling-in procedures with a daily pickup debrief in week one.'}
"""
    return report.strip()


# ─────────────────────────────────────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────
def render_header():
    """Logo + hero text."""
    # Logo
    import os
    if os.path.exists("logo.png"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", use_container_width=True)
    else:
        st.markdown(
            '<div style="text-align:center;font-size:3rem;margin-bottom:0.25rem;">🌱</div>',
            unsafe_allow_html=True,
        )

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


def render_progress(current: int, total: int):
    """Animated progress bar."""
    pct = int((current / total) * 100)
    st.markdown(
        f"""
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{pct}%"></div>
        </div>
        <div class="progress-label">Question {current} of {total}</div>
        """,
        unsafe_allow_html=True,
    )


def render_question_card(q: dict, q_num: int, answers: dict):
    """
    Render a single question inside a styled card.
    Returns the updated answer value.
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

    if q["type"] == "single":
        options = [opt["label"] for opt in q["options"]]
        current_val = answers.get(q["id"], None)
        idx = options.index(current_val) if current_val in options else None

        # st.radio — index=None means no default selection
        selected = st.radio(
            label=f"_q{q['id']}_",
            options=options,
            index=idx,
            key=f"radio_{q['id']}",
            label_visibility="collapsed",
        )
        return selected

    elif q["type"] == "text":
        val = st.text_area(
            label=f"_q{q['id']}_",
            value=answers.get(q["id"], ""),
            placeholder=q.get("placeholder", ""),
            key=f"text_{q['id']}",
            label_visibility="collapsed",
            height=110,
        )
        return val

    return None


def render_score_bar(dim_name: str, pct: int, color: str):
    """Render a single animated score bar."""
    st.markdown(
        f"""
        <div class="score-row">
            <div class="score-dim">{dim_name}</div>
            <div class="score-bar-bg">
                <div class="score-bar-fill" style="width:{pct}%; background:{color};"></div>
            </div>
            <div class="score-val">{pct}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_admin_panel(answers: dict, scores: dict):
    """Full admin report panel (shown only after admin toggle)."""
    risk_level, risk_label, badge_class = classify_risk(scores)

    st.markdown('<div class="admin-header">🔒 Admin Assessment Report</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="admin-meta">Generated: {datetime.now().strftime("%d %b %Y, %H:%M")}</div>',
        unsafe_allow_html=True,
    )

    # Risk badge
    st.markdown(
        f'<span class="risk-badge {badge_class}">{risk_label}</span>',
        unsafe_allow_html=True,
    )

    # Dimension score bars
    st.markdown("**Dimension Scores**")
    dim_colors = {
        "trust":   "#5A7A5A",
        "control": "#7A8A5A",
        "anxiety": "#8A7A5A",
        "boundary":"#5A7A8A",
    }
    dim_labels = {
        "trust": "Trust in Professionals",
        "control": "Control Orientation",
        "anxiety": "Transition Comfort",
        "boundary": "Boundary Respect",
    }
    pct = scores["pct"]
    for dim, label in dim_labels.items():
        render_score_bar(label, pct[dim], dim_colors[dim])

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Dimension explanations
    st.markdown("**Dimension Insights**")
    dim_explanations = {
        "trust": (
            "Trust in Professionals",
            "Reflects the parent's willingness to accept nursery staff decisions without needing constant justification. "
            "Low scores indicate a tendency to question professional judgment, which may require additional communication investment."
        ),
        "control": (
            "Control Orientation",
            "Measures how much the parent expects direct influence over day-to-day nursery decisions. "
            "High alignment means the parent understands the nursery operates independently within agreed frameworks."
        ),
        "anxiety": (
            "Transition Comfort",
            "Indicates emotional readiness for the child's independent experience at nursery. "
            "Parents with low scores may show visible anxiety during drop-offs, which can affect the child's settling."
        ),
        "boundary": (
            "Boundary Respect",
            "Assesses how well the parent is likely to respect communication structures, visit policies, and professional boundaries. "
            "Low scores may lead to boundary-testing behaviors such as unannounced visits."
        ),
    }
    for dim, (title, explanation) in dim_explanations.items():
        score_indicator = "✅" if pct[dim] >= 70 else ("⚠️" if pct[dim] >= 45 else "🔴")
        st.markdown(
            f"""
            <div class="dim-card">
                <div class="dim-card-title">{score_indicator} {title} — {pct[dim]}%</div>
                <div class="dim-card-body">{explanation}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # AI / rule-based narrative report
    st.markdown("**Narrative Summary**")
    with st.spinner("Generating professional assessment…"):
        report_text = generate_report(answers, scores, risk_label)

    st.markdown(
        f'<div class="report-block">{report_text.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Parent's own words
    with st.expander("📝 Parent's Open Responses"):
        st.markdown(f"**Q7 — Biggest concern:**  \n{answers.get('q7', '—')}")
        st.markdown(f"**Q8 — Vision of partnership:**  \n{answers.get('q8', '—')}")

    # Export button
    export_text = build_export_text(answers, scores, risk_label, report_text)
    st.download_button(
        label="⬇  Download Report (.txt)",
        data=export_text,
        file_name=f"enrollment_assessment_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
    )


def build_export_text(answers, scores, risk_label, report_text) -> str:
    """Compose a plain-text exportable report."""
    lines = [
        "=" * 60,
        "  NURSERY PRE-ENROLLMENT ASSESSMENT REPORT",
        f"  Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        "=" * 60,
        "",
        f"RISK CLASSIFICATION: {risk_label}",
        "",
        "DIMENSION SCORES",
        "-" * 40,
    ]
    dim_labels = {
        "trust": "Trust in Professionals",
        "control": "Control Orientation",
        "anxiety": "Transition Comfort",
        "boundary": "Boundary Respect",
    }
    for dim, label in dim_labels.items():
        lines.append(f"  {label:<28}: {scores['pct'][dim]}%")

    lines += ["", "MULTIPLE-CHOICE ANSWERS", "-" * 40]
    for q in QUESTIONS:
        if q["type"] == "single":
            lines.append(f"  {q['text']}")
            lines.append(f"  → {answers.get(q['id'], 'No answer')}")
            lines.append("")

    lines += ["OPEN RESPONSES", "-" * 40]
    lines.append(f"  Q7 — Biggest concern:\n  {answers.get('q7', '—')}")
    lines.append("")
    lines.append(f"  Q8 — Vision of partnership:\n  {answers.get('q8', '—')}")
    lines += ["", "NARRATIVE REPORT", "-" * 40, report_text, "", "=" * 60]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────────────────
def main():
    inject_styles()

    # ── Session state initialisation ──────────────────────────────────────────
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "scores" not in st.session_state:
        st.session_state.scores = None
    if "show_admin" not in st.session_state:
        st.session_state.show_admin = False
    if "report_text" not in st.session_state:
        st.session_state.report_text = ""

    # ── THANK-YOU SCREEN ──────────────────────────────────────────────────────
    if st.session_state.submitted:
        # Show logo even on thank-you
        import os
        if os.path.exists("logo.png"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("logo.png", use_container_width=True)
        else:
            st.markdown('<div style="text-align:center;font-size:3rem;">🌱</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="thankyou-wrap">
                <div class="thankyou-icon">🌿</div>
                <div class="thankyou-title">Thank You for Sharing</div>
                <div class="thankyou-body">
                    We've received your responses and our team will review them carefully.
                    A member of our team will be in touch shortly to discuss next steps
                    and answer any questions you may have.<br><br>
                    We look forward to welcoming your child into our community.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Admin toggle ──────────────────────────────────────────────────────
        with st.expander("🔒 Staff Access — View Assessment Report", expanded=False):
            # Simple PIN protection
            pin = st.text_input(
                "Enter staff PIN to view report",
                type="password",
                key="admin_pin",
                placeholder="••••",
            )
            if pin == "1234":   # Change PIN via st.secrets in production
                st.session_state.show_admin = True
            elif pin and pin != "1234":
                st.warning("Incorrect PIN.")

        if st.session_state.show_admin and st.session_state.scores:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            render_admin_panel(st.session_state.answers, st.session_state.scores)

        # Reset button (for demo / testing)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↩  Start a New Assessment"):
            for key in ["submitted", "answers", "scores", "show_admin", "report_text"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        return   # Stop rendering the form

    # ── ASSESSMENT FORM ───────────────────────────────────────────────────────
    render_header()

    st.markdown(
        '<div class="info-note">ℹ  This form takes approximately 3–5 minutes to complete. '
        'All responses are handled with care and complete confidentiality.</div>',
        unsafe_allow_html=True,
    )

    # Track answered MC questions for progress
    answered_mc = sum(
        1 for q in QUESTIONS
        if q["type"] == "single" and st.session_state.answers.get(q["id"])
    )
    answered_text = sum(
        1 for q in QUESTIONS
        if q["type"] == "text" and st.session_state.answers.get(q["id"], "").strip()
    )
    total_answered = answered_mc + answered_text
    render_progress(min(total_answered, TOTAL_QUESTIONS), TOTAL_QUESTIONS)

    # ── Render questions ──────────────────────────────────────────────────────
    current_section = None
    for i, q in enumerate(QUESTIONS, start=1):
        # Section divider
        if q["section"] != current_section:
            current_section = q["section"]
            st.markdown(
                f'<div class="section-label">{current_section}</div>',
                unsafe_allow_html=True,
            )

        answer = render_question_card(q, i, st.session_state.answers)
        if answer is not None:
            st.session_state.answers[q["id"]] = answer

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Validation & Submit ───────────────────────────────────────────────────
    mc_questions = [q for q in QUESTIONS if q["type"] == "single"]
    unanswered_mc = [
        q for q in mc_questions
        if not st.session_state.answers.get(q["id"])
    ]

    if unanswered_mc:
        st.markdown(
            f'<div class="info-note" style="color:#9B3A3A;background:#FAE0E0;">⚠  '
            f'Please answer all {len(unanswered_mc)} remaining question(s) before submitting.</div>',
            unsafe_allow_html=True,
        )

    submit_disabled = bool(unanswered_mc)
    submitted = st.button(
        "Submit Reflection →",
        disabled=submit_disabled,
        key="submit_btn",
    )

    if submitted and not submit_disabled:
        # Score and store
        scores = compute_scores(st.session_state.answers)
        st.session_state.scores = scores
        st.session_state.submitted = True
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
