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
    return skill.lower().strip()


def is_abstract_requirement(skill: str) -> bool:
    normalized = normalize_skill(skill)
    return any(pattern in normalized for pattern in ABSTRACT_SKILL_PATTERNS)


def classify_score(score, is_abstract=False):
    if score >= 0.75:
        return "matched"
    if score >= 0.55:
        return "partial"
    if is_abstract and score >= 0.45:
        return "partial"
    return "missing"


def collect_resume_candidates(resume_json):
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
    normalized = get_jd_normalizer_chain().invoke({
        "text": "\n".join(jd_skills)
    })

    jd_skills = [normalize_skill(s) for s in normalized.skills]
    resume_candidates = collect_resume_candidates(resume_json)

    resume_vecs = embed_texts(resume_candidates)

    matched = []
    partial = []
    missing = []
    detailed = []

    for jd_skill in jd_skills:
        jd_vec = embed_texts([jd_skill])[0]

        best_match = None
        best_score = -1.0
        for idx, candidate_vec in enumerate(resume_vecs):
            _, score = find_best_match(jd_vec, [candidate_vec])
            if score > best_score:
                best_score = score
                best_match = resume_candidates[idx]

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
