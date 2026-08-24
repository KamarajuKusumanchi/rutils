"""
tests/src/books/book_metadata_openlib/test_fetch_edition_details_isbn_work_url.py

Integration tests for book_metadata_openlib.py — require a network connection
to Open Library. All tests are marked @pytest.mark.integration.

Run all tests:
    pytest tests/src/books/book_metadata_openlib/test_fetch_edition_details_isbn_work_url.py -v

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
def test_fetch_edition_details_populates_work_url_for_direct_isbn_lookup():
    """
    fetch_edition_details() must populate work_url for ISBN 9780691157245
    (the 2016 Princeton hardcover of Tyson's "Welcome to the Universe: An
    Astrophysical Tour"), so that `--isbn` lookups print a Work URL line the
    same way author/title searches do.

    Corner case: Open Library's jscmd=data response does not reliably include
    a "works" field (see internetarchive/openlibrary#1816), so a direct ISBN
    lookup has no way to derive work_url from that response alone.
    fetch_edition_details() must fall back to fetching the edition's own
    record (/books/OL...M.json), which always includes "works".
    """
    ed = bmo.fetch_edition_details("9780691157245")

    assert ed is not None
    assert ed["work_url"] == "https://openlibrary.org/works/OL17593191W", (
        f"Expected work_url to be populated via the edition-record fallback; "
        f"got {ed['work_url']!r}. This likely means jscmd=data started "
        "including 'works' directly (fine) or the fallback fetch to the "
        "edition's own .json record is missing or broken (not fine)."
    )
    assert ed["physical_format"] == "Hardcover", (
        f"Expected physical_format 'Hardcover' for the print edition; got "
        f"{ed['physical_format']!r}. This likely means the edition-record "
        "fallback used to populate physical_format is missing or broken."
    )