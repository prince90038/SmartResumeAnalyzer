def score_skills(skill_result):
    matched = len(skill_result.get("matched", []))
    partial = len(skill_result.get("partial", []))
    total = matched + partial + len(skill_result.get("missing", []))

    if total == 0:
        return 0

    # weighted scoring
    score = (matched * 1.0 + partial * 0.5) / total

    # scale to 40
    return round(score * 40, 2)
