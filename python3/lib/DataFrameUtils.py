import pandas as pd


def print_without_index(df: pd.DataFrame):
    # print dataframe without index
    # Got the idea from https://stackoverflow.com/questions/24644656/how-to-print-pandas-dataframe-without-index
    blank_index = [""] * len(df)
    original_index = df.index
    df.index = blank_index
    print(df)
    df.index = original_index


def ljust(s: pd.Series) -> pd.Series:
    # Left justify a column
    # Initial version is from https://stackoverflow.com/questions/74824553/how-to-left-align-column-values-in-pandas-to-string
    s = s.astype(str).str.strip()
    return s.str.ljust(s.str.len().max())
