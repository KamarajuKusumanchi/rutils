#! /usr/bin/env python3

# plot a column of data read from stdin.

import sys
import pandas as pd
import matplotlib.pyplot as plt

def parse_arguments(args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Plot a column of data read from stdin'
        )

    parser.add_argument(
        "--header", action='store_true',
        dest='header',
        help='use 1st line as header')
    parser.add_argument(
        "--no-header", action='store_false',
        dest='header',
        help='assumes that there is no header')
    parser.set_defaults(header=True)

    parser.add_argument(
        "--debug", action='store_true',
        default=False, dest='debug',
        help='show debug output. Default is false.')
    res = parser.parse_args(args)
    if res.debug:
        print(res)
    return res


# y is a pandas.core.series.Series
# ylabel is a string
def plot_col_by_index(y, ylabel):
    plt.figure(figsize=(8,6))
    plt.scatter(range(y.shape[0]), y)
    plt.title('plot by Index')
    plt.xlabel('index', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid()
    plt.show()

if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    
    header = args.header
    if (header):
        df = pd.read_csv(sys.stdin)
        plot_col_by_index(df[ df.columns[0] ], df.columns[0])
    else:
        df = pd.read_csv(sys.stdin, header=None)
        plot_col_by_index(df[ df.columns[0] ], 'data')
