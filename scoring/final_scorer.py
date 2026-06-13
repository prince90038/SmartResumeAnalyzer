def compute_final_score(skill_score, exp_score, project_score=0):
    total = skill_score + exp_score + project_score
    return round(total, 2)


def get_decision(score):
    if score >= 75:
        return "Strong Fit"
    elif score >= 60:
        return "Moderate Fit"
    elif score >= 40:
        return "Weak Fit"
    else:
        return "Not Suitable"
