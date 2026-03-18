import tkinter as tk 
from ui.board_view import BoardView
from models.player import Player

def main():
    # Initialise the main window
    root = tk.Tk()
    root.title("Mini Monopoly")
    
    # Set window size 
    root.geometry("700x720")
    
    # Board view => Pass 'root' as the parent
    board = BoardView(root, json_file="board.json")
    
    # Pack the canvas 
    board.pack()

    # Set the Players marker
    players = [
        Player("Peter"),
        Player("Billy"),
        Player("Charlotte"),
        Player("Sweedal")
    ]

    board.update_player_position(players)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()