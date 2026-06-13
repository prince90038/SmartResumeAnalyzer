from chains.jd_chain import get_jd_chain
from schemas.pydantic_models import JDOutput

from pydantic import ValidationError


# ---------------- SAFE INVOKE ----------------
def safe_invoke(chain, input_data, step_name=""):
    try:
        return chain.invoke(input_data)
    except Exception as e:
        print(f"[ERROR] {step_name} failed:", e)
        return None


# ---------------- MAIN JD PIPELINE ----------------
def process_jd(jd_text: str):
    jd_chain = get_jd_chain()

    jd_obj = safe_invoke(
        jd_chain,
        {"text": jd_text},
        "JD Parsing"
    )

    if jd_obj is None:
        raise Exception("JD parsing failed completely")

    # Convert to dict safely
    result = {
        "required_skills": jd_obj.required_skills or [],
        "optional_skills": jd_obj.optional_skills or [],
        "experience_required": jd_obj.experience_required or "",
        "responsibilities": jd_obj.responsibilities or []
    }

    # Final validation
    try:
        validated = JDOutput(**result)
    except ValidationError as e:
        print("\n[JD VALIDATION ERROR]")
        print(e)
        raise

    return validated.dict()
