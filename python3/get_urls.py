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
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises HTTPError for 4xx/5xx responses
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print('encountered exception:')
            print(e)
            retry_after = response.headers.get('Retry-After', 'unknown')
            print(f'Rate limited (429), Retry after: {retry_after}s')
    except requests.exceptions.SSLError as e:
        # handle exceptions such as
        # requests.exceptions.SSLError: HTTPSConnectionPool(host='news.ycombinator.com', port=443): Max retries
        # exceeded with url: /item?id=25271676 (Caused by SSLError(SSLCertVerificationError(1,
        # '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
        # (_ssl.c:1006)')))
        print('encountered exception:')
        print(e)
        print('disabling SSL and trying again.')
        response = requests.get(url, verify=False)

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
