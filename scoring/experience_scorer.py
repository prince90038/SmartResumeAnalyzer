def score_experience(exp_result):
    relevance = float(exp_result.get("relevance_score", 0))

    # scale to 40
    return round(relevance * 40, 2)
