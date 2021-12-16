import numpy as np
import pandas as pd

def find_low_points(field):
    reverse_field = field.iloc[::-1, ::-1]
    
    diff_from_above = field.diff(axis=0).fillna(-1)
    diff_from_left = field.diff(axis=1).fillna(-1)
    diff_from_below = reverse_field.diff(axis=0).fillna(-1).iloc[::-1, ::-1]
    diff_from_right = reverse_field.diff(axis=1).fillna(-1).iloc[::-1, ::-1]

    less_than_above = diff_from_above < 0
    less_than_left = diff_from_left < 0
    less_than_below = diff_from_below < 0
    less_than_right = diff_from_right < 0

    low_points = (
        less_than_above
        & less_than_left
        & less_than_below
        & less_than_right
    )

    return low_points

def compute_risk_sum(_input):
    field = pd.DataFrame(_input)
    low_points = find_low_points(field)
    risk_levels = field[low_points] + 1
    risk_sum = int(risk_levels.sum().sum())

    return risk_sum

def size_basins(field):
    basin_mask = field < 9

    basin_field = basin_mask.astype(int)
    print(basin_field.shift())
    print((basin_field != basin_field.shift()).cumsum())
    # print(field.groupby((field != field.shift()).cumsum(), axis=0))

def sum_biggest_basins(_input, n):
    field = pd.DataFrame(_input)
    size_basins(field)

def run(_input):

    print('Day 9, Part 1: {}'.format(compute_risk_sum(_input)))

    sum_biggest_basins(_input, 3)
    # print('Day 9, Part 2: {}'.format())
