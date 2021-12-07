import numpy as np
import pandas as pd

# Inefficient
def age(fish_state):
    n_spawn = (fish_state == 0).sum()
    fish_state -= 1
    fish_state[fish_state < 0] = 6
    return fish_state.append(pd.Series([8]*n_spawn))


class Model:
    def __init__(self):
        self.memo = {}

    def spawn(self, fish_state, n_days):
        
        if (fish_state, n_days) in self.memo:
            return self.memo[(fish_state, n_days)]
        elif n_days <= fish_state:
            total_spawn = 0
        else:
            n_direct_spawn = int((n_days - (fish_state + 1)) / 7) + 1
            # indirect_spawn = [i for i in range(fish_state, n_days, 7)]
            n_indirect_spawn = sum(
                [
                    self.spawn(
                        8,
                        n_days - i - 1
                    ) 
                    for i in range(fish_state, n_days, 7)
                ]
            )
            total_spawn = n_direct_spawn + n_indirect_spawn
        self.memo[(fish_state, n_days)] = total_spawn
        return total_spawn



def model_lanternfish(_fish_state, n_days, fast=False):

    fish_state = pd.Series(_fish_state)

    if not fast:
        for d in range(n_days):
            # Provide the population size from 2 days ago (or 0th day).
            fish_state = age(fish_state)

        return len(fish_state)
    else:
        model = Model()
        initial_pop = len(_fish_state)
        spawned = sum([model.spawn(s, n_days) for s in _fish_state])
        return initial_pop + spawned




def run(_input):

    n_fish = model_lanternfish(_input, 80, fast=False)
    print('Day 6, Part 1: {}'.format(n_fish))

    n_fish2 = model_lanternfish(_input, 256, fast=True)
    print('Day 6, Part 2: {}'.format(n_fish2))
