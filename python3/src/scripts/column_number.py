#! /usr/bin/env python3
"""Find the column number of a column in a CSV file."""

# Sample command:
# <script_name> foo.csv bar
#
# Related commands:
#   head -n1 foo.csv | tr ',' '\n' | nl
# will give column numbers for all the columns.

import typer
import pandas as pd

app = typer.Typer()


def find_column_number(csv_file: str, column_name: str) -> int:
    """Find the column number of a specific column in a CSV file."""

    # nrows=0 tells pandas to read only the header without loading any data rows.
    df = pd.read_csv(csv_file, nrows=0)
    df.columns = df.columns.str.strip()

    if column_name not in df.columns:
        print(f"Column '{column_name}' not found")
        print(f"Available columns: {list(df.columns)}")
        return -1

    return df.columns.get_loc(column_name) + 1


@app.command()
def main(csv_file: str, column_name: str):
    """Find the column number of a specific column in a CSV file."""
    col_number = find_column_number(csv_file, column_name)

    if col_number > 0:
        print(f"Column '{column_name}' is at position: {col_number}")


if __name__ == "__main__":
    app()
