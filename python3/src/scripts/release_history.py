#! /usr/bin/env python3

# tags | script to find the latest python release

import argparse
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def create_parser():
    parser = argparse.ArgumentParser(
        description="Get release history of an application"
    )
    parser.add_argument(
        "application", action="store", help="application name", choices=["python"]
    )
    parser.add_argument(
        "--limit",
        action="store",
        dest="limit",
        help="Limit to last N releases",
        default=None,
    )
    return parser


def fetch_releases():
    print("Fetching Python release history from python.org...")
    # hit the official python.org REST API (/api/v2/downloads/release/) to get up to 200 releases.
    API_URL = "https://www.python.org/api/v2/downloads/release/?format=json&limit=200"
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()
    data = response.json()
    return data


def version_sort_key(v):
    parts = v.split(".")
    return (int(parts[0]), int(parts[1]), parts[2] if len(parts) == 3 else "")


def build_dataframe(releases):
    df = pd.DataFrame(releases)
    df = df[df["show_on_download_page"]][["name", "release_date"]]
    df.columns = ["version", "release_date"]
    df["version"] = df["version"].str.replace("Python ", "", regex=False)
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce").dt.date
    df = df.sort_values(
        by=["version", "release_date"],
        key=lambda s: s.apply(version_sort_key) if s.name == "version" else s,
        ascending=True,
    ).reset_index(drop=True)
    return df


def python_release_history(limit):
    releases = fetch_releases()
    df = build_dataframe(releases)
    if limit:
        df = df.tail(limit).reset_index(drop=True)
    return df


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    application = args.application
    limit = int(args.limit) if args.limit else None
    dispatch = {"python": python_release_history}
    release_history = dispatch[application](limit)
    print(release_history.to_string(index=False))
