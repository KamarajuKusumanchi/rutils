#! /usr/bin/env python3

""" Print a file after removing comments and empty lines.

Usage:
stuff.py filename

Sample usage:
% stuff.py /etc/apt/sources.list
"""

import argparse
import re

def compact_print(fname, comment_pattern):
    empty_pattern = "^\s*$"

    fh = open(fname)
    for line in fh:
        line = line.rstrip()
        if re.search(comment_pattern, line):
            continue
        elif re.search(empty_pattern, line):
            continue
        else:
            print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Print a file after removing comments and
        empty lines.''')
    parser.add_argument(
        "fname", action="store",
        help = "Input file name")
    args = parser.parse_args()

    compact_print(args.fname, "^\s*#")
