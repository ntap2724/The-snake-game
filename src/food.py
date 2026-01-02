"""Food class for the game"""

from src.utils import get_random_position
from src.config import BOARD_WIDTH, BOARD_HEIGHT

class Food:
    """Represents the food in the game"""
    
    def __init__(self):
        """Initialize food at a random position"""
        self.position = get_random_position()
    
    def spawn(self, exclude_positions=None):
        """Spawn food at a new random position
        
        Args:
            exclude_positions (list, optional): List of (x, y) tuples to avoid. 
                Defaults to None.
        """
        if exclude_positions is None:
            exclude_positions = []
            
        attempts = 0
        while attempts < 100:
            new_pos = get_random_position()
            if new_pos not in exclude_positions:
                self.position = new_pos
                return
            attempts += 1
        
        # Timeout protection: if we try more than 100 times, just use the position anyway
        # (board almost full)
        self.position = get_random_position()
    
    def get_position(self):
        """Return the current (x, y) position of the food"""
        return self.position
