#! /usr/bin/env python3

# Order columns alphabetically
import argparse
import pandas as pd
import sys


def create_parser():
    parser = argparse.ArgumentParser(description='Order columns alphabetically')
    parser.add_argument('--strip-spaces', action='store_true', default=False,
                        help='strip out the spaces in column names before sorting.')
    parser.add_argument('--reverse', action='store_true', default=False,
                        help='reverse the sort order')
    return parser


def order_columns(df, strip_spaces, reverse):
    # If strip_spaces is True, then the spaces around the column names are
    # stripped out before they are sorted.
    # Ex:-
    # Input = ['    name', '  number', '  address']
    # if strip_spaces:
    #   output = ['  address', '    name', '  number']
    # else:
    #   output = ['    name', '  address', '  number']
    return df[sorted(df.columns, reverse=reverse,
                     key=lambda x: x.strip() if strip_spaces else x)]


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    df = pd.read_csv(sys.stdin, dtype='str')
    df2 = order_columns(df, args.strip_spaces, args.reverse)
    df2.to_csv(sys.stdout, index=False)
