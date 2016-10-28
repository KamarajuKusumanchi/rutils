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


def show_installed():
    lines = sys.stdin.read().splitlines()
    cache = apt.Cache()

    installed = []
    for line in lines:
        pkg = line.split(' ', 1)[0]
        if (pkg in cache) and cache[pkg].is_installed:
            installed.append(line)

    for line in installed:
        print(line)


if __name__ == "__main__":
    # args = parse_arguments()
    show_installed()
