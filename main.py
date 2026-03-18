from ui.board_renderer import build_tiles

tiles = build_tiles("board.json")

for tile in tiles:
    print(tile)