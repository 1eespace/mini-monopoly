import tkinter as tk 
from ui.board_view import BoardView

def main():
    # Initializse the main window
    root = tk.Tk()
    root.title("Mini Monopoly")
    
    # Set window size 
    root.geometry("700x720")
    
    # Board view => Pass 'root' as the parent
    board = BoardView(root, json_file="board.json")
    
    # Pack the canvas with padding
    board.pack(padx=10, pady=10)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()