#! /usr/bin/env python

# Find the column name and row number of a given set of values in a csv file.
#
# For example, if we have a csv file
#     Name,  Age,     City,  Marks
#     jack,   34,   Sydney,    155
#     Riti,   31,    Delhi,    177
#     Aadi,   16,   Mumbai,     81
#    Mohit,   31,    Delhi,    167
#    Veena,   81,    Delhi,    144
#  Shaunak,   35,   Mumbai,    135
#    Shaun,   35,  Colombo,    111
#
# and given a set of values [31, 81, 'Veena'] we want to output
#
# row, col, value
# 6,  Name, Veena
# 3,   Age,    31
# 5,   Age,    31
# 6,   Age,    81
# 4, Marks,    81

import pandas as pd
import numpy as np
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Find the column name and row number of a given set of values in a csv file.')
    parser.add_argument('file_name', action='store', help='name of the data file')
    parser.add_argument('values', nargs='+', help='value(s) to search. Separated by spaces')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose',
                        help='show debug output')

    args = parser.parse_args()
    if args.verbose:
        for key, value in args._get_kwargs():
            if value is not None:
                print(key, value)
    return args


def get_col_rows(df, values):
    rownum = 'rownum0'
    # For now assume that dataframe does not have a column called rownum0.
    # Todo:- afterwards, extend the logic to this case as well.
    if rownum in df.columns:
        raise ValueError(f"Name conflict. dataframe already contains {rownum} column.")
    masked = df[df.isin(values)]
    # To get the real row number, we need to offset the index by 2
    # since the first row will be header and since the default index
    # of the dataframe starts at 0.
    masked[rownum] = np.arange(2, len(masked)+2)
    result = masked.melt(id_vars=rownum, var_name='column').dropna()\
        .rename(columns={rownum: 'row'}).reset_index(drop=True)
    return result


if __name__ == '__main__':
    args = parse_arguments()
    file_name = args.file_name
    values = args.values
    # read all columns as strings so that we can do exact match.
    # read_csv preserves the white space. So strip it out.
    df = pd.read_csv(file_name, dtype='str')\
        .rename(columns=lambda x: x.strip())\
        .apply(lambda x: x.str.strip())
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    df_new = get_col_rows(df, values)
    if not df_new.empty:
        df_new.to_csv(sys.stdout, index=False)

# Credits:
# Got the data set from
# https://thispointer.com/python-find-indexes-of-an-element-in-pandas-dataframe/
# But their code involves for loops and hence not vectorized.
