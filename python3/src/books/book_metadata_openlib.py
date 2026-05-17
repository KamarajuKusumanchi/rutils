#!/usr/bin/env python3
"""
book_metadata_openlib.py — Fetch book details by ISBN, author, or title using Open Library.

Dependencies:
    pip install requests isbnlib pandas

Usage:
    python book_metadata_openlib.py --isbn 9780132350884
    python book_metadata_openlib.py --author "Robert Martin"
    python book_metadata_openlib.py --title "Clean Code"
    python book_metadata_openlib.py --author "Martin" --title "Clean"
    python book_metadata_openlib.py --author "tolkien" --title "rings"

Options can be combined. Author and title accept partial strings.
Results are capped at 10 by default (override with --max-results), deduplicated by work, and printed newest-first.
"""

# changelog:
# * 2026-05-17 print both edition URL (/books/OL…) and work URL (/works/OL…)
#              separately. work_url is now a proper COLUMNS member (replacing the
#              temporary _work_url side-channel); fetch_edition_details() derives
#              it from rec["works"][0]["key"]. Edition URL uses the bare OL key
#              with no title slug for stability (@claude).
# * 2026-05-17 filter editions to English-only (OL language key '/languages/eng')
#              in get_latest_edition_isbn(), with fallback to any-language if no
#              English edition is found.  Also pass language=eng to the search
#              API so the initial candidate set is already English-biased (@claude).
# * 2026-05-09 get_latest_edition_isbn() now tracks best_isbn/best_year across
#              all pages instead of relying on sort=publish_date desc, which OL
#              does not honour reliably (e.g. a 2007 French edition can rank
#              ahead of a 2017 English one). Also replaces nested-editions ISBN
#              resolution in _format_search_doc() with this function (@claude).
# * 2026-04-27 add --max-results CLI option; replace MAX_RESULTS constant with
#              DEFAULT_MAX_RESULTS and thread the value through search_books()
#              and combine_results() (@claude).
# * 2026-04-27 refactor lookup_by_isbn() to delegate to fetch_edition_details();
#              expand fetch_edition_details() to return authors, subjects, and
#              ol_url so both callers share a single Books API code path (@claude).
# * 2026-04-27 _format_search_doc() now uses fetch_edition_details() as the
#              primary source for all edition-level fields (title, publisher,
#              year, edition name, pages) once an ISBN is known, rather than
#              merging sparse search-response data with Books API fallbacks
#              (@claude).
# * 2026-04-26 use editions.sort=publish_date desc so the embedded edition
#              block reflects the latest edition's ISBN, publisher, and year
#              rather than aggregated work-level data (@claude).
# * 2026-04-26 initial version is from @claude.

import argparse
import re
import sys
from typing import Optional

import isbnlib
import pandas as pd
import requests

# ── Constants ─────────────────────────────────────────────────────────────────

OL_SEARCH_URL = "https://openlibrary.org/search.json"
OL_BOOKS_URL = "https://openlibrary.org/api/books"
OL_BASE = "https://openlibrary.org"

DEFAULT_MAX_RESULTS = 7
TIMEOUT = 12
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "BookSearchScript/1.0 (educational use)"})

# Columns present in every book record (keeps DataFrame shape consistent)
COLUMNS = [
    "title",
    "authors",
    "publisher",
    "year",
    "edition",
    "pages",
    "isbn",
    "subjects",
    "ol_url",
    "work_url",
    "amazon_link",
]


# ── HTTP helper ────────────────────────────────────────────────────────────────


