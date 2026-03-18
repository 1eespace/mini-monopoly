from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Tile:
    index: int
    name: str
    x1: int
    y1: int
    x2: int
    y2: int
    tile_type: str
    # For the board.json extension
    price: Optional[int] = None
    colour: Optional[str] = None
    colour_hex: Optional[str] = None

    @property
    def mid_x(self) -> float:
        # Centre of tile 
        return (self.x1 + self.x2) / 2