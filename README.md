# Mini Monopoly Game

A deterministic Monopoly game simulator built with Python and Tkinter.

This application simulates player movement, property acquisition, and rent logic based on predefined dice rolls from JSON files.

## Getting Started

### Prerequisites

- Python 3.10+
- Tkinter: Usually comes pre-installed with Python. If not, you may need to install it
- Dependencies: The project uses `webcolors` for tile colour mapping

### Installation

1. Clone the repository to your local
2. Install the required Python packages:

```bash
pip3 install tk webcolors
```

### Execution

To start the simulator, run the `main.py` script:

```bash
python3 main.py
```

The script includes a `if __name__ == "__main__":` block to ensure it runs correctly when executed directly.

## Game Rules

The simulation follows these specific rules:

- **Players:** Four players (Peter, Billy, Charlotte, Sweedal) take turns in a fixed order
- **Starting Budget:** Each player starts with $16
- **GO Tile:**
  - Everyone starts on GO
  - Passing GO rewards $1 (excluding the initial starting position)
- **Property Rules:**
  - Landing on an unowned property: Must buy it
  - Landing on an owned property: Pay rent to the owner
  - Monopoly Bonus: If an owner owns all properties of the same colour, the rent is doubled
- **Bankruptcy:** The game ends as soon as any player goes bankrupt (money < 0)
- **Winning Condition:** Once the game ends, the player with the most money remaining is the winner
- **Simplification:** No chance cards, jail, or stations are included

## Game Results

### rolls_1.json

Winner: Peter

### rolls_2.json

Winner: Charlotte

## Project Structure

```
.
├── logic/                    # Game logics
│   ├── board_renderer.py     # Handles Board
│   └── dice_roll_handler.py  # Dice roll handler
|   └── property_resolver.py  # Property (tile) management
|   └── turn_manager.py       # Turn management
├── models/                   # Data classes
│   ├── player.py
│   └── tile.py
├── ui/                     # Graphical interface (Tkinter)
│   ├── board_view.py       # Main UI Layout
│   ├── game_ui_controls.py # Dropdown, Buttons, and Labels
│   ├── style_sheet.py      # UI Constants
│   └── tile_colour.py      # Color mapping logic
├── board.json              # Board configuration
├── rolls_1.json            # Dice roll dataset 1
├── rolls_2.json            # Dice roll dataset 2
└── main.py                 # Entry point
```

## Features

- **Extensible Board:** The UI automatically calculates tile positions based on `board.json` using a clockwise layout.
- **Visual Feedback:** Real-time visualisation of player movements and property ownership using Tkinter.
- **Data Driven:** Easy to test different scenarios by switching JSON files for board layout and dice rolls.

## Design Decisions

- **Separation of Concerns:**  
  The application separates responsibilities into distinct modules (`models`, `logic`, `ui`) to improve maintainability and readability.

- **Component-Based Structure:**  
  Although not strictly following MVC, the project adopts a modular structure where each component has a clear responsibility.

- **Improving SRP (Single Responsibility Principle):**  
  The `TurnManager` was refactored by extracting property-related logic into `PropertyResolver` to ensure each class has a single responsibility.

- **UI and Logic Separation:**  
  The UI layer (Tkinter) is kept separate from game logic, making it easier to modify or replace the interface.

- **Renderer as a Bridge:**  
  `board_renderer.py` acts as a bridge between the game state and UI representation.

## Documentation

- 📄 Technical Document: [https://docs.google.com/document/d/1Sn__EZArDq-ODkPtseiEaymb0Rrj_evzybb5n9Rn8es/edit?usp=sharing]
- 👤 User Document: [https://docs.google.com/document/d/1MV0aiT7RoVih3mTHoNw_LiWF_fgQmWOsfoGAlPBuvTU/edit?usp=sharing]
