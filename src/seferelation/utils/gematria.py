import re

def is_gematria(word: str) -> bool:
    gershaim = set("'\"")
    return bool(
        re.match(r"^[קרשת]?[יכלמנסעפצ]?['\"]?[אבגדהוזחט]?[']?$", word)
        and not set(word) == gershaim
        and len(list(filter(lambda c: c in gershaim, word))) < 2
    )

GEMATRIA_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100,
    'ר': 200, 'ש': 300, 'ת': 400
}

def gematria_calc(word: str) -> int:
    value = 0
    for letter in word:
        if letter in GEMATRIA_VALUES:
            value += GEMATRIA_VALUES[letter]
    return value


def is_gmara_index(word: str) -> bool:
    return bool(
        re.match(r"^[קרשת]?[יכלמנסעפצ]?[אבגדהוזחט]?\s?[.:]?$", word)
        and re.match(r"[א-ת]", word)
    )


def gmara_cacl_index(word: str) -> str:
    daf = str(gematria_calc(word))
    if "." in word:
        daf_side = "a"
    elif ":" in word:
        daf_side = "b"
    else:
        daf_side = "a"
    return daf + daf_side

