#  MINI-MONOPOLY StyleSheet

# TILE COORDINATES
"""
Specific Position; Each tile coordinates

Python Tkinter: (x1, y1, x2, y2) Dictionary 
x1y1 leftTop and x2y2 rightBottom

""" 
TILE_POSITION = {
    0: (20, 500, 660, 670),
    1: (20, 340, 180, 500),
    2: (20, 180, 180, 340),
    3: (20, 20, 180, 180),
    4: (180, 20, 340, 180),
    5: (340, 20, 500, 180),
    6: (500, 20, 660, 180),
    7: (500, 180, 660, 340),
    8: (500, 340, 660, 500),
}

# PLAYER MARKER COLOUR
PLAYER_COLOUR = {
    "Peter": "#FEA8FE",      
    "Billy": "#FFB300",      
    "Charlotte": "#7DF0E2",  
    "Sweedal": "#938FEC"     
}

# PROPERTY COLOUR
PROPERTY_COLOUR = {
    "Brown": "#611f07",
    "Red": "#ff0400",
    "Green": "#4caf50",
    "Blue": "#0011ff",
}

# COLOUR
BOARD_BG="#f7f3e9"
TILE_FILL="#ffffff"
TILE_OUTLINE="#6b705c"
TEXT_BLACK="#000000"
TEXT_RED="#ff0000"
TEXT_PURPLE="#793bff"
PRICE_COLOUR="#FF8800"