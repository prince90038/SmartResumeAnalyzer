"""Derive critical and secondary skill gaps from matching results."""


def analyze_skill_gaps(match_result, jd_json):
    """Group missing and partial skills into priority gap buckets."""
    missing = match_result["skills"].get("missing", [])
    partial = match_result["skills"].get("partial", [])

    # prioritize missing over partial
    priority_gaps = missing + partial

    return {
        "critical_gaps": missing,
        "secondary_gaps": partial,
        "all_gaps": priority_gaps
    }
