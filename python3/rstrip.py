#! /usr/bin/env python3

""" Remove trailing whitespaces from each line. The input is read from a file
or from stdin if the file name is '-'. The output is sent to stdout.

Sample usage:
 % python3 ./rstrip.py ~/x/junk73.txt > ~/x/junk74.txt
 % cat ~/x/junk73.txt | python3 ./rstrip.py - > ~/x/junk75.txt

 % python3 ./rstrip.py ~/x/isp.txt | rev | cut -f 1 -d ',' | rev | sort | uniq -c | sort -n | wc -l
46
"""

import sys


def strip_trailing_whitespace(args):
    fname = args.fname
    using_stdin = (fname == "-")

    if (not using_stdin):
        fh = open(fname)
    else:
        fh = sys.stdin

    for line in fh:
        line = line.rstrip()
        print(line)

    if (not using_stdin):
        fh.close()


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description='''Remove trailing whitespaces from each line. The input
        is read from a file or from stdin if the file name is '-'. The output
        is send to stdout''')
    parser.add_argument(
        "fname", action="store",
        help="file to read from. Use '-' to read from stdin")
    args = parser.parse_args()

    strip_trailing_whitespace(args)
