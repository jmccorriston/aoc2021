import pandas as pd
import day1, day2, day3, day4

def parse_int_list(input):
    l = input.split('\n')
    l.remove('')
    return [int(i) for i in l]

def parse_movement_instructions(input):
    horizontal = []
    depth = []
    for l in input.split('\n'):
        if l:
            direction, value = l.split(' ')
            if direction == 'up':
                depth.append(-1 * int(value))
                horizontal.append(0)
            elif direction == 'down':
                depth.append(int(value))
                horizontal.append(0)
            elif direction == 'forward':
                depth.append(0)
                horizontal.append(int(value))

    return horizontal, depth

def parse_diagnostics(input):
    diagnostics = []
    for l in input.split('\n'):
        if l:
            diagnostics.append([int(i) for i in l])

    return diagnostics

def parse_bingo(input_lines):
    draws = [int(i) for i in input_lines[0].strip().split(',')]
    cards = []
    card = []

    for l in input_lines[1:]:
        if len(l.strip()) > 0:
            card.append([int(i)for i in l.strip().split(' ') if i])
        else:
            if len(card) > 0:
                cards.append(pd.DataFrame(card))
            card = []
    cards.append(pd.DataFrame(card))

    return draws, cards


def run_day1():

    f = open('inputs/day1.txt')
    day1.run(parse_int_list(f.read()))
    f.close()

def run_day2():
    f = open('inputs/day2.txt')
    day2.run(parse_movement_instructions(f.read()))
    f.close()

def run_day3():
    f = open('inputs/day3.txt')
    day3.run(parse_diagnostics(f.read()))
    f.close()

def run_day4():
    f = open('inputs/day4.txt')
    draws, cards = parse_bingo(f.readlines())
    day4.run(draws, cards)
    f.close()

if __name__ == "__main__":
    
     # run_day1()
     # run_day2()
     # run_day3()
     run_day4()

