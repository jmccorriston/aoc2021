import numpy as np
import pandas as pd

def count_depth_increases(depths):
    """
    Count the number of decreases in depth.

    depths: List of integer depths.
    """
    return pd.Series(depths).diff().gt(0).sum()


def count_rolling_depth_increases(depths, window_length=3):
    """
    Count the number of decreases in depth using rolling
    window sums of depth.

    depths: List of integer depths.
    window_length: Integer length of rolling windows.
    """
    rolling_depth_sums = pd.Series(depths).rolling(3).sum()
    return rolling_depth_sums.diff().gt(0).sum()


def run(_input):

    print('Day 1, Part 1: {}'.format(count_depth_increases(_input)))
    print('Day 1, Part 2: {}'.format(count_rolling_depth_increases(_input)))

