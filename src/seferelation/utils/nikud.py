import re


def remove_nikud(text: str) -> str:
    punctuation_pattern = r"[\u0591-\u05BD\u05BF-\u05C2\u05C4-\u05C7]"
    clean_text = re.sub(punctuation_pattern, "", text)
    return clean_text
