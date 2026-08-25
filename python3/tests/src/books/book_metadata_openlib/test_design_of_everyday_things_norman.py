"""
tests/src/books/book_metadata_openlib/test_design_of_everyday_things_norman.py

Regression tests for the renamed-title bug in book_metadata_openlib.py.

Corner case: Open Library work OL1879162W's canonical work-level title is
still "The Psychology of Everyday Things" (Donald Norman's original 1988
title), even though the book has been sold as "The Design of Everyday
Things" since the 2002/2013 editions. get_latest_edition_isbn()'s "match"
tier only matched an edition's title against the *work's* title, so

    book_metadata_openlib.py --title "The Design of Everyday Things" --author Norman

matched the work correctly (via Open Library's full-text search) but then
returned the 1989 "Psychology" edition (ISBN 9780465067091, 272 pages)
instead of a "Design of Everyday Things"-titled edition — because the match
tier is checked before the "any English edition" tier regardless of year,
and the 1989 edition was the only one whose title matched the work's (old)
title.

The fix threads the user's query title into get_latest_edition_isbn() as an
additional match candidate alongside the work's own title, so an edition
matching either name qualifies for the match tier.

The first two tests below are pure unit tests: they monkeypatch get_json()
so they need no network access and run as part of the normal (non
-integration) test suite. The last test is an integration test that
reproduces the exact CLI bug report end-to-end.

Run all tests:
    pytest tests/src/books/book_metadata_openlib/test_design_of_everyday_things_norman.py -v

Skip integration tests (e.g. in CI without network access):
    pytest -m "not integration" -v
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


# ── Fake Open Library editions.json response ────────────────────────────────
# Two editions of the same work: the 1989 original under its original title,
# and a later edition under its renamed title.

_FAKE_EDITIONS_PAGE = {
    "entries": [
        {
            "title": "The Psychology of Everyday Things",
            "publish_date": "1989",
            "isbn_13": ["9780465067091"],
            "physical_format": "Paperback",
        },
        {
            "title": "The Design of Everyday Things (The MIT Press)",
            "publish_date": "2014",
            "isbn_13": ["9780262525671"],
            "physical_format": "Paperback",
        },
    ],
}


# ── Unit tests (no network) ─────────────────────────────────────────────────


def test_get_latest_edition_isbn_prefers_query_title_match(monkeypatch):
    """
    get_latest_edition_isbn() must return the 2014 "Design of Everyday
    Things" edition (9780262525671) when given both the work's own (older,
    renamed) title and the title the user actually searched for — even
    though "The Design of Everyday Things" does not match the work's
    canonical title "The Psychology of Everyday Things".

    Before the fix, only the work's own title was used for match-tier
    matching, so the 1989 edition (9780465067091) would win here instead —
    reproducing the real-world CLI bug.
    """

    def fake_get_json(url, **params):
        assert url.endswith("/editions.json")
        return _FAKE_EDITIONS_PAGE

    monkeypatch.setattr(bmo, "get_json", fake_get_json)

    isbn = bmo.get_latest_edition_isbn(
        "/works/OL1879162W",
        ["The Psychology of Everyday Things", "The Design of Everyday Things"],
    )

    assert isbn == "9780262525671", (
        f"Expected the 2014 'Design of Everyday Things' edition ISBN "
        f"9780262525671, got {isbn!r}. This likely means the query title "
        "is no longer being considered as a match candidate alongside the "
        "work's own (possibly outdated) title."
    )


def test_get_latest_edition_isbn_still_accepts_single_title_string(monkeypatch):
    """
    get_latest_edition_isbn() must remain backward compatible with callers
    (including the other existing tests in this suite) that pass a single
    title string rather than a list of candidate titles.
    """

    def fake_get_json(url, **params):
        return _FAKE_EDITIONS_PAGE

    monkeypatch.setattr(bmo, "get_json", fake_get_json)

    isbn = bmo.get_latest_edition_isbn(
        "/works/OL1879162W", "The Psychology of Everyday Things"
    )

    assert isbn == "9780465067091", (
        "With only the (old) work title as a match candidate, the 1989 "
        "'Psychology of Everyday Things' edition should still win the "
        "match tier -- confirming single-string callers are unaffected by "
        "the fix."
    )


# ── Integration test (network required) ─────────────────────────────────────


@pytest.mark.integration
def test_design_of_everyday_things_end_to_end_returns_2014_mit_edition():
    """
    End-to-end reproduction of the reported bug: searching by the title the
    book is sold under today must return the 2014 MIT Press paperback
    (ISBN 9780262525671), not the 1989 "Psychology of Everyday Things"
    edition of the same Open Library work.
    """
    df = bmo.search_books(author="Norman", title="The Design of Everyday Things")

    assert not df.empty, "Expected at least one result."

    row = df.iloc[0]

    assert row["title"] == "The Design of Everyday Things (The MIT Press)"
    assert row["publisher"] == "The MIT Press"
    assert row["year"] == 2014
    assert row["pages"] == 368
    assert row["isbn"] == "9780262525671"
    assert row["work_url"] == "https://openlibrary.org/works/OL1879162W"