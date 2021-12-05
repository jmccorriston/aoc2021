import numpy as np
import pandas as pd

def binary_to_decimal(bit_series):
    bit_string = ''.join([str(i) for i in bit_series])
    return int(bit_string, 2)

def compute_gamma_and_epsilon(diagnostic_report):
    """
    Determine the gamma rate based on the diagnostic report.

    gamma_value: Integer gamma value (in base 10).
    epsilon_value: Integer epsilon value (in base 10).
    """
    diagnostics = pd.DataFrame(diagnostic_report)
    inverted_diagnostics = 1 - diagnostics

    gamma_series = diagnostics.mode(axis=0).values[0]
    epsilon_series = 1 - gamma_series
    gamma_value = binary_to_decimal(gamma_series)
    epsilon_value = binary_to_decimal(epsilon_series)
    return gamma_value, epsilon_value

def compute_o2_and_co2_rating(diagnostic_report):
    diagnostics = pd.DataFrame(diagnostic_report)

    o2_series = gas_rating_recursive(diagnostics, 0, 'o2')
    o2_value = binary_to_decimal(o2_series)

    co2_series = gas_rating_recursive(diagnostics, 0, 'co2')
    co2_value = binary_to_decimal(co2_series)

    return o2_value, co2_value


def gas_rating_recursive(diagnostics, unit, mode):
    """
    Perform the recusive gas diagnostics computation.

    diagnostics:    Pandas DataFrame containing all the rows of the diagnostics
                    report.
    unit:           Unit in the binary number currently being examined (note
                    that 0 is actually the 0th position from left to right,
                    which is actually the largest unit).
    mode:           'o2' to compute oxygen rating, 'co2' to compute co2 rating.

    Returns either a recursive call to this method, incrementing the unit by 1,
    or the final oxygen rating.
    """

    if len(diagnostics) == 1:
        return diagnostics.values[0]
    else:

        gas_filter = diagnostics[unit].mode()
        if len(gas_filter) > 1:
            gas_filter = gas_filter.values[1]
        else:
            gas_filter = gas_filter.values[0]
        if mode == 'co2':
            gas_filter = 1 - gas_filter
        return gas_rating_recursive(
            diagnostics[diagnostics[unit] == gas_filter],
            unit+1,
            mode
        )

def co2_rating_recursive(diagnostics, unit):
    """
    Perform the recusive co2 diagnostics computation.

    diagnostics:    Pandas DataFrame containing all the rows of the diagnostics
                    report.
    unit:           Unit in the binary number currently being examined (note
                    that 0 is actually the 0th position from left to right,
                    which is actually the largest unit).

    Returns either a recursive call to this method, incrementing the unit by 1,
    or the final co2 rating.
    """

    if len(diagnostics == 1):
        return int(''.join([str(i) for i in diagnostics.values[0]]), 2)
    else:
        co2_filter = diagnostics[unit].value_counts().index[-1]
        if len(co2_filter) > 1:
            co2_filter = co2_filter[0]
        return(diagnostics[diagnostics[unit] == o2_filter], unit+1)

def run(_input):

    gamma_value, epsilon_value = compute_gamma_and_epsilon(_input)

    print('Day 3, Part 1: {}'.format(gamma_value * epsilon_value))

    o2_value, co2_value = compute_o2_and_co2_rating(_input)
    print('Day 3, Part 2: {}'.format(o2_value * co2_value))
