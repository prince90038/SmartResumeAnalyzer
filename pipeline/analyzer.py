"""High-level orchestration for the resume and job-description analysis flow."""

from pipeline.jd_pipeline import process_jd
from pipeline.resume_pipeline import (
    process_resume,
    run_analysis,
    run_matching,
    run_scoring,
)


def analyze_resume(resume_path: str, jd_text: str) -> dict:
    """Run the full analysis pipeline and return match, score, and gap data."""
    resume = process_resume(resume_path)
    jd = process_jd(jd_text)
    match = run_matching(resume, jd)

    return {
        **match,
        "score": run_scoring(match),
        "analysis": run_analysis(resume, jd, match),
    }
