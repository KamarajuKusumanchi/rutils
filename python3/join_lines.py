#! /usr/bin/env python3

import argparse
import sys
# Python script to join multiple lines with a given delimiter.
# Example:
#   cat input.txt | join_lines.py
# A delimiter can be specified using -d
#   cat input.txt | join_lines.py -d ','
#
# One liner equivalent
# cat input.txt | python -c "import sys; print(', '.join([ l.strip() for l in sys.stdin.readlines() ]))"
# Ref:- https://askubuntu.com/a/872742/574082
#
# search tags | join multiple lines with comma on command line
#
# Todo: write test case
# Todo:- Figure out how to write a test case for input from stdin that uses sys.stdin.readlines(). Use mock?
# May be useful: https://stackoverflow.com/questions/35851323/how-to-test-a-function-with-input-call
#
# Sample input
# $ cat input.txt
# 163418
# 184855
# 185954
#
# Test 1
# $ cat input.txt | join_lines.py
# 163418, 184855, 185954
#
# Test 2
# $ cat input.txt | join_lines.py -d ","
# 163418,184855,185954


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Join lines'
    )
    parser.add_argument('-d', '--delimiter', action='store', dest='delim',
                        default=', ', help='delimiter')
    res = parser.parse_args()
    return res


if __name__ == '__main__':
    args = parse_arguments()
    delim = args.delim
    print(delim.join([l.rstrip() for l in sys.stdin.readlines()]))
