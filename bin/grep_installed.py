#! /usr/bin/env python3

'''
For documentation on this script, see
http://raju.shoutwiki.com/wiki/Grep_installed.py

To see what it is about, run it with -h which produces brief help.  For example
grep_installed.py -h

The brief help can also be found in parse_arguments().
'''

'''
Use case1:
Filter apt-cache search output and show information for installed packages only
% apt-cache search python apt | grep_installed.py

Use case2:
From a given set of packages, show the installed ones
% echo "python3.4 python3.5" | tr ' ' '\n' | grep_installed.py

Use case3:
From a given set of packages, show all the installed packages that are
in jessie, but are neither in stretch nor in sid. This involves multiple steps:

step 1: For each distribution of interest, create/cache the packages list
% grep_installed.py --update-cache --include-dists='jessie' \
--exclude-dists='stretch,sid'
The cache files are stored as <distribution>.gz in the cache directory
(~/.cache/grep_installed/)

step2: run the query
% echo "python3.4 python3.5" | tr ' ' '\n' | \
grep_installed.py --include-dists='jessie' --exclude-dists='stretch,sid'

step3 (optional): clear the cache
% grep_installed.py --clear-cache
This will remove all *.gz files in the cache directory
(~/.cache/grep_installed) and the directory itself (if it is empty).

Use case4:
For a given set of pacakges, print a matrix showing whether the package is
installed, and its availability in various distributions.
/* update the cache as shown before */
 % echo "python3.4 python3.5" | tr ' ' '\n' | \
grep_installed.py --include-dists='jessie' --exclude-dists='stretch,sid' \
--report matrix | column -ts ','
data       pkg        is_installed  jessie  sid    stretch
python3.4  python3.4  True          True    False  False
python3.5  python3.5  True          False   True   True
'''

import sys
import apt
import pandas as pd
import gzip
import urllib.request
import io
import xdg.BaseDirectory
import os
import glob


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
    report = args.report
    if (not all_dists):
        if (report == "packages"):
            return
        elif (report == "matrix" or report == "tabulate"):
            all_dists = ["stable", "testing", "unstable"]

    for distribution in all_dists:
        # dist_packages = read_compact_compressed_allpackages_list(distribution)
        dist_packages = read_pkg_data(distribution, args)
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


def cache_dir():
    cache_dir = os.path.join(
        xdg.BaseDirectory.xdg_cache_home, 'grep_installed'
    )
    return cache_dir


# This function is not currently used.
# In the future, I need to enhance it to address its limitations as
# outlined below. For now, I will take a shortcut and use
# http://httpredir.debian.org/debian/dists/<distribution>/<section>/binary-amd64/Packages.gz
# to get the list of packages. This is done in get_packages_in_a_section().
# The update_cache_files() is the top level function that builds all the cache.
#
# For a given distribution, a list of all available packages on all
# architectures can be downloaded from
# https://packages.debian.org/${distribution}/allpackages?format=txt.gz . Here
# the ${distribution} can be an actual name such as jessie, stretch, sid etc.,
# or a symbolic name such as stable, testing, unstable etc., For example, for
# sid this would be https://packages.debian.org/sid/allpackages?format=txt.gz .
#
# The idea here is to process this file and return a data frame containing the
# list of packages.
#
# The current implementation of this function has a few limitations. It only
# looks at the first word of each line to figure out whether the package is
# part of the distribution or not. But this is not enough. To get the correct
# list, we need to filter based on the architecture, type of package etc.,.
# Doing all that requires some regex magic.
#
# For example, the file contains lines such as
#
# python3.4 (3.4.2-1) [debports] Interactive high-level object-oriented \
# language (version 3.4)
#
# python3.4-tk virtual package provided by python3-tk
#
# which means these packages do not actually exist on my architecture (ex:-
# amd64) but the function below returns them as valid package names.
def read_compact_compressed_allpackages_list(distribution):
    fname = os.path.join(
        cache_dir(), distribution + '.txt.gz')

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


def read_pkg_data(distribution, args):
    fname = os.path.join(
        cache_dir(), distribution+'.gz')
    fname = os.path.abspath(os.path.expanduser(fname))

    try:
        df = pd.read_csv(fname, compression='gzip')
    except:
        print('Failed to read package list from', fname)
        df = pd.DataFrame(None)
    return df


# Update cache for all distributions of interest
def update_cache_files(args):
    all_dists = get_all_dists(args)

    # If no distributions are specified, the package lists of stable, testing,
    # and unstable are written.
    if (not all_dists):
        all_dists = ["stable", "testing", "unstable"]
    for distribution in all_dists:
        write_pkg_data(distribution, args)


# Build a list of packages for a given distribution and write it to a file
def write_pkg_data(distribution, args):
    df = get_pkg_data(distribution, args)

    directory = cache_dir()
    fname = os.path.join(
        directory, distribution+'.gz')
    fname = os.path.abspath(os.path.expanduser(fname))

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    print('writing:', fname)
    df.to_csv(fname, index=False, compression='gzip')


