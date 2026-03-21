from models.player import Player
from models.tile import Tile

class PropertyResolver:
    def __init__(self, tiles: list[Tile]):
        self.tiles = tiles

    # GO: NON PROPERTY TILE
    def resolve_tile(self, player: Player, tile: Tile) -> str:
        if tile.tile_type != "property":
            return f"landed on {tile.name}"

        # Property tile should have a price
        if tile.price is None:
            return f"landed on {tile.name}"

        # Buy automatically if unoccupied
        if tile.owner is None:
            player.pay(tile.price)
            tile.owner = player
            player.properties.append(tile)

            if player.is_bankrupt:
                return f"bought {tile.name} for ${tile.price} and went bankrupt"

            return f"bought {tile.name} for ${tile.price}"

        # Own property
        if tile.owner == player:
            return f"landed on own property: {tile.name}"

        # Pay rent to another player
        rent = tile.price

        # Double rent if owner has full colour (x 2)
        if tile.colour is not None and self.owner_has_full_colour(tile.owner, tile.colour):
            rent *= 2

        player.pay(rent)
        tile.owner.receive(rent)

        if player.is_bankrupt:
            return f"paid ${rent} rent to {tile.owner.name} and went bankrupt"

        return f"paid ${rent} rent to {tile.owner.name}"

    # Get all property tiles of the same colour
    def owner_has_full_colour(self, owner: Player, colour: str) -> bool:
        same_colour_tiles = [
            tile for tile in self.tiles
            if tile.tile_type == "property" and tile.colour == colour
        ]

        # Owner must own every tile in that colour
        return all(tile.owner == owner for tile in same_colour_tiles)
