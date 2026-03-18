"""
Using dataclass
    name
    current money amount 
    position
    bankrupt or not 
    properties

    pay()
    receive()

    move: depends on dice roll
    turn: static but logic
"""
from dataclasses import dataclass, field

@dataclass
class Player: 
    name: str
    money: int = 16
    position: int = 0
    is_bankrupt: bool = False
    # list and mutable value; objects of properties owned by the player
    properties: list = field(default_factory=list)

    def pay(self, amount: int) -> None:
        self.money -= amount
        if self.money < 0:
            self.is_bankrupt = True
        
    def receive(self, amount: int) -> None:
        self.money += amount