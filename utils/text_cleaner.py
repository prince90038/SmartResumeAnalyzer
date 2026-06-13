import re

def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)

    text = text.replace("•", "-").replace("●", "-")

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
