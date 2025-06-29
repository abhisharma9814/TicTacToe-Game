# game_logic.py

def check_winner(board):
    win_combos = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in win_combos:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None

def switch_player(current):
    return "O" if current == "X" else "X"

def is_draw(board):
    return "" not in board

def reset_board():
    return [""] * 9, []
