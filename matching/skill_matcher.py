"""Semantic skill matching between normalized JD skills and resume evidence."""

from matching.embedding import embed_texts
from matching.similarity import find_best_match
from matching.jd_normalizer import get_jd_normalizer_chain


ABSTRACT_SKILL_PATTERNS = [
    "knowledge",
    "understanding",
    "ability",
    "experience",
    "expertise",
    "principles",
    "architecture",
    "design"
]


def normalize_skill(skill: str) -> str:
    """Normalize a skill label for comparison and deduplication."""
    return skill.lower().strip()


def is_abstract_requirement(skill: str) -> bool:
    """Return True when a JD skill is phrased as a broad requirement."""
    normalized = normalize_skill(skill)
    return any(pattern in normalized for pattern in ABSTRACT_SKILL_PATTERNS)


def classify_score(score, is_abstract=False):
    """Map similarity scores to matched, partial, or missing categories."""
    if score >= 0.75:
        return "matched"
    if score >= 0.55:
        return "partial"
    if is_abstract and score >= 0.45:
        return "partial"
    return "missing"


def collect_resume_candidates(resume_json):
    """Build the text candidates used to compare resume evidence to JD skills."""
    candidates = set()

    for skill in resume_json.get("skills", []):
        candidates.add(normalize_skill(skill))

    for project in resume_json.get("projects", []):
        for tech in project.get("technologies", []):
            candidates.add(normalize_skill(tech))

    for exp in resume_json.get("experience", []):
        description = exp.get("description", "").strip()
        if description:
            candidates.add(normalize_skill(description))

    if not candidates:
        candidates.add("")

    return sorted(candidates)


def match_skills(jd_skills, resume_json):
    """Match normalized JD skills against resume evidence using embeddings."""
    normalized = get_jd_normalizer_chain().invoke({
        "text": "\n".join(jd_skills)
    })

    jd_skills = list(
        dict.fromkeys(normalize_skill(skill) for skill in normalized.skills if skill.strip())
    )
    if not jd_skills:
        return {"matched": [], "partial": [], "missing": [], "details": []}

    resume_candidates = collect_resume_candidates(resume_json)

    resume_vecs = embed_texts(resume_candidates)
    jd_vecs = embed_texts(jd_skills)

    matched = []
    partial = []
    missing = []
    detailed = []

    for jd_skill, jd_vec in zip(jd_skills, jd_vecs):
        best_idx, best_score = find_best_match(jd_vec, resume_vecs)
        best_match = resume_candidates[best_idx]
        best_score = min(max(best_score, 0), 1)

        category = classify_score(best_score, is_abstract_requirement(jd_skill))

        detailed.append({
            "jd_skill": jd_skill,
            "best_match": best_match,
            "score": best_score,
            "category": category
        })

        if category == "matched":
            matched.append(jd_skill)
        elif category == "partial":
            partial.append(jd_skill)
        else:
            missing.append(jd_skill)

    return {
        "matched": matched,
        "partial": partial,
        "missing": missing,
        "details": detailed
    }
