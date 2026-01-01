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
        # TODO: Implement bounds checking
        pass
    
    def check_wall_collision(self, position):
        """Check if a position collides with board walls"""
        # TODO: Implement wall collision detection
        pass
