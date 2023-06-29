import re

def _is_gematria(word: str) -> bool:
    gershaim = set("'\"")
    return bool(
        re.match(r"^[קרשת]?[יכלמנסעפצ]?['\"]?[אבגדהוזחט]?[']?$", word)
        and not set(word) == gershaim
        and len(list(filter(lambda c: c in gershaim, word))) < 2
    )

def _gimatria_calc(word: str) -> int:
    pass

def _is_gmara_index(word: str) -> bool:
    return bool(
        re.match(r"^[קרשת]?[יכלמנסעפצ]?[אבגדהוזחט]?\s?[.:]?$", word)
        and re.match(r"[א-ת]", word)
    )
