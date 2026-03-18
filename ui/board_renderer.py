import json
from pathlib import Path
from ui.style_sheet import TILE_POSITION, PROPERTY_COLOUR
from models.tile import Tile

def load_board_data(json_file: str = "board.json") -> list[dict]:
    # Load board data from json file
    board_path = Path(json_file)
    
    # Read title data from board.json
    with board_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def build_tiles(json_file: str = "board.json") -> list[Tile]:
    # Match board.json tiles with TILE_LAYOUTS by index
    board_data = load_board_data(json_file)

    # Data from board.json and TILE_POSITION are 9 (0-8)
    if len(board_data) != len(TILE_POSITION):
        raise ValueError("Board data does not match tile layout")

    tiles = []

    for index, tile_data in enumerate(board_data):
        colour_name = tile_data.get("colour")
        position = TILE_POSITION[index]

        tile = Tile(
            index=index,
            x1=position[0], y1=position[1], x2=position[2], y2=position[3],
            name=tile_data.get("name", ""),
            price=tile_data.get("price"),
            colour=colour_name,
            colour_hex=PROPERTY_COLOUR.get(colour_name) if colour_name else None,
            tile_type=tile_data.get("type", "")
        )
        
        tiles.append(tile)

    return tiles

