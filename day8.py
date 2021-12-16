import numpy as np
import pandas as pd
from collections import Counter

DIGIT_NUM_SEGS = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}

REAL_SEGS_TO_DIGIT = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}

REAL_DIGIT_SEGS = {
    0: set(['a', 'b', 'c', 'e', 'f', 'g']),
    1: set(['c', 'f']),
    2: set(['a', 'c', 'd', 'e', 'g']),
    3: set(['a', 'c', 'd', 'f', 'g']),
    4: set(['b', 'c', 'd', 'f']),
    5: set(['a', 'b', 'd', 'f', 'g']),
    6: set(['a', 'b', 'd', 'e', 'f', 'g']),
    7: set(['a', 'c', 'f']),
    8: set(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
    9: set(['a', 'b', 'c', 'd', 'f', 'g']),
}

def get_unique_seg_lens():
        # Organize digits by number of segments.
    digits_per_num_segs = {}
    for digit in DIGIT_NUM_SEGS:
        num_segs = DIGIT_NUM_SEGS[digit]
        if num_segs in digits_per_num_segs:
            digits_per_num_segs[num_segs].add(digit)
        else:
            digits_per_num_segs[num_segs] = set([digit])

    # Convert from sets of digits to lists.
    digits_per_num_segs = {k: list(v) for k, v in digits_per_num_segs.items()}

    # Get all the lengths of digits with a unique number of segment lengths.
    unique_num_segs = set()
    for num_segs in digits_per_num_segs:
        if len(digits_per_num_segs[num_segs]) == 1:
            unique_num_segs.add(num_segs)

    return unique_num_segs, digits_per_num_segs

def count_unique_seg_outputs(output_lines):

    unique_num_segs, _ = get_unique_seg_lens()

    # Count number of occurrences of digits with unique segment lengths in
    # outputs.
    count_unique_seg_len_digits = 0

    for outputs in output_lines:
        for output in outputs:
            if len(output) in unique_num_segs:
                count_unique_seg_len_digits += 1


    return count_unique_seg_len_digits

# def decrypt_seg(dig1, dig2, current_digit_segs, current_seg_key):
#     curr_diff = current_digit_segs[dig1] - current_digit_segs[dig2]

#     if len(curr_diff) == 1:
#         curr_diff = next(iter(curr_diff))
#         if curr_diff not in current_seg_key:
#             real_diff = REAL_DIGIT_SEGS[dig1] - REAL_DIGIT_SEGS[dig2]
#             real_diff = next(iter(real_diff))
#             current_seg_key[curr_diff] = real_diff

#     return current_seg_key

def decrypt_seg(dig1, dig2, current_seg_key):
    curr_diff = set(dig1) - set(dig2)

    if len(curr_diff) == 1:
        curr_diff = next(iter(curr_diff))
        if curr_diff not in current_seg_key:
            real_diff = REAL_DIGIT_SEGS[dig1] - REAL_DIGIT_SEGS[dig2]
            real_diff = next(iter(real_diff))
            current_seg_key[curr_diff] = real_diff

    return current_seg_key


def decrypt_and_sum(inputs, outputs):

    unique_num_segs, digits_per_num_segs = get_unique_seg_lens()
    num_lines = len(inputs)
    sum_total = 0

    for i in range(num_lines):
        current_answer_key = {}
        all_digits = inputs[i] + outputs[i]
        for d in all_digits:
            if len(d) == 2:
                one = set(d)
            elif len(d) == 3:
                seven = set(d)
            elif len(d) == 4:
                four = set(d)
            elif len(d) == 7:
                eight = set(d)

        # Decode d, b, a, g, f, e, then c.
        # current_answer_key[solve_a(one, seven)] = 'a'
        current_answer_key[solve_d(all_digits, seven)] = 'd'
        current_answer_key[solve_b(
            all_digits,
            one,
            current_answer_key.keys()
        )] = 'b'
        current_answer_key[solve_a(one, seven)] = 'a'
        current_answer_key[solve_g(
            all_digits,
            one,
            current_answer_key.keys()
        )] = 'g'
        current_answer_key[solve_f(all_digits, current_answer_key.keys())] = 'f'
        current_answer_key[solve_e(
            all_digits,
            one,
            current_answer_key.keys()
        )] = 'e'
        current_answer_key[solve_c(all_digits, current_answer_key.keys())] = 'c'

        decoded_digits = []

        # Decrypt each digit and multiply based on unit position.
        multipliers = [1, 10, 100, 1000]
        for d in outputs[i]:
            decoded_seg = ''
            for char in d:
                decoded_seg += current_answer_key[char]
            decoded_digit = REAL_SEGS_TO_DIGIT[''.join(sorted(decoded_seg))]
            decoded_digits.append(decoded_digit)
            sum_total += decoded_digit * multipliers.pop()
        
    return sum_total


def solve_a(one, seven):
    return (set(seven) - set(one)).pop()

def solve_d(digits, seven):
    digs = digits
    three_or_four = set()
    for dig in digs:
        d = set(dig)
        for seg in seven:
            d.discard(seg)
        if len(d) == 2:
            s = list(d)
            if (s[0] in three_or_four) and (s[1] not in three_or_four):
                return s[0]
            elif (s[1] in three_or_four) and (s[0] not in three_or_four):
                return s[1]
            else:
                three_or_four.add(s[0])
                three_or_four.add(s[1])

def solve_next(digits, unique_num, solved):
    digs = digits
    for dig in digs:
        d = set(dig)
        for seg in unique_num:
            d.discard(seg)
        for seg in solved:
            d.discard(seg)
        if len(d) == 1:
            return d.pop()

def solve_b(digits, one, solved):
    digs = digits
    for dig in digs:
        if len(dig) != 3:
            d = set(dig)
            for seg in one:
                d.discard(seg)
            for seg in solved:
                d.discard(seg)
            if len(d) == 1:
                return d.pop()

def solve_g(digits, seven, solved):
    return solve_next(digits, seven, solved)

def solve_f(digits, solved):
    digs = digits
    for dig in digs:
        d = set(dig)
        for seg in solved:
            d.discard(seg)
        if len(d) == 1:
            return d.pop()

def solve_e(digits, seven, solved):
    return solve_next(digits, seven, solved)

def solve_c(digits, solved):
    digs = digits
    for dig in digs:
        d = set(dig)
        for seg in solved:
            d.discard(seg)
        if len(d) == 1:
            return d.pop()



# Used to manually test different solution progressions.
def test():
    segs = REAL_DIGIT_SEGS
    for i in segs.values():
        print(len(i))

    for d in segs:
        segs[d].discard('a')
        segs[d].discard('b')
        # segs[d].discard('f')
        # segs[d].discard('c')
        segs[d].discard('d')
        segs[d].discard('g')
        segs[d].discard('e')

    print(segs)

    for i in segs.values():
        print(len(i))

def run(inputs, outputs):

    unique_seg_outputs = count_unique_seg_outputs(outputs)

    print('Day 8, Part 1: {}'.format(unique_seg_outputs))

    # test()
    total = decrypt_and_sum(inputs, outputs)
    print('Day 8, Part 2: {}'.format(total))
