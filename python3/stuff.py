#! /usr/bin/env python3

""" Print a file after removing comments and empty lines. If file is not
specified, input is read from stdin.

Usage:
stuff.py filename

Sample usage:
% stuff.py /etc/apt/sources.list
% cat /etc/apt/sources.list | stuff.py
% stuff.py < /etc/apt/sources.list
"""

import argparse
import re
import sys


def compact_print(fname, comment_pattern):
    empty_pattern = r"^\s*$"

    using_stdin = fname is None
    if (using_stdin):
        fh = sys.stdin
    else:
        fh = open(fname)

    for line in fh:
        line = line.rstrip()
        if re.search(comment_pattern, line):
            continue
        elif re.search(empty_pattern, line):
            continue
        else:
            print(line)

    if (not using_stdin):
        fh.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Print a file after removing comments and
        empty lines. If file is not specified, input is read from stdin.''')
    parser.add_argument(
        "fname", nargs='?', action='store',
        help="Input file name. Leave empty for stdin.")
    args = parser.parse_args()

    compact_print(args.fname, r"^\s*#")
