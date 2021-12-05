import numpy as np
import pandas as pd

def score_bingo_winner(draws, cards, start):
    """
    Score the first bingo card to win.

    draws: List of integers drawn for bingo.
    cards: List of pandas DataFrame bingo cards (5x5).

    Returns score of first bingo card to win.
    """
    winner = False
    winner_card_idx_list = []
    for i in range(start, len(draws)):
        if winner:
            break
        this_draw = draws[:i]
        for c in range(len(cards)):
            card = cards[c]
            matches = card.isin(this_draw)
            if matches.all(axis=0).sum() or matches.all(axis=1).sum():
                score = card[~matches].sum().sum() * this_draw[-1]
                winner = True
                # There could be multiple winners in one draw.
                winner_card_idx_list.append(c)

    return score, winner_card_idx_list, i

def score_last_bingo_winner(draws, cards):
    """
    Score the last bingo card to win.

    draws: List of integers drawn for bingo.
    cards: List of pandas DataFrame bingo cards (5x5).

    Returns score of last bingo card to win.
    """
    i = 5
    while len(cards) >= 1:
        score, winner_card_idx_list, i = score_bingo_winner(draws, cards, i)
        winner_card_idx_list.sort(reverse=True)
        # Remove all the cards that won in this draw.
        for idx in winner_card_idx_list:
            del cards[idx]

    return score




def run(draws, cards):

    winner_score, _, _ = score_bingo_winner(draws, cards, 5)
    print('Day 4, Part 1: {}'.format(winner_score))

    last_winner_score = score_last_bingo_winner(draws, cards)
    print('Day 4, Part 2: {}'.format(last_winner_score))
