#! /usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
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


def python_release_history(limit):
    # If you want to experiment, use public/sandbox/jupytext/python_release_history.py
    url = "https://www.python.org/doc/versions/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # We want to parse lines such as
    # <div class="section" id="python-documentation-by-version">
    # ...
    # <li><a class="reference external" href="https://docs.python.org/release/3.11.0/">Python 3.11.0</a>, documentation released on 24 October 2022.</li>
    # ...
    # </div>
    div = soup.find("div", attrs={"id": "python-documentation-by-version"})
    release_data = []
    for link in div.findAll("li"):
        # Sample output:
        # link = '<li><a class="reference external" href="https://docs.python.org/release/3.11.0/">Python 3.11.0</a>, documentation released on 24 October 2022.</li>'
        # x.contents = ['Python 3.11.0']
        # release_tag = '3.11.0'
        # y = ', documentation released on 24 October 2022.'
        # s = '24 October 2022'
        # release_date = '2022-10-24'
        x = link.find("a", attrs={"href": re.compile("^https*://")})
        matches = re.search("Python (.*)$", x.contents[0])
        release_tag = matches.group(1)
        y = link.contents[1].replace("\n", " ")
        matches = re.search(", documentation released on (\d* .* \d*)\.?$", y)
        s = matches.group(1)
        release_date = datetime.strptime(s, "%d %B %Y").date()
        # release_date = datetime.strptime(s, "%d %B %Y")
        release_data.append((release_date, release_tag))
        # if limit and len(release_data) >= limit:
        #     break
    releases = pd.DataFrame(release_data, columns=["date", "tag"])
    if limit:
        releases = releases.loc[: limit - 1, :]
    return releases


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    application = args.application
    limit = int(args.limit) if args.limit else None
    dispatch = {"python": python_release_history}
    release_history = dispatch[application](limit)
    print(release_history.to_string(index=False))
