import pandas as pd
from pandas.testing import assert_frame_equal
from datetime import datetime

from src.release_history import python_release_history


def test_python_release_history():
    data = [
        (datetime.strptime("2022-10-24", "%Y-%m-%d").date(), "3.11.0"),
        (datetime.strptime("2022-10-08", "%Y-%m-%d").date(), "3.10.8"),
        (datetime.strptime("2022-09-06", "%Y-%m-%d").date(), "3.10.7"),
        (datetime.strptime("2022-08-08", "%Y-%m-%d").date(), "3.10.6"),
        (datetime.strptime("2022-06-06", "%Y-%m-%d").date(), "3.10.5"),
    ]
    df_expected = pd.DataFrame(data, columns=["date", "tag"])
    # df_expected['date'] = pd.to_datetime(df_expected['date'], format='%Y-%m-%d')
    df_got = python_release_history(limit=5)
    assert_frame_equal(df_got, df_expected)
