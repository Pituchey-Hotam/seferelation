from typing import List, Union

import pickle
from pypdf import PdfReader
import re

from seferelation.utils import gematria, nikud
from seferelation.scrapper.sefaria_he_titles_extender import normalize_he_ref


def _visitor_body(text, cm, tm, font_dict, font_size):
    pass


def _is_source_line(line: str) -> bool:
    if len(line) < 5:
        return False
    if len(line) < 50:
        return True
    if re.match(r'^\d*\s?\.', line):
        return True
    if re.match(r'^[א-ת]?[א-ת]?\s?\.', line):
        return True
    return False


def _filter_source_line(line: str) -> str:
    idx = line.find(".")
    return line[idx+1:]


def parse_pdf_to_text_sources(path: str) -> List[str]:
    try:
        reader = PdfReader(path)
    except Exception:
        print(f"ERROR: pdf parse failed, file: {path}")
        return []
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
    # print(f"total: {len(source_text)}")
    refs = set(refs)
    if "" in refs:
        refs.remove("")
    # print("refs: ")
    # print(len(refs))
    # print(refs)
    # print()
    # print([reference.Reference(ref).to_sefaria_link() for ref in refs])
    return list(refs)


with open("scrapper/sefaria_he_titles_ext_3.pickle", "rb") as f:
    he_titles = pickle.load(f)

# import ipdb; ipdb.set_trace()

def _heb_source_to_sefaria_name(heb_ref: str) -> str:
    words = heb_ref.split()
    refs = {}
    for i in range(len(words)):
        for j in range(i, len(words)):
            sub_ref = " ".join(words[i:j+1])
            sub_ref_normal = normalize_he_ref(sub_ref)
            if sub_ref_normal in he_titles:
                if (j - i) not in refs:
                    refs[j - i] = he_titles[sub_ref_normal]
    if refs:
        return refs[max(refs.keys())]
    return ""


def _get_possible_indexes(heb_ref: str) -> List[str]:
    heb_ref = nikud.remove_nikud(heb_ref)
    words = re.findall(r"[\w.'\"]+", heb_ref)
    indexes = []
    for word in words:
        if gematria.is_gematria(word):
            indexes.append(str(gematria.gematria_calc(word)))
        elif gematria.is_gmara_index(word):
            indexes.append(gematria.gmara_calc_index(word))
    return indexes
    

def translate_source_to_sefaria(heb_ref: str) -> str:
    name = _heb_source_to_sefaria_name(heb_ref)
    if not name:
        return name
    indexes = _get_possible_indexes(heb_ref)
    return ".".join([name] + indexes)


if __name__ == "__main__":
    import sys
    print(sys.argv)
    parse_pdf_to_sefaria(sys.argv[1])

