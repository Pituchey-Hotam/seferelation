import pytest

from seferelation.utils.reference import Reference


@pytest.mark.parametrize("ref, expected", [
    ("Book 2:1-7", True),
    ("Book 2:7", False),
])
def test_ref_is_range(ref, expected):
    assert Reference(ref).is_range() == expected


@pytest.mark.parametrize("ref, ref_range, expected", [
    ("Book 2:7", "Book 2:3-9", True),
    ("Book 2:7", "Book 2:3-7", True),
    ("Book 2:7", "Book 2:3-6", False),
    ("Book 2:7", "Book 2:7", False),
    ("Book 2:7", "Other Book 2:3-9", False),
    ("Book 2:7", "Book 3:3-9", False),
    ("Book 2", "Book 3", False),
    ("Book 2", "Book 1-3", True),
])
def test_is_ref_in_range(ref, ref_range, expected):
    assert Reference(ref).is_in_range(ref_range) == expected


@pytest.mark.parametrize("link", [
    "https://www.sefaria.org.il/Chofetz_Chaim%2C_Part_One%2C_The_Prohibition_Against_Lashon_Hara%2C_Principle_3.7",
])
def test_to_sefaria_from_sefaria_link(link):
    ref = Reference.from_sefaria_link(link)
    assert ref.is_range() == False
    assert ref.to_sefaria_link() == link

