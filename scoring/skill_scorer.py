"""Convert skill-matching categories into a weighted score."""

SKILL_WEIGHT = 50


def score_skills(skill_result):
    """Score skill matches on a 0-50 scale."""
    matched = len(skill_result.get("matched", []))
    partial = len(skill_result.get("partial", []))
    total = matched + partial + len(skill_result.get("missing", []))

    if total == 0:
        return 0

    # weighted scoring
    score = (matched * 1.0 + partial * 0.5) / total

    return round(score * SKILL_WEIGHT, 2)
