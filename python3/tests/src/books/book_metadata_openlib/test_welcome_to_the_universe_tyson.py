"""
tests/src/books/book_metadata_openlib/test_welcome_to_the_universe_tyson.py

Integration tests for book_metadata_openlib.py — require a network connection
to Open Library. All tests are marked @pytest.mark.integration.

Run all tests:
    pytest tests/src/books/book_metadata_openlib/test_welcome_to_the_universe_tyson.py -v

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
def test_welcome_to_the_universe_tyson_prefers_print_over_later_audiobook():
    """
    get_latest_edition_isbn() for work OL17593191W ("Welcome to the Universe:
    An Astrophysical Tour" by Neil deGrasse Tyson) must return the 2016
    Princeton University Press hardcover (ISBN 9780691157245), not the 2018
    Audible Studios audiobook edition (ISBN 9781978605053) of the same work.

    Corner case: the audiobook edition was published two years after the
    hardcover, so a year-only "latest edition" heuristic picks the audiobook
    over the print edition. get_latest_edition_isbn() must prefer a print
    edition over an audio edition within each match tier (see
    _FORMAT_PRIORITY), falling back to audio only when no better-ranked
    format exists.
    """
    isbn = bmo.get_latest_edition_isbn(
        "/works/OL17593191W", "Welcome to the Universe: An Astrophysical Tour"
    )

    assert isbn == "9780691157245", (
        f"Expected the print hardcover ISBN 9780691157245, got {isbn!r}. "
        "This likely means the print-over-audio format preference regressed "
        "and the 2018 Audible audiobook edition (9781978605053) is being "
        "picked again just because it has a later publish year."
    )


@pytest.mark.integration
def test_welcome_to_the_universe_tyson_prefers_print_over_unspecified_format():
    """
    get_latest_edition_isbn() must also prefer the 2016 hardcover (ISBN
    9780691157245) over the 2017 Princeton edition (ISBN 9781400888993),
    even though the 2017 edition is newer.

    Corner case: OL29765874M (ISBN 9781400888993) has no physical_format on
    record at all — not "Hardcover", not "Ebook", nothing — and a
    suspiciously low page count (264, vs. 472 for the hardcover), suggesting
    it's an ebook-like scan with incomplete metadata rather than a genuine
    second print run. _classify_format() must bucket editions with no
    physical_format as "unspecified" rather than silently treating them as
    equivalent to an explicitly-labelled print edition, or this edition
    would win the "match" tier on year alone and displace the real hardcover.
    """
    isbn = bmo.get_latest_edition_isbn(
        "/works/OL17593191W", "Welcome to the Universe: An Astrophysical Tour"
    )

    assert isbn == "9780691157245", (
        f"Expected the print hardcover ISBN 9780691157245, got {isbn!r}. "
        "This likely means an edition with no physical_format on record "
        "(e.g. 9781400888993) is being treated as equal to an explicit "
        "print edition and winning on year alone."
    )


@pytest.mark.integration
def test_welcome_to_the_universe_tyson_search_also_prefers_print():
    """
    End-to-end check: search_books(author="tyson", title="welcome universe
    astrophysical") must surface the 2016 print edition of "Welcome to the
    Universe: An Astrophysical Tour", not a later audiobook or
    unspecified-format edition, confirming the fix in
    get_latest_edition_isbn() is actually reflected in search results.
    """
    df = bmo.search_books(author="tyson", title="welcome universe astrophysical")

    row = df.iloc[0]

    assert row["title"] == "Welcome to the Universe: An Astrophysical Tour"
    assert row["publisher"] == "Princeton University Press"
    assert row["year"] == 2016
    assert row["physical_format"] == "Hardcover"
    assert row["pages"] == 472
    assert row["isbn"] == "9780691157245"
    assert row["ol_url"] == "https://openlibrary.org/books/OL26196435M"
    assert row["work_url"] == "https://openlibrary.org/works/OL17593191W"
    assert row["amazon_link"] == "https://www.amazon.com/s?k=9780691157245"