import json
from pathlib import Path
from ui.style_sheet import PROPERTY_COLOUR
from models.tile import Tile

def load_board_data(json_file: str) -> list[dict]:
    # Load board data from json file
    with Path(json_file).open("r", encoding="utf-8") as f:
        return json.load(f)

# Extensibility for the Tile (No TILE_POSITION Used)
def compute_tile_positions(number_of_tiles: int, board_size: int = 680) -> dict[int, tuple]:
    """
        Layout:
            - index 0 is always GO: Fixed at the bottom-left corner
            - Remaining tiles wrap clockwise: left, top , right, and bottom
            - Tiles are distributed as evenly as possible across 4 sides
    """
    # TILES DISTRIBUTION
    # Split remaining tiles evenly across 4 sides
    side_tiles = number_of_tiles - 1    # 9 - 1 (GO)
    base = side_tiles // 4              # One side: at least 2
    remainder = side_tiles % 4          # 0 

    left_count = base + (1 if remainder > 0 else 0)
    top_count = base + (1 if remainder > 1 else 0)
    right_count = base + (1 if remainder > 2 else 0)
    bottom_count = base

    # SIZE CALCULATION
    # Set maximum of the side size
    max_per_side  = max(left_count, top_count, right_count, bottom_count, 1)
    """
    - tile_size: width/height of a single tile
    - opposite_edge: (board_size - tile_size)
    - side_length: usable space on each side (excluding the two corner tiles)
    """
    tile_size = board_size // (max_per_side + 1)            # 680 // (2 + 1) = 226
    opposite_edge = board_size - tile_size                  # 680 - 226 = 454
    # Excluding corners
    side_length = opposite_edge - tile_size                 # 454 - 226 = 228

    # EACH FUNCTIONS (4 SIDES)
    # Returns (x1, y1, x2, y2) for the 'i'th tile on that side
    def left_tile(i, total):
        tile_height = side_length // total
        # FLIP: bottom to top
        row = total - i - 1  
        return (
            0, 
            tile_size + row * tile_height, 
            tile_size, 
            tile_size + (row + 1) * tile_height
        )

    def top_tile(i, total):
        tile_width = side_length // total
        return (
            tile_size + i * tile_width, 
            0, 
            tile_size + (i + 1) * tile_width, 
            tile_size
        )

    def right_tile(i, total):
        tile_height = side_length // total
        return (
            opposite_edge, 
            tile_size + i * tile_height, 
            board_size, 
            tile_size + (i + 1) * tile_height
        )

    def bottom_tile(i, total):
        tile_width = side_length // total
        return (
            # FLIP right to left
            opposite_edge - (i + 1) * tile_width, 
            opposite_edge, 
            opposite_edge - i * tile_width, 
            board_size
        )

    # GO: fixed bottom-left corner
    positions = {0: (0, opposite_edge, tile_size, board_size)}  

    # POSITIONS
    # Clockwise: left, top, right, and bottom
    idx = 1
    for tile_position, total in [
        (left_tile,   left_count),
        (top_tile,    top_count),
        (right_tile,  right_count),
        (bottom_tile, bottom_count),
    ]:
        for i in range(total):
            positions[idx] = tile_position(i, total)
            idx += 1

    return positions

def build_tiles(json_file: str = "board.json", board_size: int = 680) -> list[Tile]:
    # Build and return a list of Tile objects from the given board json
    board_data = load_board_data(json_file)
    positions  = compute_tile_positions(len(board_data), board_size)

    # DEBUG
    print(f"board_data count: {len(board_data)}")
    print(f"positions count: {len(positions)}")
    for i, pos in positions.items():
        print(f"  [{i}] {pos}")

    tiles = []
    for index, tile_data in enumerate(board_data):
        """
            Python Tkinter: (x1, y1, x2, y2) Dictionary 
            x1y1 leftTop and x2y2 rightBottom
        """ 
        x1, y1, x2, y2 = positions[index]

        tiles.append(Tile(
            index=index,
            x1=x1, y1=y1, x2=x2, y2=y2,
            name=tile_data.get("name", ""),
            price=tile_data.get("price"),
            colour=tile_data.get("colour"),
            colour_hex=None,  
            tile_type=tile_data.get("type", "")
        ))

    return tiles