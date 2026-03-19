from models.player import Player
from models.tile import Tile

GO_MONEY = 1
STARTING_MONEY = 16


class TurnManager:
    def __init__(self, players: list[Player], tiles: list[Tile]):
        # All players in fixed Order
        self.players = players

        # Board tiles
        self.tiles = tiles

        # Index of the player whose turn is currently active
        self.current_player_index = 0

    # Return the player whose turn it is now
    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    # Move to the next player 
    def next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # Game ends; bankrupt
    def is_game_over(self) -> bool:
        # Game ends immediately if any player becomes bankrupt
        return any(player.is_bankrupt for player in self.players)

    # Get current player
    def play_turn(self, dice_roll: int) -> dict[str, object]:
        player = self.get_current_player()

        # If player is already bankrupt => GAME ENDS
        if player.is_bankrupt:
            result = {
                "player": player.name,
                "roll": dice_roll,
                "action": "game ended (bankrupt detected)",
                "position": player.position,
                "tile_name": self.tiles[player.position].name,
                "money": player.money,
                "passed_go": False,
                "bankrupt": True,
                "game_over": True,
            }
            return result

        passed_go = player.move(dice_roll, len(self.tiles))

        if passed_go:
            player.receive(GO_MONEY)

        landed_tile = self.tiles[player.position]
        action = self.resolve_tile(player, landed_tile)

        # If this turn caused bankruptcy => END 
        if player.is_bankrupt:
            result = {
                "player": player.name,
                "roll": dice_roll,
                "action": action,
                "position": player.position,
                "tile_name": landed_tile.name,
                "money": player.money,
                "passed_go": passed_go,
                "bankrupt": True,
                "game_over": True,
            }
            return result

        result = {
            "player": player.name,
            "roll": dice_roll,
            "action": action,
            "position": player.position,
            "tile_name": landed_tile.name,
            "money": player.money,
            "passed_go": passed_go,
            "bankrupt": False,
            "game_over": False,
        }

        self.next_player()
        return result

    # Non-property tile (GO)
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

        # Double rent if owner has full colour set
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


    def get_winner(self) -> str | list[str]:
        # Winner is the player with the highest money among all players
        highest_money_amount = max(player.money for player in self.players)

        winners = [
            player.name
            for player in self.players
            if player.money == highest_money_amount
        ]

        return winners[0] if len(winners) == 1 else winners

    def reset(self) -> None:
        # Reset turn back to the first player
        self.current_player_index = 0

        # Reset all players
        for player in self.players:
            player.money = STARTING_MONEY
            player.position = 0
            player.is_bankrupt = False
            player.properties.clear()

        # Clear all property owners
        for tile in self.tiles:
            if tile.tile_type == "property":
                tile.owner = None