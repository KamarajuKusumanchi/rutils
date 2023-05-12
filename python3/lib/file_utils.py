import re
from glob import glob
from datetime import datetime
import os
import shutil
import pandas as pd


def pick_first_file(dir_name, file_glob):
    dir_name = os.path.abspath(os.path.expanduser(dir_name))
    file_list = glob(os.path.join(dir_name, file_glob))
    # glob returns an empty array if no matches are found
    if not file_list:
        return None
    return sorted(file_list)[0]


def pick_last_file(dir_name, file_glob):
    dir_name = os.path.abspath(os.path.expanduser(dir_name))
    file_list = glob(os.path.join(dir_name, file_glob))
    # glob returns an empty array if no matches are found
    if not file_list:
        return None
    return sorted(file_list, reverse=True)[0]


def rename_with_timestamp(src):
    # Given a file or directory src, move it to src_asof_YYYYMMDD_HHmmSS where
    # YYYYMMDD_HHmmSS is the last modified time. This function is useful to
    # take a backup before something else overwrites the original source.
    #
    # If the destination file/directory already exists, do not overwrite it.
    #
    # Get the absolute path since src can contain something like '.' and '..'
    src = os.path.abspath(os.path.expanduser(src))
    if not os.path.exists(src):
        return
    mtime = os.path.getmtime(src)
    timestamp = datetime.fromtimestamp(mtime).strftime("%Y%m%d_%H%M%S")
    dst = src + "_asof_" + timestamp
    if not os.path.exists(dst):
        shutil.move(src, dst)
        print(src, " -> ", dst)
    else:
        print(src, " --> ", dst)


def backup_with_timestamp(src, target_dir=None):
    # Given a file or directory src, copy it to src_asof_YYYYMMDD_HHmmSS where
    # YYYYMMDD_HHmmSS is the last modified time. This function is useful to
    # take a backup before something else overwrites the original source.
    #
    # If the destination file/directory already exists, do not overwrite it.
    #
    # If target_dir is specified, src is copied into it.
    #
    # Get the absolute path since src can contain something like '.' and '..'
    src = os.path.abspath(os.path.expanduser(src))
    if not os.path.exists(src):
        return
    mtime = os.path.getmtime(src)
    timestamp = datetime.fromtimestamp(mtime).strftime("%Y%m%d_%H%M%S")

    if target_dir is None:
        target_dir = os.path.dirname(src)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    base_name = os.path.basename(src)
    dst = os.path.join(target_dir, base_name + "_asof_" + timestamp)

    if not os.path.exists(dst):
        if os.path.isfile(src):
            shutil.copy(src, dst)
        else:
            shutil.copytree(src, dst)
        print(src, " -> ", dst)
    else:
        print(src, " --> ", dst)


def find_files_by_pattern(directory, pattern, depth=-1):
    r"""
    Find files in a directory that match a pattern.

    :param directory:  top level directory to start searching from
    :param pattern: pattern to match
    :param depth: optional, the maximum depth to descend into.
        A depth of -1 implies no limit.
        Depth of 0 searches in {dir}, 1 searches in {dir, dir/foo},
        2 searches in {dir, dir/foo, dir/foo/bar} etc.,
    :return: list of files that match the pattern

    Examples:
    pattern = '.*' - find all files in directory
    pattern = '\.py$' - find all python files
    pattern = '\.csv$' - find all csv files

    pattern = 'foo' - find files that have foo anywhere in its name. This will match
                      a.foo, abfoo, foo.txt, afoo, afoob
    pattern = '.foo' - find files that have one character followed by foo. This will match
                       a.foo, abfoo, afoo, afoob
                       but not foo.txt
    pattern = '\.foo' - This will match a.foo, a.fool
    pattern = '\.foo$' - This will match a.foo but not a.fool

    Initial version of this function is from https://github.com/Public-Health-Bioinformatics/sequdas-irida-uploader/blob/master/src/API/fileutils.py
    """
    result_list = [
        os.path.join(root, filename)
        for root, dirs, files in walk(directory, depth)
        for filename in files
        if re.search(pattern, filename)
    ]
    return result_list


def walk(directory, depth):
    if depth < 0:
        return os.walk(directory)
    else:
        return walklevel(directory, depth)


