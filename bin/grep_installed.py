#! /usr/bin/env python3

'''
Filter the input and only show the list of installed packages.

For each input line, the first word is assumed to be the package name.

This is useful, for example to filter the output of apt-cache search and show
only the installed packages.

Sample usage:
  % apt-cache search python apt | show_installed.py
'''

import sys
import apt
import pandas as pd


def get_input_as_df():
    data = sys.stdin.read().splitlines()
    pkgs = [line.split(' ', 1)[0] for line in data]
    df = pd.DataFrame(
        {'pkg': pkgs,
         'data': data})
    return df


# Add 'is_installed' column to the data frame df
def add_is_installed_column(df):
    cache = apt.Cache()
    df['is_installed'] = [
        True if ((pkg in cache) and cache[pkg].is_installed) else False
        for pkg in df['pkg']
    ]


def show_installed():
    df = get_input_as_df()
    add_is_installed_column(df)

    b = df[df['is_installed']]
    for line in b['data']:
        print(line)


# Not using this function anymore.
def show_installed_simple():
    lines = sys.stdin.read().splitlines()
    cache = apt.Cache()

    installed = []
    for line in lines:
        pkg = line.split(' ', 1)[0]
        if (pkg in cache) and cache[pkg].is_installed:
            installed.append(line)

    for line in installed:
        print(line)

# def parse_arguments(args):
#     import argparse
#     parser = argparse.ArgumentParser(
#         description='

if __name__ == "__main__":
    # args = parse_arguments()
    show_installed()
    # show_installed_simple()
