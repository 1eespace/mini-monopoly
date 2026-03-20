import json
from pathlib import Path

class DiceRollHandler: 
    def __init__(self, json_file: str):
        # Store the selected dice roll file name
        self.json_file = json_file
        # Load all dice roll values from json file
        self.rolls = self.load_rolls(json_file)
        # Track position using the index
        self.current_index = 0

    # Load data from rolls_1.json / 2.json
    def load_rolls(self, json_file: str) -> list[int]:
        path = Path(json_file)
        # Raise error if the file does not exist
        if not path.exists():
            raise FileNotFoundError(f"Dice roll file not found: {path}")
        
        return json.loads(path.read_text(encoding="utf-8"))
    
    # Return True is there are still have dice rolls values
    def has_next_roll(self) -> bool:
        return self.current_index < len(self.rolls)
    
    # Return the next dice roll value and move to the next index
    def get_next_roll(self) -> int | None:
        if not self.has_next_roll():
            return None
        
        roll = self.rolls[self.current_index]
        self.current_index += 1
        return roll
    
    # RESET/ RELOAD: dice roll sequence & new json file selected
    def reset(self, json_file: str | None = None) -> None:
        if json_file is not None:
            self.json_file = json_file
            self.rolls = self.load_rolls(self.json_file)
            self.current_index = 0