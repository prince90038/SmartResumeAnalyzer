"""Reusable UI helpers for displaying skill gaps."""

import streamlit as st

from ui.components.comparison import as_bullets


def render_gaps(gaps_data: dict):
    """Render the critical and secondary gap sections."""
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
