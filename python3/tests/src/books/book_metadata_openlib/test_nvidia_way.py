"""
tests/src/books/book_metadata_openlib/test_nvidia_way.py

Integration tests for book_metadata_openlib.py — require a network connection
to Open Library. All tests are marked @pytest.mark.integration.

Run all tests:
    pytest tests/src/books/book_metadata_openlib/test_nvidia_way.py -v

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
def test_nvidia_way_returns_latest_english_edition():
    """search_books() should return the latest English edition of The Nvidia Way with all fields correct."""
    df = bmo.search_books(author=None, title="nvidia way")
    row = df.iloc[0]

    assert row["title"] == "Nvidia Way: Jensen Huang and the Making of a Tech Giant"
    assert row["authors"] == ["Tae Kim"]
    assert row["publisher"] == "Norton & Company, Incorporated, W. W."
    assert row["year"] == 2024
    assert row["edition"] is None
    assert row["pages"] == 352
    assert row["isbn"] == "9781324086710"
    assert row["ol_url"] == "https://openlibrary.org/books/OL56894633M"
    assert row["work_url"] == "https://openlibrary.org/works/OL41890401W"
    assert row["amazon_link"] == "https://www.amazon.com/s?k=9781324086710"
