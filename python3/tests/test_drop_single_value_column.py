import pandas as pd
import numpy as np
from drop_single_value_columns import drop_single_value_columns
from pandas.testing import assert_frame_equal


def test_drop_single_value_columns():
    df = pd.DataFrame({'A': [None, None],
                       'B': [None, 1],
                       'C': [2, 3],
                       'D': [4, 4]})
    df_got = drop_single_value_columns(df)
    df_expected = pd.DataFrame({'B': [None, 1],
                                'C': [2, 3]})
    assert_frame_equal(df_got, df_expected)
