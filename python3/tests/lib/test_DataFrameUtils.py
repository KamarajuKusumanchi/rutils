import pandas as pd
from lib.DataFrameUtils import print_without_index


def test_print_without_index(capsys):
    row1 = (123, "2014-07-08 00:09:00", 1411)
    row2 = (123, "2014-07-08 00:49:00", 1041)
    row3 = (123, "2014-07-08 00:09:00", 1411)
    data = [row1, row2, row3]
    # set up dataframe
    df = pd.DataFrame(data, columns=("User ID", "Enter Time", "Activity Number"))

    # see https://docs.pytest.org/en/latest/capture.html#accessing-captured-output-from-a-test-function
    # for help on how capsys works in pytest.
    print_without_index(df)
    captured = capsys.readouterr()
    expected_out = (
        "  User ID           Enter Time  Activity Number\n"
        + "      123  2014-07-08 00:09:00             1411\n"
        + "      123  2014-07-08 00:49:00             1041\n"
        + "      123  2014-07-08 00:09:00             1411\n"
    )
    assert captured.out == expected_out
