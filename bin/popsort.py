#! /usr/bin/env python3

'''
Sort output of "apt-cache search" by popularity

This script takes the output of apt-cache search command and sorts them by
popularity. The popularity ranking is obtained from the popularity contest
website http://popcon.debian.org/by_inst

Sample usage:
  % apt-cache search "^vim-" --names-only | popsort.py
  % apt-cache search sqlite browser | popsort.py
  % apt-cache search sqlite browser | popsort.py --show-ranks
'''

import urllib.request
import os
import time
import sys
import operator
import argparse

''' Retrieve the contents of a url and store it in a file.
If the file already exists, it may or may not be overwritten depending on its
age.  If the file is new, ie its age is less than a threshold, it will not be
overwritten. If the file is old, ie its age is more than a threshold, it will
be overwritten.

Inputs:
url
fname - file name
age_threshold - threshold in seconds to determine whether a file is new or old.

Sample usage:
retrieve_url('http://popcon.debian.org/by_inst', '~/data/popcon/by_inst', 86400)
'''
def retrieve_url(url, fname, age_threshold, debug = 1):
    # Convert fname to absolute path name since
    # os.makedirs() will become confused if the path elements to create include
    # pardir (eg ".." on Unix systems).
    # Ref:- https://docs.python.org/3/library/os.html
    fname = os.path.abspath( os.path.expanduser(fname) )

    if os.path.exists(fname):
        age = time.time() - os.path.getmtime(fname)
        if (age < age_threshold):
            if (debug >= 2):
                print('The file', fname, 'is new. Its age',
                age, 's is less than the threshold', age_threshold, 's.')
                print('Nothing to retrieve.')
            return
    else:
        os.makedirs( os.path.dirname(fname), exist_ok=True)

    url_handle = urllib.request.urlopen(url)
    if (debug >= 1):
        print("reading from", url)
    contents = url_handle.read()
    url_handle.close()

    file_handle = open(fname, "wb")
    if (debug >= 1):
        print("writing to", fname)
    file_handle.write( contents)
    file_handle.close()


def get_all_package_ranks(args):
    use_cache = args.use_cache
    refresh_cache = args.refresh_cache;

    debug = args.debug

    package_ranks = {}

    url = 'http://popcon.debian.org/by_inst'

    if (use_cache):
        fname = '~/data/popcon/by_inst'
        fname = os.path.abspath( os.path.expanduser(fname) )
        if (refresh_cache):
            age_threshold = 0
        else:
            age_threshold = 86400
        retrieve_url(url, fname, age_threshold)
        data_handle = open(fname, 'rb')

        if debug:
            print('reading package rankings from', fname)
    else:
        data_handle = urllib.request.urlopen(url)
        if debug:
            print('reading package rankings from', url)

    for line in data_handle:
        # We are not interested in two types of lines.
        # 1. comments that begin with #
        # 2. There is a line with '-' characters at the end that separates
        # individual package ranks with the Total line
        line=line.decode("utf-8")
        if line.startswith('#') or line.startswith('----'):
            continue
        parts = line.split()
        package_ranks[ parts[1] ] = int( parts[0] )
    data_handle.close()

    return package_ranks


def get_rank(package, ranks):
    if not package in ranks:
        return sys.maxsize
    return ranks[package]

def sort_lines(lines, all_ranks):
    d = {}
    for line in lines:
        pkg = line.split(' ',1)[0]
        d[pkg] = line

    ranks = {}
    for pkg in d.keys():
        ranks[pkg] = get_rank(pkg, all_ranks)
    sorted_ranks = sorted(ranks.items(), key=operator.itemgetter(1),
            reverse=True)

    sorted_lines = []
    for (key, val) in sorted_ranks:
        # sorted_lines.append( str(val) + ' ' + d[key] )
        sorted_lines.append( d[key] )

    return sorted_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Sort output of "apt-cache search" by popularity')
    parser.add_argument(
        '--show-ranks', action='store_true',
        default=False, dest='show_rank',
        help='show popularity rank')

    parser.add_argument(
        '--use-cache', action='store_true',
        default=True, dest='use_cache',
        help='''get popularity rankings from local cache file, not from web.
        Cache file will be updated if necessary.''')
    parser.add_argument(
        '--no-use-cache', action='store_false',
        default=True, dest='use_cache',
        help='''get popularity rankings from web, not from local cache file.
        Cache file is not touched.''')

    parser.add_argument(
        '--refresh-cache', action='store_true',
        default=False, dest='refresh_cache',
        help='''refresh cache. It will be ignored is --no-use-cache
        is specified.''')
    parser.add_argument(
        '--debug', action='store_true',
        default=False, dest='debug',
        help='show debug output')
    args = parser.parse_args()

    all_ranks = get_all_package_ranks(args)
    lines = sys.stdin.read().splitlines()
    sorted_lines = sort_lines(lines, all_ranks)

    for line in sorted_lines:
        if not args.show_rank:
            print(line)
        else:
            pkg = line.split(' ', 1)[0]
            print(get_rank(pkg, all_ranks), line)


''' 
Similar software:

http://www.linuxonly.nl/docs/56/155_Sort_Ubuntu_packages_by_popularity.html
contains a python script to do the same. 
Pros: script is simple, easy to understand
Cons: written in Python2
features lacking:
  The rankings data has to be downloaded manually.
  Does not maintain a local cache of the rankings.
  Does not show ranks.
'''
