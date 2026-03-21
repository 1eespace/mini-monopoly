import json
from pathlib import Path
from models.tile import Tile
from ui.tile_colour import colour_mapping

def load_board_data(json_file: str) -> list[dict]:
    path = Path(json_file)
    # Raise error if board file does not exist
    if not path.exists():
        raise FileNotFoundError(f"Board file not found: {path}")
    
    return json.loads(path.read_text(encoding="utf-8"))

# Extensibility for the Tile (No TILE_POSITION Used)
def compute_tile_positions(tiles_data: list[dict], board_size: int = 680) -> dict[int, tuple]:
    """
        Layout:
            - Type=GO: Fixed at the bottom-left corner
            - Remaining tiles wrap clockwise: left, top , right, and bottom
            - Tiles are distributed as evenly as possible across 4 sides
    """
    number_of_tiles = len(tiles_data)

    # Find the GO index 
    go_index = next((i for i, tile in enumerate(tiles_data) if tile.get("type") == "go"), 0)
    # List for the Property (Not GO)
    other_tiles = [i for i in range(number_of_tiles) if i != go_index]

    # TILES DISTRIBUTION
    # Split remaining tiles evenly across 4 sides
    side_tiles = len(other_tiles)       # 9 - 1 (GO)
    base = side_tiles // 4              # One side: at least 2
    remainder = side_tiles % 4          # 0 

    # Clockwise: left, top, right, and bottom
    counts = [
        base + (1 if remainder > 0 else 0), # left
        base + (1 if remainder > 1 else 0), # top
        base + (1 if remainder > 2 else 0), # right
        base                                # bottom
    ]

    # SIZE CALCULATION
    # Set maximum of the side size
    max_per_side  = max(counts)
    """
    - tile_size: width/height of a single tile
    - opposite_edge: (board_size - tile_size)
    - side_length: usable tile on each side (excluding the two corner tiles)
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

    positions = {}
    # GO FIXED POSITION: bottom-left corner 
    positions[go_index] = (0, opposite_edge, tile_size, board_size)

    # POSITIONING AS CLOCKWISE
    idx = 0
    for side_function, tiles_per_side in zip([left_tile, top_tile, right_tile, bottom_tile], counts):
        """
            Two lists
            - sides_function: left, top, right, bottom_tile()
            - counts: [2, 2, 2, 2]
            
            (left_tile, 2)
            (top_tile, 2)
            (right_tile, 2)
            (bottom_tile, 2)
        """

        for step in range(tiles_per_side):
            # Fetch tile's idx from the other_tiles
            tile_idx = other_tiles[idx]
            # Calculate the coordinates
            positions[tile_idx] = side_function(step, tiles_per_side)
            # Counter
            idx += 1

    return positions

def build_tiles(json_file: str = "board.json", board_size: int = 680) -> list[Tile]:
    # Build and return a list of Tile objects from the given board json
    board_data = load_board_data(json_file)
    positions  = compute_tile_positions(board_data, board_size)

    # Colour Hex (tile_colour.py)
    colour_map = colour_mapping(board_data) 

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
        colour_name = tile_data.get("colour")
        
        tiles.append(Tile(
            index=index,
            x1=x1, y1=y1, x2=x2, y2=y2,
            name=tile_data.get("name", ""),
            price=tile_data.get("price"),
            colour_hex=colour_map.get(colour_name) if colour_name else None,
            tile_type=tile_data.get("type", "")
        ))

    return tiles