"""Reusable UI helper for the overall fit score card."""

import streamlit as st


def render_score_card(score_data: dict):
    """Render the overall score, component scores, and fit decision."""
    st.subheader("Overall Fit Score")
    cols = st.columns(3)
    cols[0].metric("Final Score", f"{score_data.get('final_score', 0):.2f}/100")
    cols[1].metric(
        "Skills",
        f"{score_data.get('breakdown', {}).get('skills', 0):.2f}/50",
    )
    cols[2].metric(
        "Experience",
        f"{score_data.get('breakdown', {}).get('experience', 0):.2f}/50",
    )
    st.markdown(f"**Decision:** {score_data.get('decision', 'N/A')}")
    st.caption(
        "Skills and experience each contribute 50 points. "
        "75+ Strong Fit, 60-74 Moderate Fit, 40-59 Weak Fit, below 40 Not Suitable."
    )
