import tkinter as tk 
from ui.board_view import BoardView
from ui.game_ui_controls import GameUIControls

def main():
    # Initialise the main window
    root = tk.Tk()
    root.title("Mini Monopoly")
    root.geometry("1000x780")
    root.resizable(False, False)

    # BoardView (LEFT)
    board = BoardView(root, json_file="board.json")
    board.pack(side="left", padx=10, pady=10)

    # GameUIControls (RIGHT)
    controls = GameUIControls(root, board)
    controls.pack(side="right", fill="y", padx=20, pady=50)

    # Start the Tkinter event loop
    root.mainloop()


# Script runs only when executed directly
if __name__ == "__main__":
    main()