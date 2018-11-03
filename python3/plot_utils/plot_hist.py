#! /usr/bin/env python3

# plot histogram of a column of data read from stdin.

import sys
import pandas as pd
import matplotlib.pyplot as plt

import os


def plot_hist(df, ycol):
    plt.figure(figsize=(8,6))
    plt.hist(df[ycol].values)
    plt.xlabel(ycol, fontsize=12)
    plt.grid()
    plt.show()


if __name__ == "__main__":
    if os.fork():
        # Parent
        pass
    else:
        # Child
        os.setsid()
        df = pd.read_csv(sys.stdin)
        plot_hist(df, df.columns[0])
