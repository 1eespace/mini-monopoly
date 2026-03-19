import tkinter as tk
# Dropdown
from tkinter import ttk

from models.player import Player
from logic.dice_roll_handler import DiceRollHandler
from logic.turn_manager import TurnManager
from ui.board_view import BoardView
from ui.style_sheet import TEXT_BLACK

"""
    Handles the side control panel of the game:
    - dice json file selection
    - turn progression
    - game status display 
"""
class GameUIControls(tk.Frame):
    def __init__(self, parent: tk.Tk, board: BoardView):
        super().__init__(parent)

        self.board = board

        # Initialise players with fixed order
        self.players = [
            Player("Peter"),
            Player("Billy"),
            Player("Charlotte"),
            Player("Sweedal"),
        ]

        # Game logic handlers
        self.dice_handler = None
        self.turn_manager = TurnManager(self.players, self.board.tiles)

        # UI Setup
        self.build_widgets()
        self.board.update_player_position(self.players)

    # Constructs the UI elements for the control panel 
    def build_widgets(self) -> None:
        # Dice roll file dropdown
        tk.Label(self, text="Select Dice Rolls:", font=("Arial", 10, "bold")).pack(pady=5)

        # ttk for the dropdown
        self.dice_option = ttk.Combobox(
            self,
            values=["rolls_1.json", "rolls_2.json"],
            state="readonly"
        )

        self.dice_option.set("rolls_1.json")
        self.dice_option.pack(pady=5)

        # Status label; messaging 
        self.status_label = tk.Label(
            self,
            text="Game Ready",
            fg=TEXT_BLACK,
            wraplength=180,
            justify="left"
        )
        self.status_label.pack(pady=10)

        # Turn label
        self.turn_label = tk.Label(
            self,
            text="Current Turn: Peter",
            font=("Arial", 10, "bold")
        )
        self.turn_label.pack(pady=5)

        # Control Buttons; Start Game, Next Turn, and Reset Game
        self.btn_start = tk.Button(self, text="Start Game", width=15, command=self.start_game)
        self.btn_start.pack(pady=5)

        self.btn_next = tk.Button(self, text="Next Turn", width=15, state="disabled", command=self.next_turn)
        self.btn_next.pack(pady=5)

        self.btn_reset = tk.Button(self, text="Reset Game", width=15, command=self.reset_game)
        self.btn_reset.pack(pady=5)

    # REFRESH/RESET
    # Sync the visual board with the current state of player
    def refresh_board(self) -> None:
        self.board.update_player_position(self.players)

        # Update the turn indicator, if the game is still active
        if not self.turn_manager.is_game_over():
            current_player = self.turn_manager.get_current_player()
            self.turn_label.config(text=f"Current Turn: {current_player.name}")

    # START GAME 
    # Initialise the game session with the selected dice roll json file
    def start_game(self) -> None:
        selected_roll_file = self.dice_option.get()

        # Reset state and load dice sequence
        self.turn_manager.reset()
        self.dice_handler = DiceRollHandler(selected_roll_file)

        # Update UI status label
        self.status_label.config(
            text="Game started.\nClick 'Next Turn' to play.",
            fg="green"
        )

        # Toggle buttons states
        self.btn_start.config(state="disabled")
        self.btn_next.config(state="normal")

        self.refresh_board()

    # Execute a single turn based on the next value
    def next_turn(self) -> None:
        if self.dice_handler is None:
            self.status_label.config(text="Please start the game first!", fg="red")
            return

        # Check if have remaining moves in the json file
        if not self.dice_handler.has_next_roll():
            winner = self.turn_manager.get_winner()
            self.status_label.config(
                text=f"No more dice rolls.\nWinner: {winner}",
                fg="purple"
            )

            # Toggle buttons states
            self.btn_next.config(state="disabled")
            self.btn_start.config(state="normal")
            self.turn_label.config(text="Current Turn: -")
            return

        # Fetch roll and process the next movement
        roll = self.dice_handler.get_next_roll()
        if roll is None:
            return

        # Execute turn
        result = self.turn_manager.play_turn(roll)
        self.refresh_board()

        # UI display; result details with the status format 
        status_text = (
            f"{result['player']} rolled {result['roll']}\n"
            f"Landed on: {result['tile_name']}\n"
            f"Action: {result['action']}\n"
            f"Money: ${result['money']}"
        )

        if result["passed_go"]:
            status_text += "\nPassed GO (+$1)"

        # THE END: One player is_bankrupt = True
        if result["game_over"]:
            winner = self.turn_manager.get_winner()
            status_text += f"\n\nGame Over!\nWinner: {winner}"
            self.status_label.config(text=status_text, fg="red")
            self.btn_next.config(state="disabled")
            self.btn_start.config(state="normal")
            self.turn_label.config(text="Current Turn: -")
            return

        self.status_label.config(text=status_text, fg="black")

    # Clear the game state and restores to the initial UI
    def reset_game(self) -> None:
        self.turn_manager.reset()
        self.dice_handler = None

        self.status_label.config(text="Game Reset.", fg="blue")
        # First player: Peter
        self.turn_label.config(text="Current Turn: Peter")

        self.btn_start.config(state="normal")
        self.btn_next.config(state="disabled")

        self.refresh_board()