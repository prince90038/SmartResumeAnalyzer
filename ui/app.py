import streamlit as st

from pipeline.resume_pipeline import process_resume, run_matching, run_scoring
from pipeline.jd_pipeline import process_jd
from analysis.gap_analyzer import analyze_skill_gaps
from analysis.suggestion_generator import generate_suggestions


def render_score_card(score_data: dict):
    st.subheader("Overall Fit Score")
    cols = st.columns(3)
    cols[0].metric("Final Score", score_data.get("final_score", "N/A"))
    cols[1].metric("Skills", score_data.get("breakdown", {}).get("skills", "N/A"))
    cols[2].metric("Experience", score_data.get("breakdown", {}).get("experience", "N/A"))
    st.markdown(f"**Decision:** {score_data.get('decision', 'N/A')}\n")
    st.caption("Final Score = Skills score + Experience score, with each component scaled to 40 points for a maximum total of 80.")
    st.caption("Decision classification: 75+ Strong Fit, 60-74 Moderate Fit, 40-59 Weak Fit, below 40 Not Suitable.")


def format_percentage(value):
    if value is None:
        return "N/A"
    try:
        return f"{float(value) * 100:.0f}%"
    except (TypeError, ValueError):
        return str(value)


def as_bullets(items):
    if not items:
        return ["No items found."]
    if isinstance(items, str):
        lines = [line.strip("-• \t") for line in items.splitlines() if line.strip()]
        return [f"- {line}" for line in lines] if lines else ["No items found."]
    return [f"- {item}" for item in items]


def render_skill_summary(skills_data: dict):
    st.subheader("Required Skill Matching")
    cols = st.columns(3)
    cols[0].metric("Matched", len(skills_data.get("matched", [])))
    cols[1].metric("Partial", len(skills_data.get("partial", [])))
    cols[2].metric("Missing", len(skills_data.get("missing", [])))

    with st.expander("Skill match details"):
        if skills_data.get("details"):
            details = []
            for item in skills_data["details"]:
                details.append({
                    "JD Skill": item.get("jd_skill", ""),
                    "Best Match": item.get("best_match", ""),
                    "Score": format_percentage(item.get("score", 0)),
                    "Category": item.get("category", "")
                })
            st.dataframe(details, use_container_width=True)
        else:
            st.write("No skill match details available.")


def render_experience_summary(experience_data: dict):
    st.subheader("Experience Match")
    st.markdown(f"**Relevance score:** {format_percentage(experience_data.get('relevance_score'))}")
    st.markdown("**Matched areas:**")
    for line in as_bullets(experience_data.get("matched_areas", [])):
        st.markdown(line)
    st.markdown("**Missing areas:**")
    for line in as_bullets(experience_data.get("missing_areas", [])):
        st.markdown(line)


def render_gaps(gaps_data: dict):
    st.subheader("Gap Analysis")
    cols = st.columns(3)
    cols[0].metric("Critical gaps", len(gaps_data.get("critical_gaps", [])))
    cols[1].metric("Secondary gaps", len(gaps_data.get("secondary_gaps", [])))
    cols[2].metric("Total gaps", len(gaps_data.get("all_gaps", [])))

    with st.expander("View gap lists"):
        st.markdown("**Critical gaps**")
        for line in as_bullets(gaps_data.get("critical_gaps", [])):
            st.markdown(line)
        st.markdown("**Secondary gaps**")
        for line in as_bullets(gaps_data.get("secondary_gaps", [])):
            st.markdown(line)


def render_suggestions(suggest_data: dict):
    st.subheader("Resume Improvement Suggestions")
    for section, items in suggest_data.items():
        st.markdown(f"**{section.replace('_', ' ').title()}:**")
        if items:
            for item in items:
                st.markdown(f"- {item}")
        else:
            st.write("No suggestions available.")
        st.write("")


st.title("Smart Resume Analyzer")

st.markdown(
    "Upload a PDF resume and paste the job description to receive a skill and experience match analysis, score breakdown, gap analysis, and resume suggestions."
)

resume_file = st.file_uploader("Upload Resume (PDF)")
jd_text = st.text_area("Paste Job Description")


if st.button("Analyze"):
    if resume_file and jd_text:
        with open("temp_resume.pdf", "wb") as f:
            f.write(resume_file.read())

        resume = process_resume("temp_resume.pdf")
        jd = process_jd(jd_text)

        match = run_matching(resume, jd)
        score = run_scoring(match)
        gaps = analyze_skill_gaps(match, jd)
        suggestions = generate_suggestions(jd, resume, gaps)

        render_score_card(score)
        render_skill_summary(match["skills"])
        render_experience_summary(match["experience"])
        render_gaps(gaps)
        render_suggestions(suggestions.dict())
    else:
        st.warning("Upload resume and enter JD")
