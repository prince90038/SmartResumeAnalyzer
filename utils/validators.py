def validate_resume(data: dict):
    if not data.get("skills"):
        raise ValueError("Skills missing")

    if not data.get("experience"):
        raise ValueError("Experience missing")

    return True
