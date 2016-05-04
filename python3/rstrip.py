#! /usr/bin/env python3

""" Remove trailing whitespaces from each line of a file. By default, the
output will be sent to stdout.

Sample usage:
% python3 ~/work/gitlab/rutils/python3/rstrip.py ~/x/isp.txt | rev | cut -f 1 -d ',' | rev | sort | uniq -c | sort -n | wc -l
46
"""

def strip_trailing_whitespace(args):
    fname = args.fname
    fh = open(fname)
    for line in fh:
        line = line.rstrip()
        print(line)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description='''Remove trailing whitespaces from each line of a file.
        By default, the output will be send to stdout''')
    parser.add_argument(
        "fname", action="store",
        help = "Input file name")
    args = parser.parse_args()

    strip_trailing_whitespace(args)
