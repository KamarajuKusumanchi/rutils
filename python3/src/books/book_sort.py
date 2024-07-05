import os

import pandas as pd
import sys

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = dir_path
    ratings_file_name = 'book_ratings.csv'
    ratings_file_path = os.path.join(data_dir, ratings_file_name)
    ratings = pd.read_csv(ratings_file_path, comment='#')
    # print(ratings)
    book_list = sys.stdin.read().splitlines()
    book_df = pd.DataFrame({'book': book_list})
    book_df = book_df.merge(ratings, on=['book'], how='left')
    book_df['rating'].fillna(0, inplace=True)
    book_df.sort_values(by=['rating'], ascending=False, inplace=True)
    [print(x) for x in book_df['book'].values]
