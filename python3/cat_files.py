#! /usr/bin/env python3

# cat multiple files

import argparse
import shutil
import sys

def create_parser():
    parser = argparse.ArgumentParser(
        description='Cat multiple files'
    )
    parser.add_argument('source_file', nargs='+', help='files to combine')
    parser.add_argument('-o', '--output', help='output file', dest='dest_file', default=sys.stdout)
    return parser

def cat_files(dest, sources):
    """Cat multiple files into dest."""
    # Adapted from https://github.com/mongodb/mongo-python-driver/blob/master/test/utils.py
    if dest is None or dest is sys.stdout:
        # https://bugs.python.org/issue4571 says to use sys.stdout.buffer
        # when writing binary data to stdout.
        fdst = sys.stdout.buffer
    else:
        fdst = open(dest, 'wb')

    for src in sources:
        with open(src, 'rb') as fsrc:
            shutil.copyfileobj(fsrc, fdst)

    if fdst is not sys.stdout.buffer:
        fdst.close()

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    cat_files(args.dest_file, args.source_file)
    # cat_files(None, args.source_file)
    # cat_files(sys.stdout, args.source_file)