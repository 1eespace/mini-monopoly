from dataclasses import dataclass
from models.player import Player

# MUTABLE
@dataclass
class Tile:
    index: int
    name: str
    x1: int
    y1: int
    x2: int
    y2: int
    tile_type: str
    owner: Player | None = None
    # For the board.json extension
    price: int | None = None
    colour: str | None = None
    colour_hex: str | None = None

    @property
    def mid_x(self) -> float:
        # Centre of x coord 
        return (self.x1 + self.x2) / 2
    
    @property
    def mid_y(self) -> float:
        # Centre of y coord
        return (self.y1 + self.y2) / 2
    