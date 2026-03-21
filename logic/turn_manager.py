from models.player import Player
from models.tile import Tile

from logic.property_resolver import PropertyResolver

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
        # PropertyResolver
        self.resolver = PropertyResolver(tiles)

    # Return the player whose turn it is now
    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    # Move to the next player 
    def next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # GAME END: BANKRUPT
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

        # Pass GO Tile
        passed_go = player.move(dice_roll, len(self.tiles))
        if passed_go:
            player.receive(GO_MONEY)

        landed_tile = self.tiles[player.position]
        # Decide the action based on Property status
        action = self.resolver.resolve_tile(player, landed_tile)

        # THE END: If this turn caused bankruptcy
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
            "game_over": False            
        }

        self.next_player()
        return result

    # Get the Winner
    def get_winner(self) -> str | list[str]:
        # Winner: holding highest money balance among all players
        highest_money_amount = max(player.money for player in self.players)

        # Collect all player(s) who have the highest balance 
        winners = [
            player.name
            for player in self.players
            if player.money == highest_money_amount
        ]

        # 1 Winner: single player name, otherwise return list
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