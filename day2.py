import numpy as np
import pandas as pd

def get_resulting_position(horizontal_instructions, depth_instructions):
    """
    Get the resulting horizontal position and depth
    of the submarine after following forward/up/down
    instructions.

    horizontal_instructions: Integer list of horizontal instructions.
    depth_instructions:  Integer list of depth instructions (postive values
            mean greater depth, negative means shallower depth).

    Return: Resulting horizontal position (int), resulting depth
            position (int).
    """
    return sum(horizontal_instructions), sum(depth_instructions)


def get_resulting_position_with_aim(
    horizontal_instructions,
    depth_instructions,
):
    """
    Get the resulting horizontal position and depth
    of the submarine after following forward/up/down
    instructions.

    horizontal_instructions: Integer list of horizontal instructions.
    depth_instructions:  Integer list of depth instructions (postive values
            mean greater depth, negative means shallower depth).

    Return: Resulting horizontal_position (int), resulting depth_position (int).
    """
    horizontal = pd.Series(horizontal_instructions)
    depth = pd.Series(depth_instructions)
    aim = depth.cumsum()
    
    horizontal_position = horizontal.sum()
    depth_position = (aim * horizontal).sum()
    return horizontal_position, depth_position


def run(_input):

    horizontal_instructions, depth_instructions = _input
    horizontal_position, depth_position = get_resulting_position(
        horizontal_instructions,
        depth_instructions
    )

    print('Day 2, Part 1: {}'.format(horizontal_position * depth_position))

    horizontal_position, depth_position = get_resulting_position_with_aim(
        horizontal_instructions,
        depth_instructions
    )

    print('Day 2, Part 2: {}'.format(horizontal_position * depth_position))
