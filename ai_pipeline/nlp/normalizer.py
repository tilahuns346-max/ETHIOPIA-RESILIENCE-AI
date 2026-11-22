import re
AMHARIC_STOP_WORDS = {"ነው", "ላይ", "ውስጥ", "ጋር", "ወደ", "ከ", "እና", "ስለ", "እንደ", "ነበር"}

def normalize_amharic_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"[ሐኀ]", "ሀ", text)
    text = re.sub(r"[ሠ]", "ሰ", text)
    text = re.sub(r"[ዐ]", "አ", text)
    text = re.sub(r"[ፀ]", "ጸ", text)
    return " ".join([t for t in text.split() if t not in AMHARIC_STOP_WORDS])
