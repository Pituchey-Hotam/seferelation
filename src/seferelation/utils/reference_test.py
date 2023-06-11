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
    ("Book 2:7", "Book 2", True),
])
def test_is_ref_in_range(ref, ref_range, expected):
    assert Reference(ref).is_in_range(ref_range) == expected


@pytest.mark.parametrize("ref, ref_range, expected", [
    ("Berakhot 2b:7", "Berakhot 2b:3-9", True),
    ("Berakhot 5a:3", "Berakhot 5b:3-7", False),
    ("Berakhot 2a:7", "Teanit 2a:3-9", False),
    # ("Berakhot 5a:3", "Berakhot 4b:27-5a7", True), # TODO: not implemented
])
def test_is_ref_in_range_for_gmara(ref, ref_range, expected):
    assert Reference(ref).is_in_range(ref_range) == expected


@pytest.mark.parametrize("ref, ref_parent", [
    ("Book 2:7", "Book 2"),
    ("Book 2:7-9", "Book 2"),
    ("Book 2", "Book 2"),
])
def test_ref_parent(ref, ref_parent):
    assert Reference(ref).parent() == ref_parent

@pytest.mark.parametrize("link", [
    # "https://www.sefaria.org.il/Chofetz_Chaim%2C_Part_One%2C_The_Prohibition_Against_Lashon_Hara%2C_Principle_3.7",
    "https://www.sefaria.org.il/Mishnah_Nedarim.8",
    "https://www.sefaria.org.il/II_Chronicles.16.2-3",
])
def test_to_sefaria_from_sefaria_link(link):
    ref = Reference.from_sefaria_link(link)
    assert ref.to_sefaria_link() == link


@pytest.mark.parametrize("link, ref", [
    ("https://www.sefaria.org.il/Mishnah_Nedarim.8?lang=he", "Mishnah Nedarim 8"),
    ("https://www.sefaria.org.il/II_Chronicles.16.2-3?lang=he", "II Chronicles 16:2-3"),
])
def test_from_sefaria_link(link, ref):
    assert Reference.from_sefaria_link(link).ref == ref


@pytest.mark.parametrize("link, ref", [
    ("https://www.sefaria.org.il/Mishnah_Nedarim.8", "Mishnah Nedarim 8"),
    ("https://www.sefaria.org.il/II_Chronicles.16.2-3", "II Chronicles 16:2-3"),
])
def test_to_sefaria_link(link, ref):
    assert Reference(ref).to_sefaria_link() == link
