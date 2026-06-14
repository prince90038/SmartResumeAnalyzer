"""Lightweight validation helpers for extracted resume structures."""


def validate_resume(data: dict):
    """Ensure the extracted resume contains the minimum expected sections."""
    if not data.get("skills"):
        raise ValueError("Skills missing")

    if not data.get("experience"):
        raise ValueError("Experience missing")

    return True
