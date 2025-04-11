# slot/game_logic.py
import random

symbols = ['🍒', '🍉', '🍋', '🍏']

def spin_row():
    return [random.choice(symbols) for _ in range(3)]

def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == '🍒':
            return bet * 5
        elif row[0] == '🍉':
            return bet * 10
        elif row[0] == '🍏':
            return bet * 20
        elif row[0] == '🍋':
            return bet * 50
    return 0
