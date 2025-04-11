# battleship/game_logic.py
import random

def initialize_game():
    board = [['~'] * 5 for _ in range(5)]
    ship_row = random.randint(0, 4)
    ship_col = random.randint(0, 4)
    board[ship_row][ship_col] = 'S'  # S de Ship, se puede ocultar después
    return {
        'board': board,
        'hits': [],
        'message': 'Game started. Enter row and column to fire.'
    }

def process_move(board, hits, row, col):
    row, col = int(row), int(col)

    if [row, col] in hits:
        return {'board': board, 'hits': hits, 'message': 'Already tried this position.'}

    hits.append([row, col])

    if board[row][col] == 'S':
        board[row][col] = 'X'
        return {'board': board, 'hits': hits, 'message': 'Hit! You sank the ship!'}
    else:
        board[row][col] = 'O'
        return {'board': board, 'hits': hits, 'message': 'Miss. Try again.'}
