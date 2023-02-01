import pandas as pd


def print_without_index(df: pd.DataFrame):
    # print dataframe without index
    # Got the idea from https://stackoverflow.com/questions/24644656/how-to-print-pandas-dataframe-without-index
    blank_index = [""] * len(df)
    original_index = df.index
    df.index = blank_index
    print(df)
    df.index = original_index
