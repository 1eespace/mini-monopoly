"""
Using dataclass
    name
    current money amount 
    position
    bankrupt or not 
    properties

    pay()
    receive()
    move(): depends on dice roll

    turn: static but logic
"""
from dataclasses import dataclass, field

# Const
STARTING_MONEY = 16

@dataclass
class Player: 
    name: str
    money: int = STARTING_MONEY
    position: int = 0
    is_bankrupt: bool = False
    # list and mutable value: objects of properties owned by the player
    # Occupied by player (owner)
    properties: list = field(default_factory=list)

    def pay(self, amount: int) -> None:
        self.money -= amount
        if self.money < 0:
            self.is_bankrupt = True
        
    def receive(self, amount: int) -> None:
        self.money += amount

    def move(self, dice_roll: int, total_tiles: int) -> bool:
        """
        Moves the player and returns True if they passed GO tile
        idx 0 - 8; total 9 tiles (with GO)
        ex> current idx is 7 but dice is 2
        new current idx is 9, but don't have and should return to GO
        7 -> 8 -> GO 
        Formula: (current + dice roll) % total tiles 
        """
        old_position = self.position
        self.position = (self.position + dice_roll) % total_tiles 

        # BOARD WRAPPED: if the new position is smaller than the old position (not GO)
        # First round GO: They don't get paid ($1)
        return self.position < old_position
        