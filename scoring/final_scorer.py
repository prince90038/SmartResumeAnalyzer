"""Final score and decision helpers for the resume fit summary."""


def compute_final_score(skill_score, exp_score, project_score=0):
    """Combine the component scores into a bounded 0-100 final score."""
    total = skill_score + exp_score + project_score
    return round(min(max(total, 0), 100), 2)


def get_decision(score):
    """Convert the final score into a human-readable fit decision."""
    if score >= 75:
        return "Strong Fit"
    elif score >= 60:
        return "Moderate Fit"
    elif score >= 40:
        return "Weak Fit"
    else:
        return "Not Suitable"
