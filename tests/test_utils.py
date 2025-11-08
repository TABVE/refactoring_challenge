# tests/test_utils.py
from __future__ import annotations

from datetime import date
import io
import pytest

from legacy_code.utils import (
    parse_date,
    read_csv_as_dicts,
)


@pytest.mark.parametrize(
    "text",
    [
        "2024/01/02",
        "2024-01-02",
        " 2024-1-2 ",  # Whitespace and single-digit month/day should be handled.
    ],
)
def test_parse_date_slash(text):
    """Parse date with slashes."""
    got = parse_date(text)
    assert got == date(2024, 1, 2)


@pytest.mark.parametrize(
    "bad_text",
    [
        "20240102",  # no separators
        "not-a-date",
        "",  # empty
    ],
)
def test_parse_date_invalid_format_raises(bad_text):
    """Malformed date strings should raise ValueError."""
    with pytest.raises(ValueError):
        parse_date(bad_text)


def test_parse_date_invalid_components_raises():
    """Impossible date components should raise ValueError (e.g., month 13)."""
    with pytest.raises(ValueError):
        parse_date("2024-13-01")


def test_read_csv_as_dicts_strips_keys_and_values(tmp_path):
    """read_csv_as_dicts should return list of dicts with stripped keys and values."""
    p = tmp_path / "dicts.csv"
    p.write_text(" x , y \n 1 , 2 \n3,4\n", encoding="utf-8")
    dicts = read_csv_as_dicts(str(p))
    assert dicts == [{"x": "1", "y": "2"}, {"x": "3", "y": "4"}]
