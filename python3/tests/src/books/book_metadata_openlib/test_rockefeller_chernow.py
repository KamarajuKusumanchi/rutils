"""
tests/src/books/book_metadata_openlib/test_rockefeller_chernow.py

Integration tests for book_metadata_openlib.py — require a network connection
to Open Library. All tests are marked @pytest.mark.integration.

Run all tests:
    pytest tests/src/books/book_metadata_openlib/test_rockefeller_chernow.py -v

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
def test_rockefeller_chernow_returns_titan():
    """
    search_books() with author="chernow" and title="rockefeller" should return
    "Titan: The Life of John D. Rockefeller, Sr." as the first result.

    Corner case #1: the book's actual title is "Titan", not "Rockefeller", so the
    query title token "rockefeller" matches only via full-text search across
    subjects and descriptions — not a direct title-field hit.  This works
    correctly with the q="author:chernow title:rockefeller" parameter but
    returned zero results (HTTP 403) when author= and title= were passed as
    separate API parameters.

    Corner case #2: this work has a 2013 Blackstone Audiobooks edition
    (ISBN 9781470882167) alongside the 2004 Vintage Books paperback
    (ISBN 9781400077304). The audiobook is newer, so a year-only "latest
    edition" heuristic picks it over the paperback. get_latest_edition_isbn()
    must prefer the print edition over the audio edition within the match
    tier (see _FORMAT_PRIORITY / _classify_format()), regardless of year.
    """
    df = bmo.search_books(author="chernow", title="rockefeller")

    assert not df.empty, (
        "Expected at least one result for author='chernow' + title='rockefeller'; "
        "got none. Likely regression to the old separate author=/title= params "
        "that trigger a 403 from Open Library."
    )

    row = df.iloc[0]

    assert row["title"] == "Titan: The Life of John D. Rockefeller, Sr."
    assert row["authors"] == ["Ron Chernow"]
    assert row["publisher"] == "Vintage Books"
    assert row["year"] == 2004
    assert row["physical_format"] == "Paperback"
    assert row["pages"] == 832
    assert row["isbn"] == "9781400077304"
    assert row["subjects"] == [
        "Philanthropists",
        "Capitalists and financiers",
        "Industrialists",
        "Biography",
        "Rockefeller, john d. (john davison), 1839-1937",
    ]
    assert row["ol_url"] == "https://openlibrary.org/books/OL8364077M"
    assert row["work_url"] == "https://openlibrary.org/works/OL2665190W"
    assert row["amazon_link"] == "https://www.amazon.com/s?k=9781400077304"
