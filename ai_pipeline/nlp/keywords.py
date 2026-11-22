AMHARIC_HAZARD_LEXICON = {
    "HAZ-LANDSLIDE": ["ናዳ", "መደርመስ", "መሬት", "ተራራ", "ተደርምሶ"],
    "HAZ-FLASH-FLOOD": ["ጎርፍ", "ውሃ", "ሙላት", "ወንዝ", "መጥለቅለቅ"],
    "HAZ-DROUGHT": ["ድርቅ", "ዝናብ", "ከብት", "ውሃ እጥረት", "ግጦሽ"],
    "HAZ-WILDFIRE": ["ሰደድ", "እሳት", "ደን", "ቃጠሎ"]
}

def detect_hazard_from_amharic_text(text: str) -> str:
    scores = {h: sum(1 for kw in kws if kw in text) for h, kws in AMHARIC_HAZARD_LEXICON.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "HAZ-LANDSLIDE"
