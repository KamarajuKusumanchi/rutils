"""
tests/src/books/book_metadata_openlib/test_the_body_bill_bryson.py

Integration tests for book_metadata_openlib.py — require a network connection
to Open Library. All tests are marked @pytest.mark.integration.

Run all tests:
    pytest tests/src/books/book_metadata_openlib/test_the_body_bill_bryson.py -v

Run only integration tests:
    pytest -m integration -v

Skip integration tests (e.g. in CI without network access):
    pytest -m "not integration" -v

To register the marker and avoid PytestUnknownMarkWarning, add this to pytest.ini:
    [pytest]
    markers =
        integration: marks tests that require a network connection
"""

import importlib.util
from pathlib import Path

import pytest

# ── Load module from src/books/ ───────────────────────────────────────────────


def _load_module():
    path = Path(__file__).parents[4] / "src" / "books" / "book_metadata_openlib.py"
    spec = importlib.util.spec_from_file_location("book_metadata_openlib", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bmo = _load_module()


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_the_body_bryson_returns_anchor_edition():
    """
    search_books() should return the 2021 Anchor Books edition of The Body as
    the second result (after "Really Short Journey Through the Body").

    Corner case: the work has a 2022 illustrated edition ("Body - Illustrated")
    that is newer but should be demoted because its title does not match the
    work title "The Body". The title-match tier in get_latest_edition_isbn()
    must prefer the 2021 plain-titled Anchor Books edition over it.
    """
    df = bmo.search_books(author="bill bryson", title="the body")
    row = df.iloc[1]

    assert row["title"] == "The Body: A Guide for Occupants"
    assert row["authors"] == ["Bill Bryson"]
    assert row["publisher"] == "Anchor Books"
    assert row["year"] == 2021
    assert row["edition"] is None
    assert row["pages"] == 464
    assert row["isbn"] == "9780804172721"
    assert row["subjects"] == [
        "Human anatomy",
        "Human physiology",
        "Anatomy",
        "SCIENCE / Life Sciences / Human Anatomy & Physiology",
        "MEDICAL / Anatomy",
    ]
    assert row["ol_url"] == "https://openlibrary.org/books/OL31835238M"
    assert row["work_url"] == "https://openlibrary.org/works/OL20333471W"
    assert row["amazon_link"] == "https://www.amazon.com/s?k=9780804172721"
