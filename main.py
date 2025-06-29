import tkinter as tk
from tkinter import messagebox
import platform
import os

# === Global Variables ===
current_player = "X"  # Current turn tracker
board = [""] * 9      # 3x3 Tic Tac Toe board
buttons = []          # Button references
scores = {"X": 0, "O": 0, "Ties": 0}  # Score tracker
move_history = []     # For undo feature
player_names = {"X": "Player 1", "O": "Player 2"}  # Default player names
selected_mode = ""
selected_mark = ""

# === Sound on click ===
def play_click_sound():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.MessageBeep()
        else:
            os.system('afplay /System/Library/Sounds/Pop.aiff')
    except:
        pass

# === Start game with chosen mark and mode ===
def start_game(mark, mode):
    global current_player, board, selected_mode, selected_mark, move_history
    current_player = mark
    board = [""] * 9
    selected_mode = mode
    selected_mark = mark
    move_history = []
    show_board(mode)

# === Welcome screen for player names, mark, mode ===
def welcome_screen():
    def start():
        name_x = entry_x.get().strip() or "Player X"
        name_o = entry_o.get().strip() or "Player O"
        mark = mark_var.get()
        mode = mode_var.get()

        if not mark or not mode:
            messagebox.showwarning("Missing Info", "Please select mark and mode.")
            return

        player_names["X"] = name_x
        player_names["O"] = name_o
        welcome.destroy()
        start_game(mark, mode)

    welcome = tk.Tk()
    welcome.title("Tic Tac Toe")
    welcome.geometry("400x500")
    welcome.configure(bg="#1e272e")

    # Title
    tk.Label(welcome, text="TIC TAC TOE", font=("Arial", 24), bg="#1e272e", fg="cyan").pack(pady=10)

    # Player names
    tk.Label(welcome, text="Enter Player X Name:", bg="#1e272e", fg="white").pack()
    entry_x = tk.Entry(welcome)
    entry_x.pack(pady=5)

    tk.Label(welcome, text="Enter Player O Name:", bg="#1e272e", fg="white").pack()
    entry_o = tk.Entry(welcome)
    entry_o.pack(pady=5)

    # Mark selection
    tk.Label(welcome, text="Choose Your Mark", bg="#1e272e", fg="white").pack(pady=(10, 5))
    mark_var = tk.StringVar()
    tk.Radiobutton(welcome, text="X", variable=mark_var, value="X", bg="#1e272e", fg="white").pack()
    tk.Radiobutton(welcome, text="O", variable=mark_var, value="O", bg="#1e272e", fg="white").pack()

    # Mode selection
    tk.Label(welcome, text="Choose Game Mode", bg="#1e272e", fg="white").pack(pady=(20, 5))
    mode_var = tk.StringVar()
    tk.Button(welcome, text="Play vs Player", command=lambda: [mode_var.set("PvP"), start()]).pack(pady=5)
    tk.Button(welcome, text="Play vs AI", command=lambda: [mode_var.set("PvBot"), start()]).pack(pady=5)

    welcome.mainloop()

# === Click handler ===
def on_click(index, window, mode, turn_label, score_label):
    global current_player
    if board[index] != "":
        return

    play_click_sound()
    board[index] = current_player
    move_history.append((index, current_player))

    buttons[index].config(text=current_player, state="disabled",
                          bg="#1abc9c" if current_player == "X" else "#f39c12",
                          disabledforeground="white")

    winner = check_winner()
    if winner:
        scores[winner] += 1
        messagebox.showinfo("Game Over", f"{player_names[winner]} wins!")
        update_score(score_label)
        reset_board(turn_label)
        return

    if "" not in board:
        scores["Ties"] += 1
        messagebox.showinfo("Game Over", "It's a draw!")
        update_score(score_label)
        reset_board(turn_label)
        return

    current_player = "O" if current_player == "X" else "X"
    turn_label.config(text=f"{player_names[current_player]}'s Turn")

    if mode == "PvBot" and current_player == "O":
        window.after(500, lambda: bot_move(window, mode, turn_label, score_label))

# === Undo feature ===
def undo_move(turn_label):
    global current_player
    if move_history:
        index, last_player = move_history.pop()
        board[index] = ""
        buttons[index].config(text="", state="normal", bg="#ecf0f1")
        current_player = last_player
        turn_label.config(text=f"{player_names[current_player]}'s Turn")

# === Bot logic (simple but defends) ===
def bot_move(window, mode, turn_label, score_label):
    winning_lines = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in winning_lines:
        line = [board[a], board[b], board[c]]
        if line.count("O") == 2 and line.count("") == 1:
            move = [a, b, c][line.index("")]
            on_click(move, window, mode, turn_label, score_label)
            return
    for a,b,c in winning_lines:
        line = [board[a], board[b], board[c]]
        if line.count("X") == 2 and line.count("") == 1:
            move = [a, b, c][line.index("")]
            on_click(move, window, mode, turn_label, score_label)
            return
    if board[4] == "":
        on_click(4, window, mode, turn_label, score_label)
        return
    for i in [0,2,6,8]:
        if board[i] == "":
            on_click(i, window, mode, turn_label, score_label)
            return
    for i in [1,3,5,7]:
        if board[i] == "":
            on_click(i, window, mode, turn_label, score_label)
            return

# === Winner checker ===
def check_winner():
    win_combos = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in win_combos:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None

# === Reset board ===
def reset_board(turn_label):
    global board, move_history, current_player
    board = [""] * 9
    move_history = []
    for btn in buttons:
        btn.config(text="", state="normal", bg="#ecf0f1")
    current_player = selected_mark
    turn_label.config(text=f"{player_names[current_player]}'s Turn")

# === Score update ===
def update_score(score_label):
    score_label.config(
        text=f"{player_names['X']} (X): {scores['X']}   Ties: {scores['Ties']}   {player_names['O']} (O): {scores['O']}"
    )

# === Quit confirmation ===
def quit_game(window):
    if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
        window.destroy()

# === Show game board ===
def show_board(mode):
    window = tk.Tk()
    window.title("Tic Tac Toe")
    window.configure(bg="#1e272e")

    turn_label = tk.Label(window, text=f"{player_names[current_player]}'s Turn", font=("Arial", 16), bg="#1e272e", fg="white")
    turn_label.grid(row=0, column=0, columnspan=3, pady=10)

    score_label = tk.Label(window, text="", font=("Arial", 12), bg="#1e272e", fg="lightgray")
    score_label.grid(row=1, column=0, columnspan=3)
    update_score(score_label)

    for i in range(9):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2,
                        bg="#ecf0f1", command=lambda i=i: on_click(i, window, mode, turn_label, score_label))
        btn.grid(row=(i//3)+2, column=i%3, padx=5, pady=5)
        buttons.append(btn)

    tk.Button(window, text="Undo", command=lambda: undo_move(turn_label)).grid(row=5, column=0, pady=10)
    tk.Button(window, text="Reset", command=lambda: reset_board(turn_label)).grid(row=5, column=1)
    tk.Button(window, text="Quit", command=lambda: quit_game(window)).grid(row=5, column=2)

    window.mainloop()

# === Run the game ===
welcome_screen()
