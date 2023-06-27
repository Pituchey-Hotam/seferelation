from typing import List

import requests
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
    for source in source_text:
        sefaria_ref = translate_source_to_sefaria(source)
        print(f"souce:\t{source}\nsefaria:\t{sefaria_ref}")


def translate_source_to_sefaria(heb_ref: str) -> str:
    url = f"https://www.sefaria.org/api/name/{heb_ref}"
    response = requests.get(url).json()
    if response["is_ref"] == True:
        return response["ref"]
    return "pasten"



if __name__ == "__main__":
    import sys
    print(sys.argv)
    parse_pdf_to_sefaria(sys.argv[1])

