# modules/chat.py
import re

def clean_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s]", "", s)  # elimina signos de puntuación
    return s.strip()

