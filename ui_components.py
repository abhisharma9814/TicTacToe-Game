# ui_components.py

import tkinter as tk

def create_grid_buttons(parent, on_click_callback):
    buttons = []
    for i in range(9):
        btn = tk.Button(
            parent,
            text="",
            font=("Arial", 20),
            width=5,
            height=2,
            bg="#ecf0f1",
            command=lambda i=i: on_click_callback(i)
        )
        btn.grid(row=(i//3)+2, column=i%3, padx=5, pady=5)
        buttons.append(btn)
    return buttons
