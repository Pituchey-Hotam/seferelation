from types import List

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


def parse_pdf_sources(path: str) -> List[str]:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text(visitor_text=_visitor_body))
    
    lines = ''.join(text).splitlines()
    source_lines = [line for line in lines if _is_source_line(line)]
    return source_lines


def translate_source_to_sefaria(heb_ref: str) -> str:
    pass
