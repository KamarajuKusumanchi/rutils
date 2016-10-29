#! /usr/bin/env python3

'''
See parse_arguments() for a description of what this script is about.
'''

'''
To download the files
wget "https://packages.debian.org/jessie/allpackages?format=txt.gz" \
        -O /home/rajulocal/x/jessie.tgz
wget "https://packages.debian.org/stretch/allpackages?format=txt.gz" \
        -O /home/rajulocal/x/stretch.tgz
wget "https://packages.debian.org/sid/allpackages?format=txt.gz" \
        -O /home/rajulocal/x/sid.tgz
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


def parse_arguments(args):
    import argparse
    import textwrap    # for dedent

    parser = argparse.ArgumentParser(
        description="Filter lines corresponding to installed packages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
        Show the list of installed packages that are in one
        distribution but not in another. For example, this script can help
        figure out the list of installed packages that are part of Jessie but
        are neither part of Stretch nor Sid.

        The input is read from stdin and output is written to stdout.

        Only the first word of each input line is assumed to be the package
        name. This becomes useful to filter "apt-cache search" output and only
        show the lines corresponding to the installed packages.

        Sample usage:
        % apt-cache search python apt | show_installed.py

        '''))
    parser.add_argument(
        "--include-dist", action="store",
        dest="include_dist",
        help='''Show only if the package is from this distribution. It can be a
        comma separated list if multiple distributions are involved.
        ''')
    parser.add_argument(
        "--exclude-dist", action="store",
        dest="exclude_dist",
        help='''Show only if the package is not from this distribution. It can be a
        comma separated list if mutliple distributions are involved.
       ''')
    args = parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    show_installed()
    # show_installed_simple()
