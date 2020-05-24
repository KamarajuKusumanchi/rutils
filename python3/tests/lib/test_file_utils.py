import os

import pytest

from lib.file_utils import find_files_by_pattern


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
