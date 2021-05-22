import os
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

from col_row import get_col_rows


def test_get_col_rows():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(test_dir, 'data')
    file_name = os.path.join(test_data_dir, 'marks.csv')
    df = pd.read_csv(file_name, dtype='str')\
        .rename(columns=lambda x: x.strip())\
        .apply(lambda x: x.str.strip())
    values = ['31', '81', 'Veena']
    df_got = get_col_rows(df, values)
    df_expected = pd.DataFrame({'row': [6, 3, 5, 6, 4],
                                'column': ['Name', 'Age', 'Age', 'Age', 'Marks'],
                                'value': ['Veena', '31', '31', '81', '81']})
    df_expected['row'] = df_expected['row'].astype(np.int)
    assert_frame_equal(df_got, df_expected)
