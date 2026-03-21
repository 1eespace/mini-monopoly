import tkinter as tk
from logic.board_renderer import build_tiles
from ui.style_sheet import (
    BOARD_BG, TILE_FILL, TILE_OUTLINE, TEXT_BLACK, PRICE_COLOUR, PLAYER_COLOUR
)
from models.tile import Tile

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

    def draw_tile(self, tile: Tile) -> None:
        # Draw the main rectangular box of the tile
        self.create_rectangle(
            tile.x1, tile.y1, tile.x2, tile.y2,
            fill=TILE_FILL,
            outline=TILE_OUTLINE,
            width=2
        )

        # Draw the property colour bar if a color exists
        if tile.colour_hex:
            self.create_rectangle(
                tile.x1, tile.y1, tile.x2, tile.y1 + 20,
                fill=tile.colour_hex,
                outline=""
            )

        # Render the tile name 
        self.create_text (
            tile.mid_x, tile.y1 + 45,
            text=tile.name,
            fill=TEXT_BLACK,
            font=("Arial", 10, "bold"),
        )
 
        # Render the price label if it's not None
        if tile.price is not None:
            self.create_text (
                tile.mid_x, tile.y2 - 20,
                text=f"${tile.price}",
                fill=PRICE_COLOUR,
                font=("Arial", 10, "bold")
            )

    # Render the player 
    def update_player_position(self, players: list) -> None:
        """
        Updates player and their current money balance on the board
        All 4 players are rendered until someone's balance < 0 (bankrupt)
        """
        self.delete("player_marker")

        # Use PLAYER_COLOUR mapping
        player_names = ["Peter", "Billy", "Charlotte", "Sweedal"]

        # Offsets to prevent players from overlapping on the same tile
        offsets = [(-40, -15), (40, -15), (-40, 15), (40, 15)]
        
        for i, player in enumerate(players):
            # Get tile and colour info
            current_tile = self.tiles[player.position]
            # If player_name's colour is None
            colour = PLAYER_COLOUR.get(player_names[i], TEXT_BLACK)
            offset_x, offset_y = offsets[i]

            # Draw Player as Circle 
            self.create_oval (
                current_tile.mid_x + offset_x - 10, current_tile.mid_y + offset_y - 10,
                current_tile.mid_x + offset_x + 10, current_tile.mid_y + offset_y + 10,
                        fill=colour,
                        outline="white",
                        width=2,
                        tags="player_marker"
            )
            
            # Draw Player's name Above the circle
            self.create_text (
                    current_tile.mid_x + offset_x, current_tile.mid_y + offset_y - 5,
                    text=player.name,
                    fill=TEXT_BLACK,
                    font=("Arial", 8, "bold"),
                    tags="player_marker"
            )

            # Draw Money Balance ($16)
            self.create_text (
                current_tile.mid_x + offset_x, current_tile.mid_y + offset_y + 10, 
                        text=f"${player.money}",
                        fill=TEXT_BLACK, 
                        font=("Arial", 9, "bold"),
                        tags="player_marker"
            )
        
    # Display the owner (player who occupied/bought) name
    # NO need refresh/delete during the game
    def display_owner_name (self, tiles: list) -> None:
        for tile in tiles: 
            # GO tile is not property
            if tile.tile_type == "property" and tile.owner is not None:

                # Specific tag for preventing duplicate display
                tag = f"owner_tile_{tile.index}"

                # Match player's colour 
                owner_colour = PLAYER_COLOUR.get(tile.owner.name, TEXT_BLACK)

                if not self.find_withtag(tag):
                    self.create_text(
                        tile.mid_x, 
                        tile.mid_y + 18,  
                        text=f"Owner: {tile.owner.name}",
                        fill=owner_colour, 
                        font=("Arial", 8, "bold"),
                        tags=(tag, "static_owner") 
                )
    
    # When the GAME RESET should clear the owner labels
    def clear_owner_labels(self) -> None:
        self.delete("static_owner")