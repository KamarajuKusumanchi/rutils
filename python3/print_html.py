#! /usr/bin/env python3

# Script to print the contents of a url.
# This will come in handy if you are trying to parse the contents of a url to
# extract some specific information.

import argparse
import requests
from bs4 import BeautifulSoup

import sys

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
    # I am getting the following error when the output is redirected to a
    # file.
    #   $ print_html.py https://www.python.org/doc/versions/ > ~/x/junk.txt
    #   Traceback (most recent call last):
    #     File 'C:\Users\raju\work\github\rutils\python3\print_html.py', line 29, in <module>
    #       print(content)
    #     File 'C:\Users\raju\.conda\envs\py310\lib\encodings\cp1252.py', line 19, in encode
    #       return codecs.charmap_encode(input,self.errors,encoding_table)[0]
    #   UnicodeEncodeError: 'charmap' codec can't encode character '\u25bc' in position 6443: character maps to <undefined>
    # To fix this, reconfigure stdin and stdout as suggested in
    # https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    content = get_content(url)
    print(content)
