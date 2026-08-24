"""
tests/src/scripts/book_metadata_openlib/test_bash_cookbook_albing.py

Integration tests for book_metadata_openlib.py — require a network connection
to Open Library. All tests are marked @pytest.mark.integration.

Run all tests:
    pytest tests/src/scripts/book_metadata_openlib/test_bash_cookbook_albing.py -v

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

# ── Load module from src/scripts/ ─────────────────────────────────────────────


def _load_module():
    path = Path(__file__).parents[4] / "src" / "books" / "book_metadata_openlib.py"
    spec = importlib.util.spec_from_file_location("book_metadata_openlib", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bmo = _load_module()


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_bash_cookbook_returns_second_edition():
    """search_books() should return the 2017 second edition of the bash Cookbook with all fields correct."""
    df = bmo.search_books(author="albing", title="bash cookbook")
    row = df.iloc[0]

    assert row["title"] == "bash Cookbook: Solutions and Examples for bash Users"
    assert row["authors"] == ["Carl Albing", "JP Vossen"]
    assert row["publisher"] == "O'Reilly Media"
    assert row["year"] == 2017
    assert row["edition"] is None
    assert row["physical_format"] == "paperback; eBook"
    assert row["pages"] == 726
    assert row["isbn"] == "9781491975336"
    assert row["subjects"] == [
        "UNIX (Computer file)",
        "UNIX Shells",
        "User interfaces (Computer systems)",
        "Unix shells (computer programs)",
        "Unix (computer operating system)",
    ]
    assert row["ol_url"] == "https://openlibrary.org/books/OL26834170M"
    assert row["work_url"] == "https://openlibrary.org/works/OL7951526W"
    assert row["amazon_link"] == "https://www.amazon.com/s?k=9781491975336"


@pytest.mark.integration
def test_bash_cookbook_combo_format_beats_older_plain_paperback():
    """
    get_latest_edition_isbn() must return the 2017 second edition (ISBN
    9781491975336), not the 2007 first edition (ISBN 9780596526788).

    Corner case: the 2017 edition's physical_format is the compound string
    "paperback; eBook" (a single OL record covering both a paperback and an
    ebook release), not the bare "Paperback" the 2007 edition uses.
    _classify_format() must recognise the print keyword inside a compound
    format string and classify the edition as "print" — not "ebook" just
    because the string also happens to contain "eBook". Misclassifying it as
    "ebook" would drop it a full priority tier below the plain-"Paperback"
    2007 edition and return the wrong (older, shorter) edition.
    """
    isbn = bmo.get_latest_edition_isbn("/works/OL7951526W", "bash Cookbook")

    assert isbn == "9781491975336", (
        f"Expected the 2017 second edition ISBN 9781491975336, got {isbn!r}. "
        "This likely means a compound physical_format like 'paperback; eBook' "
        "is being misclassified as ebook again and losing to the older, "
        "plain-'Paperback' 2007 first edition (9780596526788)."
    )


@pytest.mark.integration
def test_combine_results_deduplicates_by_isbn():
    """combine_results() should return one row when isbn_book and search_df share the same ISBN."""
    isbn_book = {col: None for col in bmo.COLUMNS}
    isbn_book.update({"isbn": "9781491975336", "year": 2017})

    search_df = bmo.search_books(author="albing", title="bash cookbook")

    results = bmo.combine_results(
        isbn_book=isbn_book,
        search_df=search_df,
        existing_isbns=set(),
        max_results=10,
    )

    assert len(results) == 1
    assert results.iloc[0]["isbn"] == "9781491975336"