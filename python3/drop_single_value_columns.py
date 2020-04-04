# remove columns with the same value
import pandas as pd
import sys


def drop_single_value_columns(df):
    nunique = df.apply(pd.Series.nunique)
    # pd.Series.nunique does not count None values.
    # So if all values in a column are missing, then nunique will return 0.
    # To account for such columns, add 1 if there is a NaN anywhere in the column.
    nunique += df.isna().any().astype(int)
    cols_to_drop = nunique[nunique == 1].index
    result = df.drop(cols_to_drop, axis=1)
    return result


if __name__ == '__main__':
    df = pd.read_csv(sys.stdin)
    # df.to_csv(sys.stdout, index=False)
    df2 = drop_single_value_columns(df)
    df2.to_csv(sys.stdout, index=False)
