from typing import List, Union

import requests
import pickle
from pypdf import PdfReader
import re


def _visitor_body(text, cm, tm, font_dict, font_size):
    pass


def _is_source_line(line: str) -> bool:
    if re.match(r'^\d*\s?\.', line):
        return True
    if re.match(r'^[א-ת]?[א-ת]?\s?\.', line):
        return True
    return False


def _filter_source_line(line: str) -> str:
    idx = line.find(".")
    return line[idx+1:]


def parse_pdf_to_text_sources(path: str) -> List[str]:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text(visitor_text=_visitor_body))
    
    lines = ''.join(text).splitlines()
    source_lines = [_filter_source_line(line) for line in lines if _is_source_line(line)]
    return source_lines


def parse_pdf_to_sefaria(path: str) -> List[str]:
    source_text = parse_pdf_to_text_sources(path)
    refs = []
    for source in source_text:
        sefaria_ref = translate_source_to_sefaria(source)
        refs.append(sefaria_ref)
        # print(f"souce:\t{source}\nsefaria:\t{sefaria_ref}")
    print(f"total: {len(source_text)}")
    refs = set(refs)
    print("refs: ")
    print(len(refs))
    print(refs)
    print()


with open("scrapper/sefaria_he_titles_2023_06_27.pickle", "rb") as f:
    he_titles = pickle.load(f)

def _heb_source_to_sefaria_name(heb_ref: str) -> str:
    words = heb_ref.split(" ")
    for i in range(len(words)):
        for j in range(len(words)):
            sub_ref = " ".join(words[i:j+1])
            if sub_ref in he_titles:
                return he_titles[sub_ref]
    return "pasten"


def _is_gematria(word: str) -> bool:
    gershaim = set("'\"")
    return bool(
        re.match(r"^[קרשת]?[יכלמנסעפצ]?['\"]?[אבגדהוזחט]?[']?$", word)
        and not set(word) == gershaim
        and len(list(filter(lambda c: c in gershaim, word))) < 2
    )

def _is_gmara_index(word: str) -> bool:
    return re.match(r"^[קרשת]?[יכלמנסעפצ]??[אבגדהוזחט]?[.:]?$", word)

def _get_possible_indexes(heb_ref: str) -> List[Union[int, str]]:
    words = re.findall(r"[\w.'\"]+", heb_ref)
    


def translate_source_to_sefaria(heb_ref: str) -> str:
    name = _heb_source_to_sefaria_name(heb_ref)
    indexes = _get_possible_indexes(heb_ref)



if __name__ == "__main__":
    import sys
    print(sys.argv)
    parse_pdf_to_sefaria(sys.argv[1])

