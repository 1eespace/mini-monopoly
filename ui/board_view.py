import tkinter as tk
from ui.board_renderer import build_tiles
from ui.style_sheet import (
    BOARD_BG, TILE_FILL, TILE_OUTLINE, TITLE_COLOUR, PRICE_COLOUR
)

class BoardView(tk.Canvas):
    def __init__(self, parent: tk.Tk, json_file: str = "board.json"):
        # Initialise the parent class (tk.Canvas) 
        # and attach it to the main window (parent)
        super().__init__(
            parent,
            width=680,
            height=690,
            background=BOARD_BG,
        )

        # Load tile data from the JSON file
        self.tiles = build_tiles(json_file)
        # Render all components onto the canvas
        self.draw_board()

    def draw_board(self) -> None:
        # Iterates through the tile list and draws each tile
        for tile in self.tiles:
            self.draw_tile(tile)

    def draw_tile(self, tile: dict) -> None:
        # Rendering a single/each tile including the box, colour bar and text
        # Extract coordinates for easier access
        x1, y1, x2, y2 = tile["x1"], tile["y1"], tile["x2"], tile["y2"]
        mid_x = (x1 + x2) / 2

        # Draw the main rectangular box of the tile
        self.create_rectangle(
            x1, y1, x2, y2,
            fill=TILE_FILL,
            outline=TILE_OUTLINE,
            width=2
        )

        # Draw the property colour bar if a color exists
        if tile.get("colour_hex"):
            self.create_rectangle(
                x1, y1, x2, y1 + 20,
                fill=tile["colour_hex"],
                outline=""
            )

        # Render the tile name (Title)
        self.create_text (
            mid_x, y1 + 45,
            text=tile["name"],
            fill=TITLE_COLOUR,
            font=("Arial", 10, "bold"),
        )
 
        # Render the price label if it's not None
        if tile.get("price") is not None:
            self.create_text (
                mid_x, y2 - 20,
                text=f"${tile['price']}",
                fill=PRICE_COLOUR,
                font=("Arial", 10, "bold")
            )