"""Reusable UI helper for resume improvement suggestions."""

import streamlit as st


def render_suggestions(suggestion_data: dict):
    """Render the generated improvement suggestions by section."""
    st.subheader("Resume Improvement Suggestions")
    for section, items in suggestion_data.items():
        st.markdown(f"**{section.replace('_', ' ').title()}:**")
        if items:
            for item in items:
                st.markdown(f"- {item}")
        else:
            st.write("No suggestions available.")
