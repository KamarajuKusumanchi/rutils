import pandas as pd
import numpy as np

import pytest
import sys


def is_series_single_valued(s):
    # Note:- https://stackoverflow.com/questions/54405704/check-if-all-values-in-dataframe-column-are-the-same
    # gives the following solution. It is fast but fails in some corner cases.
    # The solution they propose is
    #
    # a = s.to_numpy() # s.values (pandas<0.24)
    # return (a[0] == a).all()
    #
    # But for series such as
    #   pd.Series([None, np.nan])
    #   pd.Series([np.nan, np.nan])
    # it gives False. But I want that to be True.
    #
    return s.drop_duplicates().size == 1


@pytest.mark.parametrize(
    "s, result",
    [
        (pd.Series([3, 4, 3, 3]), False),
        (pd.Series([2, 2, 2, None]), False),
        (pd.Series([2, 2, 2, 2]), True),
        (pd.Series([None]), True),
        (pd.Series([np.nan]), True),
        (pd.Series([None, None]), True),
        (pd.Series([None, np.nan]), True),
        (pd.Series([np.nan, np.nan]), True),
    ],
)
def test_is_series_single_valued(s, result):
    assert is_series_single_valued(s) == result


class NotOne(ValueError):
    # Borrowed this idea from https://github.com/owid/covid-19-data/blob/master/scripts/scripts/utils/db_utils.py
    pass

def get_unique_value(s):
    # If s is a single valued Series, return that value. Otherwise throw an error.
    unique = s.drop_duplicates()
    if unique.size != 1:
        raise NotOne('Expected 1 unique value but got %d' % (unique.size))
    else:
        return unique[0]

def test_get_unique_value():
    s1 = pd.Series([3, 3, 3, 3])
    assert get_unique_value(s1) == 3
    s2 = pd.Series([None, None, None])
    assert get_unique_value(s2) is None
    s3 = pd.Series([np.nan, np.nan])
    assert np.isnan(get_unique_value(s3))

    # See https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/metrics/tests/test_pairwise.py to get an
    # idea of how to test for an exception.
    s4 = pd.Series([3, 3, None, 3])
    err_msg = 'Expected 1 unique value but got 2'
    with pytest.raises(NotOne, match=err_msg):
        get_unique_value(s4)

if __name__ == "__main__":
    # https://stackoverflow.com/questions/35353771/invoke-pytest-from-python-for-current-module-only shows how to
    # invoke pytest on the current file itself.
    pytest.main(sys.argv)
