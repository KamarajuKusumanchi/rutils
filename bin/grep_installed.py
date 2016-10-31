#! /usr/bin/env python3

'''
See parse_arguments() for a description of what this script is about.
'''

'''
To download the files
wget "https://packages.debian.org/jessie/allpackages?format=txt.gz" \
        -O /home/rajulocal/x/jessie.txt.gz
wget "https://packages.debian.org/stretch/allpackages?format=txt.gz" \
        -O /home/rajulocal/x/stretch.txt.gz
wget "https://packages.debian.org/sid/allpackages?format=txt.gz" \
        -O /home/rajulocal/x/sid.txt.gz
'''

import sys
import apt
import pandas as pd
import gzip


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


def add_distribution_columns(df, args):
    all_dists = get_all_dists(args)
    if (not all_dists):
        return

    for distribution in all_dists:
        dist_packages = read_compact_compressed_allpackages_list(distribution)
        if (dist_packages.empty):
            continue

        df[distribution] = df['pkg'].isin(dist_packages['pkg'])


def get_all_dists(args):
    dists_to_include = get_dists_to_include(args)
    dists_to_exclude = get_dists_to_exclude(args)

    all_dists = dists_to_include + dists_to_exclude
    return all_dists


def get_dists_to_include(args):
    include_dist = args.include_dist

    dists_to_include = []
    if (include_dist is not None):
        dists_to_include = [x.strip() for x in include_dist.split(',')]
    return dists_to_include


def get_dists_to_exclude(args):
    exclude_dist = args.exclude_dist

    dists_to_exclude = []
    if (exclude_dist is not None):
        dists_to_exclude = [x.strip() for x in exclude_dist.split(',')]
    return dists_to_exclude


# For a given distribution, a list of all available packages on all
# architectures can be downloaded from
# https://packages.debian.org/${distribution}/allpackages?format=txt.gz . Here
# the ${distribution} can be an actual name such as jessie, stretch, sid etc.,
# or a symbolic name such as stable, testing, unstable etc., For example, for
# sid this would be https://packages.debian.org/sid/allpackages?format=txt.gz .
#
# The idea here is to process this file and return a data frame containing the
# list of packages.
def read_compact_compressed_allpackages_list(distribution):
    fname = '/home/rajulocal/x/' + distribution + '.txt.gz'

    df = pd.DataFrame(None)
    try:
        # Check if the file can be opened.
        with gzip.open(fname, 'rt') as f:
            for i in range(6):
                ignore = f.readline()
            df['pkg'] = [line.split(' ', 1)[0] for line in f]
    except:
        print("Unable to open", fname, "while processing", distribution,
              "distribution")
    return df


def show_installed(args):
    debug = args.debug

    df = get_input_as_df()
    add_is_installed_column(df)
    add_distribution_columns(df, args)

    if debug:
        out_file = "agg.csv"
        print("dumping dataframe to", out_file)
        df.to_csv(out_file, index=False)

    condition = get_condition(df, args)
    b = df[condition]

    if (not b.empty):
        for line in b['data']:
            print(line)


def get_condition(df, args):
    dists_to_include = get_dists_to_include(args)
    dists_to_exclude = get_dists_to_exclude(args)

    condition = df['is_installed']

    for distribution in dists_to_include:
        if (distribution in df.columns):
            condition &= df[distribution]

    for distribution in dists_to_exclude:
        if (distribution in df.columns):
            condition &= ~df[distribution]

    return condition


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
    # parser.add_argument(
    #     "--update", action="store_true",
    #     dest="update_cache",
    #     help='''update the package lists'''
    #     )
    parser.add_argument(
        "--debug", action='store_true',
        default=False, dest='debug',
        help='show debug output')
    return parser.parse_args()


def run_code():
    args = parse_arguments(sys.argv[1:])
    show_installed(args)
    # show_installed_simple()

if __name__ == "__main__":
    run_code()
