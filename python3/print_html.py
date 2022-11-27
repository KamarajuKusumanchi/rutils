#! /usr/bin/env python3

# Script to print the contents of a url.
# This will come in handy if you are trying to parse the contents of a url to
# extract some specific information.

import argparse
import requests
from bs4 import BeautifulSoup


def create_parser():
    parser = argparse.ArgumentParser(description="Print the contents of a url")
    parser.add_argument("url", action="store", help="url to parse")
    return parser


def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    url = args.url
    content = get_content(url)
    print(content)