def get_json(url: str, **params) -> Optional[dict]:
    """GET a URL with optional query params; return parsed JSON or None."""
    try:
        r = SESSION.get(url, params=params or None, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.HTTPError as exc:
        print(f"  [HTTP {exc.response.status_code}] {url}", file=sys.stderr)
    except requests.RequestException as exc:
        print(f"  [Request error] {exc}", file=sys.stderr)
    return None


# ── Helpers ────────────────────────────────────────────────────────────────────


def extract_year(date_str: str) -> Optional[int]:
    m = re.search(r"\d{4}", str(date_str))
    return int(m.group()) if m else None


def amazon_link(isbn: str) -> str:
    return f"https://www.amazon.com/s?k={isbnlib.canonical(isbn)}"


def pick_best_isbn(isbn_list: list) -> Optional[str]:
    """
    From a raw list of ISBN strings, return a valid ISBN-13 if one exists,
    otherwise the first valid ISBN-10.  Uses a pandas Series for filtering.
    """
    s = pd.Series(isbn_list, dtype=str).map(isbnlib.canonical).dropna()
    s = s[s != ""]
    isbn13 = s[s.map(isbnlib.is_isbn13)]
    if not isbn13.empty:
        return isbn13.iloc[0]
    isbn10 = s[s.map(isbnlib.is_isbn10)]
    return isbn10.iloc[0] if not isbn10.empty else None


# ── Open Library: ISBN lookup ──────────────────────────────────────────────────


def lookup_by_isbn(isbn: str) -> Optional[dict]:
    """Validate isbn, normalise to ISBN-13, then delegate to fetch_edition_details."""
    clean = isbnlib.canonical(isbn)
    if not (isbnlib.is_isbn10(clean) or isbnlib.is_isbn13(clean)):
        print(f"  '{isbn}' does not look like a valid ISBN.", file=sys.stderr)
        return None

    isbn13 = isbnlib.to_isbn13(clean) or clean
    ed = fetch_edition_details(isbn13)
    if not ed["title"]:
        return None

    return {
        "title": ed["title"],
        "authors": ed["authors"],
        "publisher": ed["publisher"] or "Unknown",
        "year": ed["year"],
        "edition": ed["edition_name"],
        "pages": ed["pages"],
        "isbn": isbn13,
        "subjects": ed["subjects"],
        "ol_url": ed["ol_url"],
        "work_url": ed["work_url"],
        "amazon_link": amazon_link(isbn13),
    }


# ── Open Library: edition detail lookup ───────────────────────────────────────


def fetch_edition_details(isbn: str) -> dict:
    """
    Fetch all edition-level fields for a single ISBN via the Books API.
    Returns a dict with normalised values (None when absent).
    Used by _format_search_doc() as the authoritative source for edition data
    once we have an ISBN, rather than piecing things together from the search
    response's sparse nested edition block.
    """
    empty = {
        "title": None,
        "authors": [],
        "publisher": None,
        "year": None,
        "edition_name": None,
        "pages": None,
        "subjects": [],
        "ol_url": "",
        "work_url": "",
    }
    # Always use ISBN-13 so the bibkey and response key match reliably.
    isbn13 = isbnlib.to_isbn13(isbnlib.canonical(isbn)) or isbn
    data = get_json(OL_BOOKS_URL, bibkeys=f"ISBN:{isbn13}", format="json", jscmd="data")
    if not data:
        return empty
    rec = data.get(f"ISBN:{isbn13}", {})
    if not rec:
        return empty

    title = rec.get("title")
    subtitle = rec.get("subtitle")
    if title and subtitle:
        title = f"{title}: {subtitle}"

    publishers = rec.get("publishers") or []
    return {
        "title": title,
        "authors": [a["name"] for a in rec.get("authors", [])],
        "publisher": publishers[0].get("name") if publishers else None,
        "year": extract_year(rec.get("publish_date", "")),
        "edition_name": rec.get("edition_name"),
        "pages": rec.get("number_of_pages"),
        "subjects": [s["name"] for s in rec.get("subjects", [])][:5],
        # Use the bare /books/OL…M key rather than the slugged "url" field
        # (e.g. /books/OL56894633M instead of /books/OL56894633M/Nvidia_Way).
        "ol_url": f"{OL_BASE}{rec['key']}" if rec.get("key") else rec.get("url", ""),
        # Work URL from the embedded works list (e.g. /works/OL41890401W).
        "work_url": (
            f"{OL_BASE}{rec['works'][0]['key']}"
            if rec.get("works")
            else ""
        ),
    }


# ── Open Library: latest edition ISBN for a work ──────────────────────────────


def get_latest_edition_isbn(work_key: str) -> Optional[str]:
    """
    Walk all paginated editions for a work and return the ISBN belonging to
    the newest English-language edition.

    Language filtering: editions are kept only when their 'languages' list
    contains '/languages/eng' (Open Library's key for English).  Editions
    with no language field are treated as non-English and skipped so that
    ambiguous records don't crowd out confirmed English ones.  If no English
    edition with an ISBN is found, we fall back to the newest edition of any
    language rather than returning nothing.

    We do not rely on sort=publish_date desc because OL's ordering is
    unreliable in practice — translations and poorly dated records can sort
    ahead of newer editions (e.g. a 2007 French edition outranking a 2017
    English one). Instead we track the best ISBN ourselves across all pages.
    """
    url = f"{OL_BASE}{work_key}/editions.json"
    page_size = 50  # maximum OL allows per request
    offset = 0
    best_eng_isbn: Optional[str] = None
    best_eng_year: int = 0
    best_any_isbn: Optional[str] = None
    best_any_year: int = 0

    while True:
        data = get_json(url, limit=page_size, offset=offset)
        if not data:
            break

        for ed in data.get("entries", []):
            isbn = pick_best_isbn(ed.get("isbn_13", []) + ed.get("isbn_10", []))
            if not isbn:
                continue

            year = extract_year(ed.get("publish_date", "")) or 0

            # Track best across all languages (fallback)
            if year > best_any_year:
                best_any_year = year
                best_any_isbn = isbn

            # Check for English: OL stores languages as a list of dicts
            # e.g. [{"key": "/languages/eng"}]
            langs = [
                lang.get("key", "") for lang in ed.get("languages", [])
            ]
            is_english = any("eng" in k for k in langs)
            if is_english and year > best_eng_year:
                best_eng_year = year
                best_eng_isbn = isbn

        # Stop if this page was the last one
        if len(data.get("entries", [])) < page_size:
            break
        offset += page_size

    # Prefer the best English edition; fall back to best of any language
    return best_eng_isbn or best_any_isbn


# ── Open Library: search ───────────────────────────────────────────────────────


def search_books(
    author: Optional[str], title: Optional[str], max_results: int = DEFAULT_MAX_RESULTS
) -> pd.DataFrame:
    """
    Search Open Library by author/title; return results as a DataFrame.
    Each row is one work (latest edition), deduped and sorted newest-first.
    """
    params = {
        "limit": max_results * 4,
        "fields": "key,title,subtitle,author_name,subject,first_publish_year",
        "language": "eng",  # restrict search results to English editions
    }
    if author:
        params["author"] = author
    if title:
        params["title"] = title

    data = get_json(OL_SEARCH_URL, **params)
    if not data or not data.get("docs"):
        return pd.DataFrame(columns=COLUMNS)

    rows = [_format_search_doc(doc) for doc in data["docs"]]
    rows = [r for r in rows if r]  # drop None entries

    df = pd.DataFrame(rows, columns=COLUMNS)

    # ── Deduplicate: one row per Open Library work key ─────────────────────
    # Deduplicate on work_url (stable work identifier) so two editions of the
    # same work aren't both shown, even though ol_url now points to the edition.
    df["_sort_year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0)
    df = (
        df.sort_values("_sort_year", ascending=False)
        .drop_duplicates(subset=["work_url"])
        .drop(columns=["_sort_year"])
        .head(max_results)
    )

    return df


def _format_search_doc(doc: dict) -> Optional[dict]:
    work_key = doc.get("key", "")

    # ── Resolve the latest edition's ISBN via the dedicated editions endpoint ──
    # The search response's nested editions block is sparse and its sort order
    # is unreliable, so we query the work's editions directly, walking all pages
    # newest-first, and take the first ISBN we find.
    isbn = get_latest_edition_isbn(work_key) if work_key else None

    # ── Fetch all edition-level fields directly from the Books API ─────────
    ed = fetch_edition_details(isbn) if isbn else {}

    title = ed.get("title") or doc.get("title", "Unknown Title")
    subtitle = doc.get("subtitle")
    if subtitle and subtitle not in title:
        title = f"{title}: {subtitle}"

    # Prefer the edition-level URL from the Books API (e.g. /books/OL56894633M)
    # so the link points directly to the specific edition, not the work overview.
    # Fall back to the work URL if the Books API didn't return one.
    edition_url = ed.get("ol_url") or (f"{OL_BASE}{work_key}" if work_key else "")
    # Work URL: prefer the one resolved from the Books API (which may differ
    # from the search-doc key); fall back to building it from the search key.
    work_url = ed.get("work_url") or (f"{OL_BASE}{work_key}" if work_key else "")

    return {
        "title": title,
        "authors": doc.get("author_name", []),
        "publisher": ed.get("publisher") or "Unknown",
        "year": ed.get("year") or doc.get("first_publish_year"),
        "edition": ed.get("edition_name"),
        "pages": ed.get("pages"),
        "isbn": isbn,
        "subjects": doc.get("subject", [])[:5],
        "ol_url": edition_url,
        "work_url": work_url,
        "amazon_link": amazon_link(isbn) if isbn else None,
    }


# ── Merge & sort all results ──────────────────────────────────────────────────


def combine_results(
    isbn_book: Optional[dict],
    search_df: pd.DataFrame,
    existing_isbns: set,
    max_results: int = DEFAULT_MAX_RESULTS,
) -> pd.DataFrame:
    """
    Merge the optional ISBN lookup result with the search DataFrame,
    drop duplicates by ISBN, and sort newest-first.
    """
    frames = []

    if isbn_book:
        frames.append(pd.DataFrame([isbn_book], columns=COLUMNS))
        if isbn_book["isbn"]:
            existing_isbns.add(isbn_book["isbn"])

    if not search_df.empty:
        # Drop rows whose ISBN was already added by the --isbn lookup
        filtered = search_df[~search_df["isbn"].isin(existing_isbns)]
        frames.append(filtered)

    if not frames:
        return pd.DataFrame(columns=COLUMNS)

    combined = pd.concat(frames, ignore_index=True)

    # Sort newest-first; unknown years go to the bottom
    combined["_sort_year"] = pd.to_numeric(combined["year"], errors="coerce").fillna(0)
    combined = (
        combined.sort_values("_sort_year", ascending=False)
        .drop(columns=["_sort_year"])
        .head(max_results)
        .reset_index(drop=True)
    )

    return combined


# ── Output ────────────────────────────────────────────────────────────────────


def print_book(row: pd.Series, index: int) -> None:
    print(f"\n  [{index}]")
    print(f"  Title       : {row['title']}")

    authors = row["authors"]
    if authors:
        print(f"  Author(s)   : {', '.join(authors)}")
    print(f"  Publisher   : {row['publisher']}")
    print(f"  Year        : {int(row['year']) if pd.notna(row['year']) else 'Unknown'}")
    if row["edition"] and pd.notna(row["edition"]):
        print(f"  Edition     : {row['edition']}")
    if pd.notna(row["pages"]) and row["pages"]:
        print(f"  Pages       : {int(row['pages'])} (this edition)")
    if row["isbn"]:
        print(f"  ISBN-13     : {row['isbn']}")
    subjects = row["subjects"]
    if subjects:
        print(f"  Subjects    : {', '.join(str(s) for s in subjects)}")
    if row["ol_url"]:
        print(f"  Edition URL : {row['ol_url']}")
    if row["work_url"]:
        print(f"  Work URL    : {row['work_url']}")
    if row["amazon_link"]:
        print(f"  Amazon      : {row['amazon_link']}")
    else:
        print("  Amazon      : (no ISBN available)")


# ── CLI ────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="book_metadata_openlib.py",
        description=(
            "Search Open Library for books by ISBN, author, and/or title.\n"
            "Partial strings are accepted for author and title.\n"
            "Up to 10 results are shown — one (latest) edition per work,\n"
            "printed in reverse chronological order."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --isbn 9780132350884\n"
            "  %(prog)s --author 'Robert Martin'\n"
            "  %(prog)s --title 'Clean Code'\n"
            "  %(prog)s --author 'tolkien' --title 'rings'\n"
            "  %(prog)s --author 'hawking' --title 'brief history'\n"
        ),
    )
    p.add_argument(
        "--isbn", metavar="ISBN", help="ISBN-10 or ISBN-13 (hyphens optional)"
    )
    p.add_argument("--author", metavar="AUTHOR", help="Author name or partial name")
    p.add_argument("--title", metavar="TITLE", help="Book title or partial title")
    p.add_argument(
        "--max-results",
        metavar="N",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=f"Maximum number of results to display (default: {DEFAULT_MAX_RESULTS})",
    )
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not any([args.isbn, args.author, args.title]):
        parser.print_help()
        sys.exit(1)

    isbn_book = None
    search_df = pd.DataFrame(columns=COLUMNS)
    seen_isbns: set = set()

    # ── ISBN direct lookup ─────────────────────────────────────────────────
    if args.isbn:
        print(f"\nLooking up ISBN {args.isbn} …")
        isbn_book = lookup_by_isbn(args.isbn)
        if not isbn_book:
            print("  No book found for that ISBN.")

    # ── Author / title search ──────────────────────────────────────────────
    if args.author or args.title:
        parts = []
        if args.author:
            parts.append(f'author="{args.author}"')
        if args.title:
            parts.append(f'title="{args.title}"')
        print(f"\nSearching Open Library for {' + '.join(parts)} …")
        search_df = search_books(
            author=args.author, title=args.title, max_results=args.max_results
        )
        if search_df.empty:
            print("  No results found.")

    # ── Merge, dedup, sort ─────────────────────────────────────────────────
    results = combine_results(
        isbn_book, search_df, seen_isbns, max_results=args.max_results
    )

    if results.empty:
        print("\nNo books found.")
        sys.exit(0)

    print(f"\n{'═' * 64}")
    print(f"  {len(results)} result(s) — latest edition per work, newest first")
    print(f"{'═' * 64}")

    print(f"\n{'═' * 64}")
    for i, (_, row) in enumerate(results.iterrows(), start=1):
        print_book(row, i)

    print(f"\n{'═' * 64}")


if __name__ == "__main__":
    main()
