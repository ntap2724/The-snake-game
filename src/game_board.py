"""GameBoard class for managing the game arena"""

from src.config import BOARD_WIDTH, BOARD_HEIGHT

class GameBoard:
    """Represents the game board/arena"""
    
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        """Initialize the game board"""
        self.width = width
        self.height = height
    
    def is_within_bounds(self, position):
        """Check if a position is within board boundaries"""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height
    
    def check_wall_collision(self, position):
        """Check if a position collides with board walls"""
        return not self.is_within_bounds(position)

    def wrap_position(self, position):
        """Wrap a position to the opposite side when it exits the board"""
        x, y = position
        return (x % self.width, y % self.height)
