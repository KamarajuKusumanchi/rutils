#! /usr/bin/env python3

# Script to get urls in a url.

import argparse
import requests
from bs4 import BeautifulSoup
import re


def create_parser():
    parser = argparse.ArgumentParser(
        description='Get urls in a url'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        default=False, dest='verbose',
        help='explain what is being done'
    )
    parser.add_argument(
        'url', action='store',
        help='source url'
    )
    return parser


def get_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [
        x.get('href')
        for x in soup.find_all(name='a', attrs={'href': re.compile('^https*://')})
    ]
    return urls


if __name__ == '__main__':
    # src = sys.argv[1]
    parser = create_parser()
    args = parser.parse_args()
    if args.verbose:
        print(args)

    url = args.url
    urls = get_urls(url)
    for x in urls:
        print(x)