def get_pkg_data(distribution, args):
    sections = ['main', 'contrib', 'non-free']

    frames = [get_packages_in_a_section(distribution, s, args)
              for s in sections]
    df = pd.concat(frames)

    return df


# Returns a dataframe containing the list of packages in a distribution for a
# given section. The section is one of 'main', 'contrib', 'non-free'.
def get_packages_in_a_section(distribution, section, args):
    debug = args.debug

    df = pd.DataFrame(None)

    # Assuming that the architecture is always going to be amd64.
    # Todo:- Need to enhance this later and make it architecture independent.
    request = "http://httpredir.debian.org/debian/dists/" + distribution \
              + "/" + section + "/binary-amd64/Packages.gz"
    if debug:
        print("processing url", request)

    try:
        response = urllib.request.urlopen(request)
        with gzip.open(response, 'rt') as gzipFile:
            # for i in range(10):
            #     print(gzipFile.readline().strip())
            dictList = []
            for line in gzipFile:
                d = {}
                if line[:8] == 'Package:':
                    pkg = line.split(' ')[1].strip()
                elif line[:8] == 'Version:':
                    version = line.split(' ')[1].strip()
                    d['pkg'] = pkg
                    d['version'] = version
                    d['section'] = section
                    dictList.append(d)
                else:
                    continue
            df = pd.DataFrame(dictList)
            df.drop_duplicates(inplace='True')
            print('Processed:', request)
    except:
        print("Unable to get data from", request)

    return df


def clear_cache_files(args):
    directory = cache_dir()
    files = os.path.join(directory, '*.gz')
    for fname in glob.glob(files):
        print('removing', fname)
        os.unlink(fname)

    if not os.listdir(directory):
        print('removing', directory)
        os.rmdir(directory)


def show_installed(args):
    debug = args.debug
    report = args.report

    df = get_input_as_df()
    add_is_installed_column(df)
    add_distribution_columns(df, args)

    if debug:
        out_file = "agg.csv"
        print("dumping dataframe to", out_file)
        df.to_csv(out_file, index=False)

    if (report == "matrix"):
        df.to_csv(sys.stdout, index=False)
    elif (report == "tabulate"):
        tabulate_data_frame(df)
    elif (report == "packages"):
        condition = get_condition(df, args)
        b = df[condition]

        if (not b.empty):
            for line in b['data']:
                print(line)
    else:
        print("report = ", report, "is not a valid option")


def tabulate_data_frame(df):
    try:
        from tabulate import tabulate
        print(tabulate([list(row) for row in df.values],
              headers=list(df.columns), tablefmt='plain'))
    except:
        print("\nWarning: tabulate package is not found.",
              "Dumping it to csv instead.\n")
        df.to_csv(sys.stdout, index=False)


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
        description='Show installed packages after filtering them by ' +
        'their availability in different distributions.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
This script can be used to show the list of installed packages that are in one
distribution but not in another. For example, it can be used to figure out the
list of installed packages that are part of Debian Stable but are neither part
of Debian Testing nor Debian Unstable. The script can handle both symbolic
distribution names such as Stable/Testing/Unstable and actual distribution
names such as Jessie/Stretch/Sid etc., The script can process "apt-cache
search" output. The output from the script can be shown in different "report"
formats.

The input is read from stdin and output is written to stdout.

Only the first word of each input line is assumed to be the package name. This
becomes useful when processing "apt-cache search" output.

For complete documentation with sample use cases see
http://raju.shoutwiki.com/wiki/Grep_installed.py
        '''))
    parser.add_argument(
        "--include-dists", action="store",
        dest="include_dist",
        help='''Show only if the package is from this distribution. It can be a
        comma separated list if multiple distributions are involved.
        ''')
    parser.add_argument(
        "--exclude-dists", action="store",
        dest="exclude_dist",
        help='''Show only if the package is not from this distribution. It can be a
        comma separated list if mutliple distributions are involved.
       ''')
    parser.add_argument(
        "--update-cache", action="store_true",
        dest="update_cache",
        help='''update the package lists'''
        )
    parser.add_argument(
        "--clear-cache", action="store_true",
        dest="clear_cache",
        help="clear cache files and directory"
        )
    parser.add_argument(
        '--report', action='store',
        dest="report", default='packages',
        choices=['packages', 'matrix', 'tabulate'],
        help='''Type of reports to produce.'''
        )
    parser.add_argument(
        "--debug", action='store_true',
        default=False, dest='debug',
        help='show debug output')
    return parser.parse_args()


def run_code():
    args = parse_arguments(sys.argv[1:])
    if (args.debug):
        print("args\n", args)
    if (args.update_cache):
        update_cache_files(args)
    elif (args.clear_cache):
        clear_cache_files(args)
    else:
        show_installed(args)
    # show_installed_simple()


if __name__ == "__main__":
    run_code()
