import os

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from lib.file_utils import find_files_by_pattern, count_files


def test_find_files_by_pattern_no_depth_specified():
    # Check that find_files_by_pattern() does a recursive search if depth is not specified.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(os.path.dirname(dir_path), 'data', 'walk')
    txt_files = find_files_by_pattern(data_dir, r'\.txt$')
    txt_files = [os.path.relpath(x, data_dir) for x in txt_files]
    nfiles_got = len(txt_files)
    nfiles_expected = 14
    assert nfiles_got == nfiles_expected, \
        'Expecting {} files but got {} files instead'.format(nfiles_expected, nfiles_got)


@pytest.mark.parametrize('pattern, depth, nfiles_expected', [
    (r'\.txt$', -1, 14),
    (r'\.txt$', 0, 0),
    (r'\.txt$', 1, 2),
    (r'\.txt$', 2, 6),
    (r'\.txt$', 3, 14),
    (r'^monthly', 1, 0),
    (r'^monthly', 2, 4),
])
def test_find_files_by_pattern_depth_specified(pattern, depth, nfiles_expected):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(os.path.dirname(dir_path), 'data', 'walk')
    txt_files = find_files_by_pattern(data_dir, pattern, depth)
    txt_files = [os.path.relpath(x, data_dir) for x in txt_files]
    nfiles_got = len(txt_files)
    assert nfiles_got == nfiles_expected, \
        'Expecting {} files but got {} files instead'.format(nfiles_expected, nfiles_got)


def test_count_text_files():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(os.path.dirname(dir_path), 'data', 'count_files')
    df_got = count_files(data_dir, r'\.txt', False)
    data_expected = [(r'\.txt', 0, '.', 3),
                     (r'\.txt', 1, 'd1', 2),
                     (r'\.txt', 2, 'd1/d2', 2),
                     (r'\.txt', 3, 'd1/d2/d3', 1)]
    df_expected = pd.DataFrame(data_expected, columns=['pattern', 'level', 'name_space', 'count'])
    df_expected['name_space'] = df_expected['name_space'].apply(os.path.normpath)
    assert_frame_equal(df_got, df_expected)

def test_count_and_list_text_files():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(os.path.dirname(dir_path), 'data', 'count_files')
    df_got = count_files(data_dir, r'\.txt', True)
    data_expected = [(r'\.txt', 0, '.', 3, ['analysis.txt', 'f1.txt', 'f7.txt']),
                     (r'\.txt', 1, 'd1', 2, ['f2.txt', 'f6.txt']),
                     (r'\.txt', 2, 'd1/d2', 2, ['f3.txt', 'f4.txt']),
                     (r'\.txt', 3, 'd1/d2/d3', 1, ['f5.txt'])]
    df_expected = pd.DataFrame(data_expected, columns=['pattern', 'level', 'name_space', 'count', 'files'])
    df_expected['name_space'] = df_expected['name_space'].apply(os.path.normpath)
    assert_frame_equal(df_got, df_expected)

def test_count_hidden_files():
    # To ensure that count_files is parsing the hidden directories
    # To ensure that directories with 0 file count are not shown in the output.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(os.path.dirname(dir_path), 'data', 'count_files')
    df_got = count_files(data_dir, r'\.csv', True)
    data_expected = [(r'\.csv', 0, '.', 1, ['c.csv']),
                     (r'\.csv', 1, '.hidden', 1, ['c.csv'])]
    df_expected = pd.DataFrame(data_expected, columns=['pattern', 'level', 'name_space', 'count', 'files'])
    df_expected['name_space'] = df_expected['name_space'].apply(os.path.normpath)
    assert_frame_equal(df_got, df_expected)

def test_count_and_list_all_files():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(os.path.dirname(dir_path), 'data', 'count_files')
    df_got = count_files(data_dir, r'\.*', True)
    data_expected = [(r'\.*', 0, '.', 4, ['analysis.txt', 'c.csv', 'f1.txt', 'f7.txt']),
                     (r'\.*', 1, '.hidden', 1, ['c.csv']),
                     (r'\.*', 1, 'd1', 2, ['f2.txt', 'f6.txt']),
                     (r'\.*', 2, 'd1/d2', 2, ['f3.txt', 'f4.txt']),
                     (r'\.*', 3, 'd1/d2/d3', 1, ['f5.txt'])]
    df_expected = pd.DataFrame(data_expected, columns=['pattern', 'level', 'name_space', 'count', 'files'])
    df_expected['name_space'] = df_expected['name_space'].apply(os.path.normpath)
    assert_frame_equal(df_got, df_expected)
