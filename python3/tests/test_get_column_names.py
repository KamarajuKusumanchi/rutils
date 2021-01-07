import os

import get_column_names


def test_column_names(capsys):
    # see https://docs.pytest.org/en/latest/capture.html#accessing-captured-output-from-a-test-function
    # for help on how capsys works in pytest.
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(test_dir, "data")
    file_name = os.path.join(test_data_dir, "marks.csv")

    get_column_names.main(file_name)
    captured = capsys.readouterr()

    output_expected = "Name\nAge\nCity\nMarks\n"
    assert captured.out == output_expected
