from typing import Dict
import re
import pickle


HE_TITLES_PATH = "sefaria_he_titles.pickle"

def _ext_1_fix_whitespaces(he_titles: Dict[str, str]):
    fixed = {}
    for he, en in he_titles.items():
        fixed[he.strip()] = en
    return fixed


def ext_1_fix_whitespaces():
    with open(HE_TITLES_PATH, "rb") as f:
        he_titles = pickle.load(f)
    he_titles_ext_1 = _ext_1_fix_whitespaces(he_titles)
    with open("sefaria_he_titles_ext_1.pickle", "wb") as f:
        pickle.dump(he_titles_ext_1, f)


def ext_2_remove_redundent_al():
    """
    Transform names from: ר"ן על קידושין
    to: ר"ן קידושין
    """
    with open("sefaria_he_titles_ext_1.pickle", "rb") as f:
        he_titles = pickle.load(f)
    masehtot = [
        "ברכות", "שבת", "יבמות", "בבא קמא", "זבחים", "כתובות", "עירובין",
        "כתובות", "בבא מציעא", "מנחות", "פסחים", "נדרים", "בבא בתרא", "חולין", "נגעים",
        "כלאים", "שקלים", "נזיר", "סנהדרין", "בכורות", "פרה", "שביעית",
        "יומא", "סוטה", "מכות", "ערכין", "טהרות", "תרומות", "סוכה", "גיטין",
        "שבועות", "תמורה", "מקואות", "מעשרות", "ביצה", "קידושין", "עדיות",
        "כריתות", "נידה", "מעשר שני", "ראש השנה", "עבודה זרה", "מעילה", "מכשירין",
        "חלה", "תענית", "אבות", "תמיד", "זבים", "עוקצים"                                                                                                
    ]
    he_titles_ext = {}
    for he, en in he_titles.items():
        words = he.split(" ")
        if "על" not in words:
            continue
        al = words.index("על")
        if al > 0 and words[al+1] in masehtot:
            without_al = words[:al] + words[al+1:]
            he_titles_ext[" ".join(without_al)] = en
    print(f"old len: {len(he_titles)}")
    he_titles.update(he_titles_ext)
    print(f"add len: {len(he_titles_ext)}")
    with open("sefaria_he_titles_ext_2.pickle", "wb") as f:
        pickle.dump(he_titles, f)
            

def clear_special_characters(word: str) -> str:
    return ''.join([char for char in word if re.match(r'[א-ת0-9\s]', char)])

def ext_3_remove_quotes():
    """
    Remove quotes and other special characters.
    For example, it makes רמב"ם == רמבם
    """
    with open("sefaria_he_titles_ext_2.pickle", "rb") as f:
        he_titles: Dict = pickle.load(f)
    he_titles_ext = {}
    for title, en in he_titles.items():
        if re.search(r'[^א-ת0-9\s]', title):
            he_titles_ext[clear_special_characters(title)] = en
    print(f"old len: {len(he_titles)}")
    print(f"add len: {len(he_titles_ext)}")
    for title, en in he_titles_ext.items():
        if title not in he_titles:
            he_titles[title] = en
    print(len(he_titles))
    with open("sefaria_he_titles_ext_3.pickle", "wb") as f:
        pickle.dump(he_titles, f)


def normalize_he_ref(he_ref: str) -> str:
    return clear_special_characters(he_ref)


def main():
    ext_3_remove_quotes()


if __name__ == "__main__":
    main()