def walklevel(directory, depth=0):
    """Descend into a directory up to a specified depth.
    It works just like os.walk, but you can pass a depth parameter that
    indicates how deep the recursion will go. Depth must be >= 0.

    Initial version is from:
    http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below

    :param directory: top level directory to start the walk from
    :param depth: the maximum depth to descend into
        must be >= 0
        A depth of 0 walks in {dir}, 1 walks in {dir, dir/foo},
        2 walks in {dir, dir/foo, dir/foo/bar} etc.,

        Note:- The depth here is equal to LEVELS - 1 in 'find directory -maxdepth LEVELS' since
        find . -maxdepth 1    lists files in {dir}
        find . -maxdepth 2    lists files in {dir, dir/foo}
        find . -maxdepth 3    lists files in {dir, dir/foo, dir/foo/bar} etc.,

    :return: a generator
    """
    assert depth >= 0
    directory = directory.rstrip(os.path.sep)
    assert os.path.isdir(directory)
    num_sep = directory.count(os.path.sep)
    for root, dirs, files in os.walk(directory):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep_this - num_sep >= depth:
            del dirs[:]


def count_files(top, pattern, list_files):
    # Given a 'pattern' count the number of files in each subdirectory
    # of 'top'. If list_files is True, the file names are shown in a column.
    #
    # Consider the following directory structure
    # rajulocal@hogwarts ~/work/github/rutils/python3/tests/data/count_files
    #  % tree -a
    # .
    # ├── analysis.txt
    # ├── c.csv
    # ├── d1
    # │   ├── d2
    # │   │   ├── d3
    # │   │   │   └── f5.txt
    # │   │   ├── f3.txt
    # │   │   └── f4.txt
    # │   ├── f2.txt
    # │   └── f6.txt
    # ├── f1.txt
    # ├── f7.txt
    # └── .hidden
    #     └── c.csv
    #
    # 4 directories, 10 files
    #
    # To count the text files
    # df = count_files('tests/data/count_files', '\.txt', False)
    # df
    # Out[5]:
    #   pattern  level name_space  count
    # 0   \.txt      0          .      3
    # 1   \.txt      1         d1      2
    # 2   \.txt      2      d1\d2      2
    # 3   \.txt      3   d1\d2\d3      1
    #
    # To see what those files are
    # df = count_files('tests/data/count_files', '\.txt', True)
    # df
    # Out[6]:
    #   pattern  level name_space  count                           files
    # 0   \.txt      0          .      3  [analysis.txt, f1.txt, f7.txt]
    # 1   \.txt      1         d1      2                [f2.txt, f6.txt]
    # 2   \.txt      2      d1\d2      2                [f3.txt, f4.txt]
    # 3   \.txt      3   d1\d2\d3      1                        [f5.txt]
    #
    # To get the total number of files
    # df['count'].sum()
    # Out[7]:
    # 8
    #
    # To count the csv files
    # df = count_files('tests/data/count_files', '\.csv', True)
    # df
    # Out[8]:
    #   pattern  level name_space  count    files
    # 0   \.csv      0          .      1  [c.csv]
    # 1   \.csv      1    .hidden      1  [c.csv]
    # df['count'].sum()
    # Out[9]:
    # 2
    # To count all the files
    # df = count_files('tests/data/count_files', '.*', True)
    # df
    # Out[10]:
    #   pattern  level name_space  count                                  files
    # 0      .*      0          .      4  [analysis.txt, c.csv, f1.txt, f7.txt]
    # 1      .*      1    .hidden      1                                [c.csv]
    # 2      .*      1         d1      2                       [f2.txt, f6.txt]
    # 3      .*      2      d1\d2      2                       [f3.txt, f4.txt]
    # 4      .*      3   d1\d2\d3      1                               [f5.txt]
    # df['count'].sum()
    # Out[11]:
    # 10
    # which matches with the file count from the tree command.
    #
    # Ref:-
    # * https://stackoverflow.com/questions/72274073/python-count-files-in-a-directory-and-all-its-subdirectories
    # * To experiment - https://github.com/KamarajuKusumanchi/notebooks/blob/master/python/so_72274073_count_files/count_files.ipynb
    #
    # tags | for each directory in folder find the number of files,
    # number of files in a directory and its subdirectories,
    # dokuwiki count pages
    #
    # Todo:- add a depth parameter to restrict how far down we have to search
    # in 'top' directory.
    top = os.path.abspath(os.path.expanduser(top))
    res = []
    for root, dirs, files in os.walk(top):
        name_space = os.path.relpath(root, top)
        level = (
            os.path.normpath(name_space).count(os.sep) + 1 if name_space != "." else 0
        )
        matches = [file for file in files if re.search(pattern, file)]
        if matches:
            if list_files:
                # sort the list of files so that the output is consistent
                # across different OSes.
                res.append((pattern, level, name_space, len(matches), sorted(matches)))
            else:
                res.append((pattern, level, name_space, len(matches)))

    if list_files:
        df = pd.DataFrame(
            res, columns=["pattern", "level", "name_space", "count", "files"]
        )
    else:
        df = pd.DataFrame(res, columns=["pattern", "level", "name_space", "count"])
    return df
