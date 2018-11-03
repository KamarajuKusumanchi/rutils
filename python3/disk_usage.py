import argparse
import os
import sys


def get_size(path):
    """
    Get size of a file or folder.
    Should give the same output as "du -sb <path>"
    :param path: The absolute path of a file or directory.
    :return:
    """
    size = 0

    # If path is a file, os.walk(path) for loop  will not even run once.
    # So take care of this separately.
    if os.path.isfile(path):
        return os.path.getsize(path)

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            size += os.path.getsize(file_path)
    return size


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description='Get disk usage.'
    )
    parser.add_argument(
        'file', action='store',
        help='disk usage of a file or a directory'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    path = os.path.abspath(args.file)
    size = get_size(path)
    print(size, '\t', path)
