#! /usr/bin/env python3

# Script to backup a file or directory
#
# The input is copied to src_asof_YYYYMMDD_HHmmSS where src is the original
# file or directory and YYYYMMDD_HHmmSS is its last modified time.

import sys
import os
import argparse

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from lib.file_utils import backup_with_timestamp


def parse_arguments(args):
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
    args = parser.parse_args()
    if args.verbose:
        print(args)
    return args


# src = sys.argv[1]
args = parse_arguments(sys.argv[1:])
src = args.source
target_dir = args.target_dir
backup_with_timestamp(src, target_dir)
