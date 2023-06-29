import pytest

from seferelation import pdf_parser



@pytest.mark.parametrize("gimatria, expected", [
    ("ב", True),
    ("יא", True),
    ("קכא", True),
    ("תו", True),
    ("ת'ו", True),
    ("תו'", True),
    ("קכ\"א", True),
    ("פסטן", False),
    ("ככא", False),
    ("קקא", False),
    ("בלא", False),
    ("ק'כא", False),
])
def test_is_gimatria(gimatria, expected):
    assert pdf_parser._is_gematria(gimatria) == expected
