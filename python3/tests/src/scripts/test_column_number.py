from src.scripts.column_number import find_column_number
from pathlib import Path


def test_find_existing_column():
    cur_dir = Path(__file__).resolve().parent
    data_dir = cur_dir.parent.parent / "data"
    csv_file = data_dir / "people.csv"
    result = find_column_number(csv_file, 'number')
    assert result == 2


def test_find_nonexistent_column(capsys):
    cur_dir = Path(__file__).resolve().parent
    data_dir = cur_dir.parent.parent / "data"
    csv_file = data_dir / "people.csv"
    result = find_column_number(csv_file, 'NonExistent')
    assert result == -1

    captured = capsys.readouterr()
    assert "not found" in captured.out
