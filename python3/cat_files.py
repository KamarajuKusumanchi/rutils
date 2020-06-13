#! /usr/bin/env python3

# cat multiple files
#
# Sample usage:
#     cat_files.py file1 file2
# prints the output to stdout
#     cat_files.py file1 file2 -o out_file
# print the output to out_file
#
# If there are multiple files with the same headers, we can concatenate
# them and only keep the headers of the first file by using --collapse-headers
# option. For example
#     cat_files.py file1.csv file2.csv --collapse-headers
#     cat_files.py file1.csv file2.csv --collapse-headers -o out_file.csv

import argparse
import shutil
import sys


def create_parser():
    parser = argparse.ArgumentParser(
        description='Cat multiple files'
    )
    parser.add_argument('source_file', nargs='+', help='files to combine')
    parser.add_argument('-o', '--output', help='output file',
                        dest='dest_file', default=sys.stdout)
    parser.add_argument('--collapse-headers', help='ignore all headers except the first',
                        action='store_true', default=False)
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


def cat_files_with_same_header(dest, sources):
    """Cat multiple files into dest. Ignore headers in all the files except the first."""
    if dest is None or dest is sys.stdout:
        fdst = sys.stdout
    else:
        fdst = open(dest, 'w')

    first_src = sources.pop(0)
    with open(first_src, 'r') as fsrc:
        header = fsrc.readline()
        fdst.write(header)
        shutil.copyfileobj(fsrc, fdst)

    for src in sources:
        with open(src, 'r') as fsrc:
            # read but ignore the header
            header = fsrc.readline()
            shutil.copyfileobj(fsrc, fdst)

    if fdst is not sys.stdout:
        fdst.close()


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    # print(args)
    if args.collapse_headers:
        cat_files_with_same_header(args.dest_file, args.source_file)
        # cat_files_with_same_header(None, args.source_file)
        # cat_files_with_same_header(sys.stdout, args.source_file)
    else:
        cat_files(args.dest_file, args.source_file)
        # cat_files(None, args.source_file)
        # cat_files(sys.stdout, args.source_file)
