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


@pytest.mark.parametrize('s, result', [
    (pd.Series([3, 4, 3, 3]), False),
    (pd.Series([2, 2, 2, None]), False),
    (pd.Series([2,2, 2, 2]), True),
    (pd.Series([None]), True),
    (pd.Series([np.nan]), True),
    (pd.Series([None, None]), True),
    (pd.Series([None, np.nan]), True),
    (pd.Series([np.nan, np.nan]), True)
])
def test_is_series_single_valued(s, result):
    assert is_series_single_valued(s) == result


if __name__ == '__main__':
    # https://stackoverflow.com/questions/35353771/invoke-pytest-from-python-for-current-module-only shows how to
    # invoke pytest on the current file itself.
    pytest.main(sys.argv)
