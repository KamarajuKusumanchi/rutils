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
Results are capped at 7 by default (override with --max-results), deduplicated by work, and printed newest-first.
"""

# changelog:
# * 2026-04-26 initial version is from @claude.
# * 2026-04-26 use editions.sort=publish_date desc so the embedded edition
#              block reflects the latest edition's ISBN, publisher, and year
#              rather than aggregated work-level data (@claude).
# * 2026-04-27 _format_search_doc() now uses fetch_edition_details() as the
#              primary source for all edition-level fields (title, publisher,
#              year, edition name, pages) once an ISBN is known, rather than
#              merging sparse search-response data with Books API fallbacks
#              (@claude).
# * 2026-04-27 refactor lookup_by_isbn() to delegate to fetch_edition_details();
#              expand fetch_edition_details() to return authors, subjects, and
#              ol_url so both callers share a single Books API code path (@claude).
# * 2026-04-27 add --max-results CLI option; replace MAX_RESULTS constant with
#              DEFAULT_MAX_RESULTS and thread the value through search_books()
#              and combine_results() (@claude).
# * 2026-05-09 get_latest_edition_isbn() now tracks best_isbn/best_year across
#              all pages instead of relying on sort=publish_date desc, which OL
#              does not honour reliably (e.g. a 2007 French edition can rank
#              ahead of a 2017 English one). Also replaces nested-editions ISBN
#              resolution in _format_search_doc() with this function (@claude).
# * 2026-05-17 filter editions to English-only (OL language key '/languages/eng')
#              in get_latest_edition_isbn(), with fallback to any-language if no
#              English edition is found.  Also pass language=eng to the search
#              API so the initial candidate set is already English-biased (@claude).
# * 2026-05-17 print both edition URL (/books/OL…) and work URL (/works/OL…)
#              separately. work_url is now a proper COLUMNS member (replacing the
#              temporary _work_url side-channel); fetch_edition_details() derives
#              it from rec["works"][0]["key"]. Edition URL uses the bare OL key
#              with no title slug for stability (@claude).
# * 2026-05-17 fix get_latest_edition_isbn(): treat editions with no languages
#              field as English (missing data, not confirmed non-English); init
#              best_*_year to -1 so undated editions are never silently dropped.
#              Simplify pick_best_isbn() to drop pandas dependency; inline
#              lookup_by_isbn() into fetch_edition_details(); remove redundant
#              combine_results() function; collapse subtitle logic (@claude).
# * 2026-05-25 fix search_books(): replace separate author=/title= params with a
#              single q="author:X title:Y" query string. Open Library's search API
#              returns 403 when author= and title= are passed as independent
#              parameters together; the structured-field q= syntax is accepted and
#              also produces tighter results (e.g. "rockefeller" + "chernow" now
#              finds Titan correctly) (@claude).
# * 2026-05-23 fix get_latest_edition_isbn(): prefer the latest English edition
#              whose title matches the work title (case-insensitive prefix match)
#              over variant titles such as "Body - Illustrated". Editions with no
#              languages field are treated as English (missing data, not confirmed
#              non-English) in all tiers. Explicitly non-English editions only
#              compete in the any-language fallback tier. Restore combine_results()
#              which was removed in the May 17 refactor but is still used by
#              tests. Pass work_title from _format_search_doc() into
#              get_latest_edition_isbn() (@claude).
# * 2026-08-23 fix get_latest_edition_isbn(): within each match tier, prefer
#              non-audio editions (print/ebook) over audio editions regardless
#              of year, so a later audiobook release no longer displaces an
#              earlier print edition of the same work (e.g. Tyson's "Welcome
#              to the Universe: An Astrophysical Tour" was returning the 2018
#              Audible edition instead of the 2016 Princeton hardcover). Audio
#              is only returned as a last resort. Also fix fetch_edition_details():
#              jscmd=data does not reliably include a "works" field, so --isbn
#              lookups were missing Work URL; fall back to fetching the
#              edition's own record (which always has "works") when jscmd=data
#              omits it (@claude).
# * 2026-08-24 add "physical_format" to COLUMNS/output (printed as "Format").
#              fetch_edition_details() now always fetches the edition's own
#              .json record (previously only when work_url was missing) so
#              physical_format is populated reliably. Fix get_latest_edition_isbn():
#              generalise the print/audio split into a 4-way _classify_format()
#              (print > unspecified > ebook > audio); editions with no
#              physical_format on record are no longer treated as equivalent
#              to explicit print editions, since they're sometimes ebook-like
#              scans with no format label (e.g. a 2017 Tyson "Welcome to the
#              Universe" edition with an unset physical_format and a
#              suspiciously low page count was still outranking the 2016
#              hardcover under the previous print-vs-audio-only split) (@claude).
# * 2026-08-24 fix _classify_format(): physical_format can name more than one
#              format for a single edition (e.g. OL's "paperback; eBook" for
#              a combo print/ebook record). Check print keywords before
#              ebook/audio keywords so such a string is classified "print",
#              not "ebook". Previously the 2017 second edition of "bash
#              Cookbook" (ISBN 9781491975336, physical_format "paperback;
#              eBook") was misclassified as ebook on the "ebook" substring
#              alone and lost to the plain 2007 "Paperback" first edition,
#              which is exactly the kind of regression this whole format-tier
#              mechanism was meant to prevent (@claude).

import argparse
import re
import sys
from typing import Optional

import isbnlib
import pandas as pd
import requests

# ── Constants ─────────────────────────────────────────────────────────────────

OL_SEARCH_URL = "https://openlibrary.org/search.json"
OL_BOOKS_URL  = "https://openlibrary.org/api/books"
OL_BASE       = "https://openlibrary.org"

DEFAULT_MAX_RESULTS = 7
TIMEOUT = 12

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "BookSearchScript/1.0 (educational use)"})

COLUMNS = [
    "title",
    "authors",
    "publisher",
    "year",
    "edition",
    "physical_format",
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
    """Return the first valid ISBN-13 from the list, or the first valid ISBN-10."""
    best10 = None
    for raw in isbn_list:
        c = isbnlib.canonical(raw)
        if isbnlib.is_isbn13(c):
            return c
        if not best10 and isbnlib.is_isbn10(c):
            best10 = c
    return best10


def join_title(title: Optional[str], subtitle: Optional[str]) -> Optional[str]:
    if title and subtitle and subtitle not in title:
        return f"{title}: {subtitle}"
    return title or None


def _titles_match(work_title: str, edition_title: str) -> bool:
    """True if the edition title matches the work title (case-insensitive prefix match)."""
    wt = work_title.strip().lower()
    et = edition_title.strip().lower()
    return et == wt or et.startswith(wt + ":") or et.startswith(wt + " ")


_PRINT_FORMAT_KEYWORDS  = (
    "hardcover", "hardback", "paperback", "trade paper", "mass market",
    "spiral", "board book", "library binding", "pamphlet", "leather bound",
    "plastic comb", "loose leaf", "unknown binding", "perfect",
)
_AUDIO_FORMAT_KEYWORDS  = ("audio", "mp3 cd", "playaway", "cassette")
_EBOOK_FORMAT_KEYWORDS  = ("ebook", "e-book", "kindle", "nook", "epub")

# Priority order when choosing between editions of the same match tier: a
# confirmed physical print edition beats one with no format on record, which
# beats a confirmed ebook, which beats a confirmed audio edition.
_FORMAT_PRIORITY = ("print", "unspecified", "ebook", "audio")


def _classify_format(physical_format: str) -> str:
    """
    Classify an OL edition's physical_format string as one of _FORMAT_PRIORITY.

    physical_format can list more than one format for a single edition (e.g.
    OL's "paperback; eBook" for a print/ebook combo record). Print keywords
    are checked first so any edition that names a physical print format is
    classified "print" even if the same string also mentions an ebook or
    audio companion format — the string is naming what the edition *is*,
    not ruling out the other formats it's also available in.

    An empty/missing physical_format is classified "unspecified" rather than
    assumed to be print: some editions with no format on record turn out to
    be ebook-like scans (e.g. an edition with a suspiciously low page count
    and no borrow/preview options), so they shouldn't automatically outrank
    an edition explicitly labelled "Hardcover" or "Paperback" just for being
    newer. They still outrank confirmed ebook/audio editions, since most
    unlabelled editions genuinely are ordinary print books with incomplete
    metadata.
    """
    fmt = (physical_format or "").strip().lower()
    if not fmt:
        return "unspecified"
    if any(kw in fmt for kw in _PRINT_FORMAT_KEYWORDS):
        return "print"
    if any(kw in fmt for kw in _AUDIO_FORMAT_KEYWORDS):
        return "audio"
    if any(kw in fmt for kw in _EBOOK_FORMAT_KEYWORDS):
        return "ebook"
    return "print"


# ── Open Library: edition detail lookup ───────────────────────────────────────


def fetch_edition_details(isbn: str) -> Optional[dict]:
    """
    Fetch all edition-level fields for a single ISBN via the Books API.
    Returns a normalised dict, or None if the ISBN isn't found.
    Handles ISBN-10 → ISBN-13 normalisation internally.
    """
    isbn13 = isbnlib.to_isbn13(isbnlib.canonical(isbn)) or isbn
    data = get_json(OL_BOOKS_URL, bibkeys=f"ISBN:{isbn13}", format="json", jscmd="data")
    if not data:
        return None
    rec = data.get(f"ISBN:{isbn13}")
    if not rec:
        return None

    # jscmd=data does not reliably include "works" or "physical_format" (see
    # internetarchive/openlibrary#1816 for the "works" gap), so a direct ISBN
    # lookup often can't derive them from `rec` alone. Fetch the edition's own
    # record, which always includes both.
    edition_rec = get_json(f"{OL_BASE}{rec['key']}.json") if rec.get("key") else None
    work_url = (
        f"{OL_BASE}{rec['works'][0]['key']}" if rec.get("works")
        else f"{OL_BASE}{edition_rec['works'][0]['key']}"
        if edition_rec and edition_rec.get("works")
        else ""
    )
    physical_format = rec.get("physical_format") or (edition_rec or {}).get("physical_format")

    publishers = rec.get("publishers") or []
    return {
        "title":           join_title(rec.get("title"), rec.get("subtitle")),
        "authors":         [a["name"] for a in rec.get("authors", [])],
        "publisher":       publishers[0].get("name") if publishers else None,
        "year":            extract_year(rec.get("publish_date", "")),
        "edition_name":    rec.get("edition_name"),
        "physical_format": physical_format,
        "pages":           rec.get("number_of_pages"),
        "subjects":        [s["name"] for s in rec.get("subjects", [])][:5],
        # Bare /books/OL…M key — no slugged title — for a stable URL.
        "ol_url":          f"{OL_BASE}{rec['key']}" if rec.get("key") else rec.get("url", ""),
        "work_url":        work_url,
        "isbn13":          isbn13,
    }


# ── Open Library: best edition ISBN for a work ────────────────────────────────


def get_latest_edition_isbn(
    work_key: str,
    work_title: str = "",
) -> Optional[str]:
    """
    Walk all paginated editions for a work and return the best ISBN using
    this priority:
      1. Latest English-or-unlabelled edition whose title matches the work title.
      2. Latest English-or-unlabelled edition (any title).
      3. Latest any-language edition as last resort.

    Editions with no languages field are treated as English (missing data, not
    confirmed non-English). Explicitly non-English editions only compete in tier 3.

    Within each of the three tiers above, editions are further split by
    _classify_format() into _FORMAT_PRIORITY order (print beats unspecified
    beats ebook beats audio), and the latest year wins within that format
    class. A lower-priority format class is only returned when no candidate
    exists in any higher one. Without this, a book's audiobook or ebook
    release — which often comes out a year or two after the original print
    edition — would silently displace the print edition just for being newer
    (e.g. a 2018 audiobook, or an unlabelled 2017 digital scan, outranking a
    2016 hardcover of the same work).

    We don't rely on sort=publish_date desc because OL's ordering is
    unreliable — a 2007 French edition can sort ahead of a 2017 English one.
    """
    url       = f"{OL_BASE}{work_key}/editions.json"
    page_size = 50

    # best[tier][format_class] = (isbn, year)
    best: dict = {
        tier: {fmt_class: (None, -1) for fmt_class in _FORMAT_PRIORITY}
        for tier in ("match", "eng", "any")
    }

    offset = 0
    while True:
        data = get_json(url, limit=page_size, offset=offset)
        if not data:
            break

        for ed in data.get("entries", []):
            isbn = pick_best_isbn(ed.get("isbn_13", []) + ed.get("isbn_10", []))
            if not isbn:
                continue

            year      = extract_year(ed.get("publish_date", "")) or 0
            langs     = [lang.get("key", "") for lang in ed.get("languages", [])]
            # Unlabelled editions (no languages field) are treated as English.
            is_eng    = not langs or any("eng" in k for k in langs)
            matches   = work_title and _titles_match(work_title, ed.get("title", ""))
            fmt_class = _classify_format(ed.get("physical_format", ""))

            if year > best["any"][fmt_class][1]:
                best["any"][fmt_class] = (isbn, year)

            if is_eng and year > best["eng"][fmt_class][1]:
                best["eng"][fmt_class] = (isbn, year)

            if is_eng and matches and year > best["match"][fmt_class][1]:
                best["match"][fmt_class] = (isbn, year)

        if len(data.get("entries", [])) < page_size:
            break
        offset += page_size

    for tier in ("match", "eng", "any"):
        for fmt_class in _FORMAT_PRIORITY:
            isbn, _ = best[tier][fmt_class]
            if isbn:
                return isbn
    return None


# ── Open Library: search ───────────────────────────────────────────────────────


def _format_search_doc(doc: dict) -> Optional[dict]:
    work_key   = doc.get("key", "")
    work_title = doc.get("title", "")
    isbn = get_latest_edition_isbn(work_key, work_title) if work_key else None
    ed   = fetch_edition_details(isbn) if isbn else {}

    # Title: prefer the Books API value (has subtitle merged); fall back to
    # search doc, merging its separate subtitle field if present.
    title = (
        ed.get("title")
        or join_title(doc.get("title"), doc.get("subtitle"))
        or "Unknown Title"
    )

    ol_url   = ed.get("ol_url")   or (f"{OL_BASE}{work_key}" if work_key else "")
    work_url = ed.get("work_url") or (f"{OL_BASE}{work_key}" if work_key else "")

    return {
        "title":           title,
        "authors":         doc.get("author_name", []),
        "publisher":       ed.get("publisher") or "Unknown",
        "year":            ed.get("year") or doc.get("first_publish_year"),
        "edition":         ed.get("edition_name"),
        "physical_format": ed.get("physical_format"),
        "pages":           ed.get("pages"),
        "isbn":            isbn,
        "subjects":        doc.get("subject", [])[:5],
        "ol_url":          ol_url,
        "work_url":        work_url,
        "amazon_link":     amazon_link(isbn) if isbn else None,
    }


def search_books(
    author: Optional[str],
    title: Optional[str],
    max_results: int = DEFAULT_MAX_RESULTS,
) -> pd.DataFrame:
    """Search Open Library by author/title; return one row per work, newest-first."""
    params = {
        "limit":    max_results * 4,
        "fields":   "key,title,subtitle,author_name,subject,first_publish_year",
        "language": "eng",
    }
    q_parts = []
    if author:
        q_parts.append(f"author:{author}")
    if title:
        q_parts.append(f"title:{title}")
    params["q"] = " ".join(q_parts)

    data = get_json(OL_SEARCH_URL, **params)
    if not data or not data.get("docs"):
        return pd.DataFrame(columns=COLUMNS)

    rows = [r for doc in data["docs"] if (r := _format_search_doc(doc))]
    if not rows:
        return pd.DataFrame(columns=COLUMNS)

    df = pd.DataFrame(rows, columns=COLUMNS)
    df["_sort_year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0)
    df = (
        df.sort_values("_sort_year", ascending=False)
        .drop_duplicates(subset=["work_url"])
        .drop(columns=["_sort_year"])
        .head(max_results)
        .reset_index(drop=True)
    )
    return df


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
        if isbn_book.get("isbn"):
            existing_isbns.add(isbn_book["isbn"])

    if not search_df.empty:
        frames.append(search_df[~search_df["isbn"].isin(existing_isbns)])

    if not frames:
        return pd.DataFrame(columns=COLUMNS)

    combined = pd.concat(frames, ignore_index=True)
    combined["_sort_year"] = pd.to_numeric(combined["year"], errors="coerce").fillna(0)
    return (
        combined.sort_values("_sort_year", ascending=False)
        .drop(columns=["_sort_year"])
        .head(max_results)
        .reset_index(drop=True)
    )


# ── Output ────────────────────────────────────────────────────────────────────


def print_book(row: pd.Series, index: int) -> None:
    print(f"\n  [{index}]")
    print(f"  Title       : {row['title']}")
    if row["authors"]:
        print(f"  Author(s)   : {', '.join(row['authors'])}")
    print(f"  Publisher   : {row['publisher']}")
    print(f"  Year        : {int(row['year']) if pd.notna(row['year']) else 'Unknown'}")
    if row["edition"] and pd.notna(row["edition"]):
        print(f"  Edition     : {row['edition']}")
    if row["physical_format"] and pd.notna(row["physical_format"]):
        print(f"  Format      : {row['physical_format']}")
    if pd.notna(row["pages"]) and row["pages"]:
        print(f"  Pages       : {int(row['pages'])} (this edition)")
    if row["isbn"]:
        print(f"  ISBN-13     : {row['isbn']}")
    if row["subjects"]:
        print(f"  Subjects    : {', '.join(str(s) for s in row['subjects'])}")
    if row["ol_url"]:
        print(f"  Edition URL : {row['ol_url']}")
    if row["work_url"]:
        print(f"  Work URL    : {row['work_url']}")
    print(f"  Amazon      : {row['amazon_link'] or '(no ISBN available)'}")


# ── CLI ────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="book_metadata_openlib.py",
        description=(
            "Search Open Library for books by ISBN, author, and/or title.\n"
            "Partial strings are accepted for author and title.\n"
            f"Up to {DEFAULT_MAX_RESULTS} results are shown — one (latest) edition per work,\n"
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
    p.add_argument("--isbn",   metavar="ISBN",   help="ISBN-10 or ISBN-13 (hyphens optional)")
    p.add_argument("--author", metavar="AUTHOR", help="Author name or partial name")
    p.add_argument("--title",  metavar="TITLE",  help="Book title or partial title")
    p.add_argument(
        "--max-results",
        metavar="N",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=f"Maximum number of results to display (default: {DEFAULT_MAX_RESULTS})",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()

    if not any([args.isbn, args.author, args.title]):
        build_parser().print_help()
        sys.exit(1)

    frames: list[pd.DataFrame] = []
    seen_isbns: set[str] = set()

    # ── ISBN direct lookup ─────────────────────────────────────────────────
    if args.isbn:
        print(f"\nLooking up ISBN {args.isbn} …")
        clean = isbnlib.canonical(args.isbn)
        if not (isbnlib.is_isbn10(clean) or isbnlib.is_isbn13(clean)):
            print(f"  '{args.isbn}' does not look like a valid ISBN.", file=sys.stderr)
        else:
            isbn13 = isbnlib.to_isbn13(clean) or clean
            ed = fetch_edition_details(isbn13)
            if not ed or not ed.get("title"):
                print("  No book found for that ISBN.")
            else:
                row = {
                    "title":           ed["title"],
                    "authors":         ed["authors"],
                    "publisher":       ed["publisher"] or "Unknown",
                    "year":            ed["year"],
                    "edition":         ed["edition_name"],
                    "physical_format": ed["physical_format"],
                    "pages":           ed["pages"],
                    "isbn":            isbn13,
                    "subjects":        ed["subjects"],
                    "ol_url":          ed["ol_url"],
                    "work_url":        ed["work_url"],
                    "amazon_link":     amazon_link(isbn13),
                }
                frames.append(pd.DataFrame([row], columns=COLUMNS))
                seen_isbns.add(isbn13)

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
        else:
            frames.append(search_df[~search_df["isbn"].isin(seen_isbns)])

    # ── Merge, sort, display ───────────────────────────────────────────────
    if not frames:
        print("\nNo books found.")
        sys.exit(0)

    results = pd.concat(frames, ignore_index=True)
    results["_sort_year"] = pd.to_numeric(results["year"], errors="coerce").fillna(0)
    results = (
        results.sort_values("_sort_year", ascending=False)
        .drop(columns=["_sort_year"])
        .head(args.max_results)
        .reset_index(drop=True)
    )

    sep = "═" * 64
    print(f"\n{sep}")
    print(f"  {len(results)} result(s) — latest edition per work, newest first")
    print(sep)
    for i, (_, row) in enumerate(results.iterrows(), start=1):
        print(f"\n{sep}")
        print_book(row, i)
    print(f"\n{sep}")


if __name__ == "__main__":
    main()