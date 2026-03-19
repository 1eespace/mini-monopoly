import tkinter as tk 
from ui.board_view import BoardView
from ui.game_ui_controls import GameUIControls

def main():
    root = tk.Tk()
    root.title("Mini Monopoly")
    root.geometry("1000x720")
    root.resizable(False, False)

    board = BoardView(root, json_file="board.json")
    board.pack(side="left", padx=10, pady=10)

    controls = GameUIControls(root, board)
    controls.pack(side="right", fill="y", padx=20, pady=50)

    root.mainloop()


if __name__ == "__main__":
    main()