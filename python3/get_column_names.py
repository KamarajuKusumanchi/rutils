#! /usr/bin/env python3

# Given a csv file, print its column names one per line.

import pandas as pd
import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="get column names of a csv file")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        dest="verbose",
        help="explain what is being done",
    )
    parser.add_argument("file_name", action="store", help="file name")
    return parser


def main(file_name):
    df = pd.read_csv(file_name)
    # Strip out the white space from both ends of the column names
    df.columns = df.columns.str.strip()
    [print(x) for x in df.columns]


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    if args.verbose:
        print(args)

    file_name = args.file_name
    main(file_name)
