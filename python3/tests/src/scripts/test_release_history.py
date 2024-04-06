import pandas as pd
from pandas.testing import assert_frame_equal

from src.scripts.release_history import python_release_history


def test_python_release_history():
    data = {'date': ["2024-02-06", "2023-12-08", "2023-10-02", "2024-02-06", "2023-12-04"],
            'tag': ["3.12.2", "3.12.1", "3.12.0", "3.11.8", "3.11.7"]}
    df_expected = pd.DataFrame(data)
    df_expected['date'] = pd.to_datetime(df_expected['date'], format='%Y-%m-%d')
    df_got = python_release_history(limit=5)
    assert_frame_equal(df_got, df_expected)
