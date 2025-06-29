# ai_module.py

def get_ai_move(board):
    winning_lines = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    # Try to win
    for a, b, c in winning_lines:
        line = [board[a], board[b], board[c]]
        if line.count("O") == 2 and line.count("") == 1:
            return [a, b, c][line.index("")]
    # Block X
    for a, b, c in winning_lines:
        line = [board[a], board[b], board[c]]
        if line.count("X") == 2 and line.count("") == 1:
            return [a, b, c][line.index("")]
    # Center
    if board[4] == "":
        return 4
    # Corners
    for i in [0, 2, 6, 8]:
        if board[i] == "":
            return i
    # Sides
    for i in [1, 3, 5, 7]:
        if board[i] == "":
            return i
    return -1  # fallback
