"""Convert experience relevance into a weighted score."""

EXPERIENCE_WEIGHT = 50


def score_experience(exp_result):
    """Score experience relevance on a 0-50 scale."""
    relevance = float(exp_result.get("relevance_score", 0))
    relevance = min(max(relevance, 0), 1)

    return round(relevance * EXPERIENCE_WEIGHT, 2)
