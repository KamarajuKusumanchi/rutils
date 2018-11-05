#! /usr/bin/env python3

import subprocess
import argparse
import os

''' Utility program to grep a git repository but exclude the .git directory.

Call it as
  <scriptname> pattern [directory]
The directory name is optional. If missing, the current directory will be used.

If the directory belongs to a .git repository, the top level directory of the
repository will be used in searching. Otherwise an error message is printed and
grepping is done in the original directory.
'''


def do_it(cmd, debug=0, dry=0):
    if (debug):
        print(cmd)
    if (not dry):
        subprocess.call([cmd], shell=True)


def get_gitroot(dirname):
    ''' get the top level git directory.
    If it is not found, return the argument itself.

    Ref:- https://github.com/MaxNoe/python-gitpath/
    '''
    try:
        os.chdir(dirname)
        base = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
    except ValueError:
        print("No git repository found for ", dirname)
        return dirname
    return base.decode('utf-8').strip()


def do_grep(args):
    pattern = args.pattern
    # conversion to absolute path seems to be important if something like ../..
    # is passed.
    directory = get_gitroot(os.path.abspath(args.dir))

    # enclose the pattern in double quotes.
    # ignore swap files created by vim.
    cmd = 'grep -sir "' + pattern + '" ' + directory +  \
        ' --exclude-dir=".git" --exclude="*.swp" --color'
    do_it(cmd, args.debug)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='grep a git repository')
    parser.add_argument(
        "pattern", action="store",
        help="pattern to search for")
    parser.add_argument(
        "dir", nargs='?',
        default=os.getcwd(),
        help="directory")
    parser.add_argument(
        "--debug", action="store_true",
        default=False, dest="debug",
        help="show debug output")
    args = parser.parse_args()

    do_grep(args)
