#! /usr/bin/env python3

# Script to backup a file or directory
#
# The input is copied to src_asof_YYYYMMDD_HHmmSS where src is the original
# file or directory and YYYYMMDD_HHmmSS is its last modified time.

import argparse
import sys

# The path_magic sets the sys.path so that file_utils in the lib directory
# can be imported. The reason for adding it there instead of directly setting
# the path here itself is to prevent pycodestyle errors such as
#     E402 module level import not at top of file
# This work around was suggested in
# https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path/36829884
from path_magic import add_project_root_to_path

from lib.file_utils import backup_with_timestamp


def create_parser():
    parser = argparse.ArgumentParser(
        description="Make backup"
    )
    parser.add_argument(
        '-t', '--target-directory', action='store',
        dest='target_dir',
        help='copy all source to target_dir'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        default=False, dest='verbose',
        help='explain what is being done'
    )
    parser.add_argument(
        'source', action='store',
        help='source directory to backup'
    )
    return parser


if __name__ == '__main__':
    # src = sys.argv[1]
    parser = create_parser()
    args = parser.parse_args()
    if args.verbose:
        print(args)

    src = args.source
    target_dir = args.target_dir
    backup_with_timestamp(src, target_dir)
