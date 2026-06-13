from pydantic import ValidationError

from utils.pdf_loader import extract_text
from utils.text_cleaner import clean_text
from schemas.pydantic_models import ResumeModel

from chains.segment_chain import get_segment_chain
from chains.skills_chain import get_skills_chain
from chains.experience_chain import get_experience_chain
from chains.projects_chain import get_projects_chain
from chains.education_chain import get_education_chain

from matching.skill_matcher import match_skills
from matching.experience_matcher import match_experience

from scoring.skill_scorer import score_skills
from scoring.experience_scorer import score_experience
from scoring.final_scorer import compute_final_score, get_decision

from analysis.gap_analyzer import analyze_skill_gaps
from analysis.suggestion_generator import generate_suggestions


# ---------------- SAFE INVOKE ----------------
def safe_invoke(chain, input_data, step_name=""):
    try:
        return chain.invoke(input_data)
    except Exception as e:
        print(f"[ERROR] {step_name} failed:", e)
        return None


# ---------------- MAIN PIPELINE ----------------
def process_resume(pdf_path: str):
    # Step 1: Extract + Clean
    raw = extract_text(pdf_path)
    clean = clean_text(raw)

    # Step 2: Segment
    segment_chain = get_segment_chain()
    sections = safe_invoke(segment_chain, {"text": clean}, "Segmentation")

    if sections is None:
        raise Exception("Segmentation failed")

    # Step 3: Extract each section
    skills_obj = safe_invoke(
        get_skills_chain(),
        {"text": sections.skills_section},
        "Skills Extraction"
    )

    exp_obj = safe_invoke(
        get_experience_chain(),
        {"text": sections.experience_section},
        "Experience Extraction"
    )

    proj_obj = safe_invoke(
        get_projects_chain(),
        {"text": sections.projects_section},
        "Projects Extraction"
    )

    edu_obj = safe_invoke(
        get_education_chain(),
        {"text": sections.education_section},
        "Education Extraction"
    )

    # Step 4: Convert to dict safely
    result = {
        "skills": skills_obj.skills if skills_obj else [],
        "experience": exp_obj.experience if exp_obj else [],
        "projects": proj_obj.projects if proj_obj else [],
        "education": edu_obj.education if edu_obj else []
    }

    # Step 5: Final validation (CRITICAL)
    try:
        validated = ResumeModel(**result)
    except ValidationError as e:
        print("\n[VALIDATION ERROR]")
        print(e)
        raise

    return validated.dict()


def run_matching(resume_json, jd_json):
    skill_result = match_skills(
        jd_json.get("required_skills", []),
        resume_json
    )

    experience_result = match_experience(
        jd_json.get("responsibilities", []),
        resume_json.get("experience", [])
    ).model_dump()

    return {
        "skills": skill_result,
        "experience": experience_result
    }


def run_scoring(match_result):
    skill_score = score_skills(match_result["skills"])
    exp_score = score_experience(match_result["experience"])

    final_score = compute_final_score(skill_score, exp_score)

    decision = get_decision(final_score)

    return {
        "final_score": final_score,
        "breakdown": {
            "skills": skill_score,
            "experience": exp_score
        },
        "decision": decision
    }


def run_analysis(resume_json, jd_json, match_result):
    gap_data = analyze_skill_gaps(match_result, jd_json)

    suggestions = generate_suggestions(
        jd_json,
        resume_json,
        gap_data
    )

    return {
        "gaps": gap_data,
        "suggestions": suggestions.dict()
    }
