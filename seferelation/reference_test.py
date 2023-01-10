import pytest

from .sheet_parser import _is_ref_in_range


@pytest.mark.parametrize("ref, ref_range, expected", [
    ("Book 2:7", "Book 2:3-9", True),
    ("Book 2:7", "Book 2:3-7", True),
    ("Book 2:7", "Book 2:3-6", False),
    ("Book 2:7", "Book 2:7", False),
    ("Book 2:7", "Other Book 2:3-9", False),
    ("Book 2:7", "Book 3:3-9", False),
])
def test_is_ref_in_range(ref, ref_range, expected):
    assert _is_ref_in_range(ref, ref_range) == expected

