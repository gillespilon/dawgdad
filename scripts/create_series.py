#! /usr/bin/env python3
"""
Create a Pandas series.

A series of type integer can contain np.nan if it's Int64 (nullable type),
not int64.

It's too early to switch to pd.NA for missing values.

./create_series.py > create_series.txt

TODO:
- Ensure each example has:
    1. pd.Series example
    2. dd.random_data example
"""

import random

from pandas.api.types import CategoricalDtype
import pandas as pd
import numpy as np

import dawgdad as dd


def main():
    header_title = 'Create series'
    header_id = 'create-series'
    output_url = 'create_series.html'
    original_stdout = dd.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    print('Create Pandas series')
    print()
    print('uniform distribution, dtype: float, list_a, series_a')
    # series_a = dd.random_data(
    #     distribution='uniform',
    #     size=7,
    #     loc=13,
    #     scale=70
    # ).rename('A')
    list_a = [14.758, 78.956, np.nan, 57.361, 39.018, 75.764, 65.869]
    print(list_a)
    series_a = pd.Series(
        data=list_a,
        name='A'
    ).astype(dtype='float64')
    print(series_a)
    print()
    print('boolean distribution, dtype: boolean (nullable), list_b, series_b')
    # series_b = dd.random_data(
    #     distribution='bool',
    #     size=7
    # ).rename('B')
    list_b = [False, True, np.nan, False, True, True, False]
    print(list_b)
    series_b = pd.Series(
        data=list_b,
        name='B'
    ).astype(dtype='boolean')
    print(series_b)
    print()
    print('category distribution, dtype: category, list_c, series_c')
    # series_c = dd.random_data(
    #     distribution='category,
    #     size=7'
    # ).rename('C')
    # print(series_c.head())
    list_c = ['small', 'medium', '', 'medium', 'large', 'large', 'small']
    print(list_c)
    series_c = pd.Series(
        data=list_c,
        name='C'
    ).astype(dtype='category')
    print(series_c)
    print()
    print('C dtype:', series_c.dtype)
    print()
    print('C dtype:', type(series_c.dtype).__name__)
    print()
    print('category distribution, dtype: category, list_c, series_c')
    # series_c = dd.random_data(
    #     distribution='categories,
    #     size=7'
    # ).rename('C')
    # print(series_c.head())
    list_cs = ['small', 'medium', '', 'medium', 'large', 'large', 'small']
    categories = ['small', 'medium', 'large']
    print(list_cs)
    print()
    size = 13
    random_state = 42
    random.seed(a=random_state)
    series_cs = pd.Series(
        data=random.choices(
            population=list_cs,
            k=size
        ),
        name='CS'
    ).astype(
        dtype=CategoricalDtype(
            categories=categories,
            ordered=True
        )
    )
    print(series_cs)
    print()
    print('CS dtype:', series_cs.dtype)
    print()
    print('CS dtype:', type(series_cs.dtype).__name__)
    print()
    print('timedelta distribution, dtype: timedelta64[ns], list_d, series_d')
    # series_d = dd.random_data(
    #     distribution='timedelta',
    #     size=7
    # ).rename('D')
    list_d = [0, 0, pd.NaT, 0, 0, 0, 0 ]
    print(list_d)
    series_d = pd.Series(
        data=list_d,
        name='D'
    ).astype(dtype='timedelta64[ns]')
    print(series_d)
    print()
    print('uniform distribution, dtype: float64, list_i, series_i')
    # series_i = dd.random_data(
    #     distribution='uniform',
    #     size=7,
    #     loc=13,
    #     scale=70
    # ).rename('I')
    list_i = [
        6.554271, 23.958127, np.nan, 58.231292, 67.349036, 75.083105, 30.503073
    ]
    print(list_i)
    series_i = pd.Series(
        data=list_i,
        name='I'
    ).astype(dtype='float64')
    print(series_i)
    print()
    print('strings distribution, dtype:str, list_r, series_r')
    # series_r = dd.random_data(
    #     distribution='strings',
    #     strings=['0', '1'],
    #     size=7
    # ).rename('R')
    list_r = ['1', '1', '', '0', '0', '1']
    print(list_r)
    series_r = pd.Series(
        data=list_r,
        dtype='str',
        name='R'
    ).astype(dtype='str')
    print('series_r:')
    print(series_r)
    print()
    print('strings distribution, dtype:str, list_s, series_3')
    # series_s = dd.random_data(
    #     distribution='strings',
    #     size=7
    # ).rename('S')
    list_s = ['male', 'female', '', 'male', 'female', 'female', 'male']
    print(list_s)
    series_s = pd.Series(
        data=list_s,
        dtype='str',
        name='S'
    ).astype(dtype='str')
    print('series_s:')
    print(series_s)
    print()
    print('datetime distribution, dtype: datetime64[ns], list_t, series_t')
    # series_t = dd.random_data(
    #     distribution='datetime',
    #     size=7
    # ).rename('T')
    list_t = [
        '2020-12-12 16:33:48', '2020-12-13 16:33:48', pd.NaT,
        '2020-12-15 16:33:48', '2020-12-16 16:33:48', '2020-12-17 16:33:48',
        '2020-12-18 16:33:48'
    ]
    print(list_t)
    series_t = pd.Series(
        data=list_t,
        name='T'
    ).astype(dtype='datetime64[ns]')
    print(series_t)
    print()
    print('normal distribution, dtype: float64, list_x, series_x')
    # series_x = dd.random_data(
    #     distribution='norm',
    #     size=7,
    #     loc=69,
    #     scale=13
    # ).rename('X')
    list_x = [42.195, 82.630, np.nan, 86.738, 85.656, 79.281, 50.015]
    print(list_x)
    series_x = pd.Series(
        data=list_x,
        dtype='float64',
        name='X'
    ).astype(dtype='float64')
    print(series_x)
    print()
    print('integer distribution, dtype: Int64 (nullable), list_y, series_y')
    # series_y = dd.random_data(
    #     distribution='randint',
    #     size=7,
    #     low=0,
    #     high=2
    # ).rename('Y')
    list_y = [1, 0, 1, np.nan, 1, 0, 0]
    print(list_y)
    series_y = pd.Series(
        data=list_y,
        name='Y'
    ).astype(dtype='Int64')
    print(series_y)
    print()
    dd.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


if __name__ == '__main__':
    main()
