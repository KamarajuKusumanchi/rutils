# remove columns with the same value
import pandas as pd
import sys

# Todo:- How to extend this concept when grouping on some index columns.
# For example, consider
# df = pd.DataFrame({'id': [1, 1, 2, 2, 3, 3],
#                    'fld': [4, 4, 5, 5, 6, 6],
#                    'A':[None, None, None, None, None, None],
#                    'B': [None, 1, 1, 1, None, 1],
#                    'C': [2,3, 2, 3, 4, 4],
#                    'D': [4,4, 4, 5, 6, 7]})
# grps = df.groupby(['id', 'fld'])
# For group in grps, we want to apply the drop_single_value_columns
# function, then aggregate the results back up



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
