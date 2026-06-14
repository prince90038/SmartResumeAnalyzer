"""Text normalization helpers for resume and job-description content."""

import re


def clean_text(text: str) -> str:
    """Normalize whitespace and repair broken bullet-style line wrapping."""
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)

    for bullet in (
        "\u2022",
        "\u25cf",
        "\u25aa",
        "\u00e2\u20ac\u00a2",
        "\u00e2\u2014\u008f",
    ):
        text = text.replace(bullet, "-")

    lines = text.split("\n")
    cleaned = []
    buffer = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if re.search(r"[.!?:]$", line):
            buffer += " " + line
            cleaned.append(buffer.strip())
            buffer = ""
        else:
            buffer += " " + line

    if buffer:
        cleaned.append(buffer.strip())

    return "\n".join(cleaned)
