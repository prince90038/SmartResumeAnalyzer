"""Streamlit entry point for the Smart Resume Analyzer dashboard."""

import logging
import tempfile
from pathlib import Path

import streamlit as st

from pipeline.analyzer import analyze_resume
from ui.components.comparison import (
    render_experience_summary,
    render_skill_summary,
)
from ui.components.gap_display import render_gaps
from ui.components.score_card import render_score_card
from ui.components.suggestions import render_suggestions

LOGGER = logging.getLogger(__name__)
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


st.set_page_config(page_title="Smart Resume Analyzer")
st.title("Smart Resume Analyzer")
st.markdown(
    "Upload a PDF resume and paste the job description to receive a skill and "
    "experience match analysis, score breakdown, gap analysis, and resume suggestions."
)

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=220)

if st.button("Analyze", type="primary"):
    if not resume_file:
        st.warning("Upload a PDF resume.")
    elif not jd_text.strip():
        st.warning("Enter a job description.")
    elif resume_file.size > MAX_UPLOAD_BYTES:
        st.warning("The resume PDF must be 10 MB or smaller.")
    else:
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix="temp_resume_",
                suffix=".pdf",
                delete=False,
            ) as temp_file:
                temp_file.write(resume_file.getbuffer())
                temp_path = Path(temp_file.name)

            with st.spinner("Analyzing the resume and job description..."):
                result = analyze_resume(str(temp_path), jd_text.strip())

            render_score_card(result["score"])
            render_skill_summary(result["skills"])
            render_experience_summary(result["experience"])
            render_gaps(result["analysis"]["gaps"])
            render_suggestions(result["analysis"]["suggestions"])
        except Exception as exc:
            LOGGER.exception("Resume analysis failed")
            st.error(
                "Analysis could not be completed. Check the configuration, "
                "network connection, and PDF contents, then try again."
            )
            with st.expander("Technical details"):
                st.code(str(exc))
        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)
