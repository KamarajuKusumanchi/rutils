import pandas as pd
from pandas.testing import assert_frame_equal

from src.scripts.release_history import python_release_history


def test_python_release_history():
    # This test will fail as new python versions are released. To update it
    # with the latest versions, use https://www.python.org/downloads/
    data = {
        'version': ["3.14.3", "3.14.4", "3.14.5", "3.14.6", "3.14.7"],
        'release_date': [
            "2026-02-03",
            "2026-04-07",
            "2026-05-10",
            "2026-06-10",
            "2026-08-05"
        ],
    }

    df_expected = pd.DataFrame(data)
    df_expected['release_date'] = pd.to_datetime(
        df_expected['release_date'], errors="coerce"
    ).dt.date
    df_got = python_release_history(limit=5)
    assert_frame_equal(df_got, df_expected)
