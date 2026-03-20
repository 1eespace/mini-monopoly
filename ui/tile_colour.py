import webcolors
# https://webcolors.readthedocs.io/en/stable/

def colour_mapping(board_data: list[dict]) -> dict[str, str | None]:
    # Colour name to hex mapping from board.json
    colour_map = {}

    for tile in board_data:
        # Read colour data from the json file
        colour_name = tile.get("colour")
        if colour_name and colour_name not in colour_map:
            try:
                colour_map[colour_name] = webcolors.name_to_hex(colour_name.lower())

            # Raise ValueError like None or int instead of str
            except (ValueError):
                print(f"[Warning] Unknown colour '{colour_name}'")
                colour_map[colour_name] = None

    return colour_map