import numpy as np
import pandas as pd

def determine_alignment_constant(_input):
    positions = pd.Series(_input)
    alignment = int(positions.median())
    fuel = (positions - alignment).abs().sum()

    return alignment, fuel

def fuel_func(alignment, positions):
    return (positions - alignment).abs().apply(lambda x: int(x*(x+1)/2)).sum()

def determine_alignment(_input):
    positions = pd.Series(_input)
    domain = range(min(positions), max(positions)+1)
    costs = [fuel_func(alignment, positions) for alignment in domain]
    min_cost = min(costs)
    alignment = costs.index(min_cost) + domain[0]

    return alignment, min_cost

def run(_input):

    alignment, fuel = determine_alignment_constant(_input)
    print('Day 7, Part 1: Alignment {}, Fuel: {}'.format(alignment, fuel))
    alignment, fuel = determine_alignment(_input)
    print('Day 7, Part 2: Alignment {}, Fuel: {}'.format(alignment, fuel))
