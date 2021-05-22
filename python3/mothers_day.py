#! /usr/bin/env python3

# Get mothers day for a given year.

import argparse
from datetime import date


def create_parser():
    parser = argparse.ArgumentParser(
        description='Get mothers day for a given year'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        default=False, dest='verbose',
        help='explain what is being done'
    )
    parser.add_argument(
        'year', action='store',
        help='year'
    )
    return parser


def get_mothers_day(year):
    # In 1914, President Woodrow Wilson signed a proclamation
    # establishing the second Sunday in May as a national
    # holiday that honors mothers.
    # Ref:- https://en.wikipedia.org/wiki/Mother's_Day
    if isinstance(year, str):
        year = int(year)
    month = 5
    first_day = date(year, month, 1)
    day = 15 - first_day.isoweekday()
    mdate = date(year, month, day).isoformat()
    return mdate


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.verbose:
        print(args)

    year = args.year
    mdate = get_mothers_day(year)
    print(mdate)
