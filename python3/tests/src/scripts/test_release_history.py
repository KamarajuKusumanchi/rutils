import pandas as pd
from pandas.testing import assert_frame_equal

from src.scripts.release_history import python_release_history


def test_python_release_history():
    data = {'date': ["2022-10-24", "2022-10-08", "2022-09-06", "2022-08-08", "2022-06-06"],
            'tag': ["3.11.0", "3.10.8", "3.10.7", "3.10.6", "3.10.5"]}
    df_expected = pd.DataFrame(data)
    df_expected['date'] = pd.to_datetime(df_expected['date'], format='%Y-%m-%d')
    df_got = python_release_history(limit=5)
    assert_frame_equal(df_got, df_expected)
