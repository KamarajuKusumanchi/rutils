"""
tests/src/books/book_metadata_openlib/test_django_beginners_william_s_vincent.py

Integration tests for book_metadata_openlib.py — require a network connection
to Open Library. All tests are marked @pytest.mark.integration.

Run all tests:
    pytest tests/src/books/book_metadata_openlib/test_django_beginners_william_s_vincent.py -v

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
def test_django_beginners_returns_latest_edition():
    """
    search_books() should return the 2024 edition of Django for Beginners with all fields correct.

    Corner case: the 2024 edition (OL59474729M) has no 'languages' field set in Open Library,
    while an older 2018 edition (OL40867918M) does have '/languages/eng' set explicitly.
    The script must treat a missing languages field as English (not confirmed non-English),
    so that the 2024 edition wins the newest-first comparison rather than being silently
    excluded in favour of the fully-labelled 2018 edition.
    """
    df = bmo.search_books(author="william s. vincent", title="django beginners")
    row = df.iloc[0]

    assert row["title"] == "Django for Beginners: Build Modern Web Applications with Python"
    assert row["authors"] == ["William S. Vincent"]
    assert row["publisher"] == "Still River Press"
    assert row["year"] == 2024
    assert row["edition"] is None
    assert row["isbn"] == "9781735467269"
    assert row["subjects"] == ["Computer software", "Internet"]
    assert row["ol_url"] == "https://openlibrary.org/books/OL59474729M"
    assert row["work_url"] == "https://openlibrary.org/works/OL22297316W"
    assert row["amazon_link"] == "https://www.amazon.com/s?k=9781735467269"
