import pytest

from seferelation.utils import gematria



@pytest.mark.parametrize("text, expected", [
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
def test_is_gematria(text, expected):
    assert gematria._is_gematria(text) == expected


@pytest.mark.parametrize("gmara, expected", [
    ("ב", True),
    ("קכא", True),
    ("יד:", True),
    ("ג .", True),
    (":", False),
    ("אבג:", False),
])
def test_is_gmara_index(gmara, expected):
    assert gematria._is_gmara_index(gmara) == expected