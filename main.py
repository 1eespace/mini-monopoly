import tkinter as tk 
# Dropdown for the dice_roll json files
from tkinter import ttk

from ui.board_view import BoardView
from models.player import Player

def main():
    # Initialise the main window
    root = tk.Tk()
    root.title("Mini Monopoly")
    
    # Set window size 
    root.geometry("900x720")
    
    # root.resizable(False, False)

    # Board view (left side) => Pass 'root' as the parent
    board = BoardView(root, json_file="board.json")
    board.pack(side="left", padx=10, pady=10)

    # Panels: Dropdown, Buttons (right side)
    controls = tk.Frame(root)
    controls.pack(side="right", fill="y", padx=20, pady=50)

    # Dropdown
    tk.Label(controls, text="Select Dice Rolls:", font=("Arial", 10, "bold")).pack(pady=5)
    dice_option = ttk.Combobox(controls, values=["rolls_1.json", "rolls_2.json"], state="readonly")
    dice_option.set("rolls_1.json")
    dice_option.pack(pady=5)

    # Status Labels
    status_label = tk.Label(controls, text="Game Ready", fg="blue")
    status_label.pack(pady=10)

    # Buttons 
    btn_start = tk.Button(controls, text="Start Game", width=15)
    btn_start.pack(pady=5)

    btn_next = tk.Button(controls, text="Next Turn", width=15, state="disabled")
    btn_next.pack(pady=5)

    btn_reset = tk.Button(controls, text="Reset Game", width=15)
    btn_reset.pack(pady=5)

    # Set the Players marker (Order)
    players = [Player("Peter"), Player("Billy"), Player("Charlotte"), Player("Sweedal")]
    # Update their positions
    board.update_player_position(players)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()