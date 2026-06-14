"""Reusable UI helpers for skill and experience comparison sections."""

import streamlit as st


def format_percentage(value):
    """Render a numeric value as a percentage label when possible."""
    if value is None:
        return "N/A"
    try:
        return f"{float(value) * 100:.0f}%"
    except (TypeError, ValueError):
        return str(value)


def as_bullets(items):
    """Normalize list-like content into markdown bullet strings."""
    if not items:
        return ["No items found."]
    if isinstance(items, str):
        items = [line.strip("-• \t") for line in items.splitlines() if line.strip()]
    return [f"- {item}" for item in items]


def render_skill_summary(skills_data: dict):
    """Render the skill-match summary and detail table."""
    st.subheader("Required Skill Matching")
    cols = st.columns(3)
    cols[0].metric("Matched", len(skills_data.get("matched", [])))
    cols[1].metric("Partial", len(skills_data.get("partial", [])))
    cols[2].metric("Missing", len(skills_data.get("missing", [])))

    with st.expander("Skill match details"):
        details = [
            {
                "JD Skill": item.get("jd_skill", ""),
                "Best Match": item.get("best_match", ""),
                "Score": format_percentage(item.get("score", 0)),
                "Category": item.get("category", ""),
            }
            for item in skills_data.get("details", [])
        ]
        if details:
            st.dataframe(details, use_container_width=True)
        else:
            st.write("No skill match details available.")


def render_experience_summary(experience_data: dict):
    """Render the experience match summary section."""
    st.subheader("Experience Match")
    st.markdown(
        f"**Relevance score:** {format_percentage(experience_data.get('relevance_score'))}"
    )
    st.markdown("**Matched areas:**")
    for line in as_bullets(experience_data.get("matched_areas", [])):
        st.markdown(line)
    st.markdown("**Missing areas:**")
    for line in as_bullets(experience_data.get("missing_areas", [])):
        st.markdown(line)
