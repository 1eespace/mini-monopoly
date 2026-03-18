import json
from pathlib import Path
from ui.style_sheet import TILE_POSITION, PROPERTY_COLOUR


def load_board_data(json_file: str = "board.json") -> list[dict]:
    # Load board data from json file
    board_path = Path(json_file)
    
    # Read title data from board.json
    with board_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def build_tiles(json_file: str = "board.json") -> list[dict]:
    # Match board.json tiles with TILE_LAYOUTS by index
    board_data = load_board_data(json_file)

    # Data from board.json and TILE_POSITION are 9 (0-8)
    if len(board_data) != len(TILE_POSITION):
        raise ValueError("Board data does not match tile layout")

    tiles = []

    for index, tile_data in enumerate(board_data):
        colour_name = tile_data.get("colour")
        # PROPERTY_COLOUR from style_sheet.py
        # Convert colour name to hex code for drawing
        colour_hex = PROPERTY_COLOUR.get(colour_name) if colour_name else None

        tile = {
            # Tile position from config (style_sheet.py)
            "index": index,
            "x1": TILE_POSITION[index][0],
            "y1": TILE_POSITION[index][1],
            "x2": TILE_POSITION[index][2],
            "y2": TILE_POSITION[index][3],

            # Tile info from JSON; name, price, colour, type (property or GO)
            "name": tile_data.get("name", ""),
            "price": tile_data.get("price"),
            "colour": colour_name,
            "colour_hex": colour_hex,
            "type": tile_data.get("type", ""),
        }

        tiles.append(tile)

    return tiles

"""
build tiles output;

[
    {
        "index": 0,
        "x1": 20,
        "y1": 500,
        "x2": 660,
        "y2": 670,
        "name": "GO",
        "price": None,
        "colour": None,
        "colour_hex": None,
        "type": "go"
    },
    {
        "index": 1,
        "x1": 20,
        "y1": 340,
        "x2": 180,
        "y2": 500,
        "name": "The Burvale",
        "price": 1,
        "colour": "Brown",
        "colour_hex": "#8d6e63",
        "type": "property"
    }
]

"""