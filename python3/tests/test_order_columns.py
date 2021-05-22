import os
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from order_columns import order_columns


@pytest.fixture(name='df', scope='module')
def initialize():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(test_dir, 'data')
    file_name = os.path.join(test_data_dir, 'people.csv')
    df = pd.read_csv(file_name, dtype='str')
    return df


def test_order_columns_raw(df):
    df_got = order_columns(df, strip_spaces=False, reverse=False)
    df_expected = df[['    name', '  address', '  number']]
    assert_frame_equal(df_got, df_expected)


def test_order_columns_strip(df):
    df_got = order_columns(df, strip_spaces=True, reverse=False)
    df_expected = df[['  address', '    name', '  number']]
    assert_frame_equal(df_got, df_expected)


def test_order_columns_raw_reverse(df):
    df_got = order_columns(df, strip_spaces=False, reverse=True)
    df_expected = df[['  number', '  address', '    name']]
    assert_frame_equal(df_got, df_expected)


def test_order_columns_strip_reverse(df):
    df_got = order_columns(df, strip_spaces=True, reverse=True)
    df_expected = df[['  number', '    name', '  address']]
    assert_frame_equal(df_got, df_expected)
