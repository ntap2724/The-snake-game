"""Utility functions for the Snake Game"""

import random
from src.config import BOARD_WIDTH, BOARD_HEIGHT

def get_random_position():
    """Generate a random position on the game board"""
    x = random.randint(0, BOARD_WIDTH - 1)
    y = random.randint(0, BOARD_HEIGHT - 1)
    return (x, y)

def is_valid_direction(current_dir, new_dir):
    """Check if the new direction is valid (not 180 degree turn)"""
    opposite_dirs = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT'
    }
    return opposite_dirs.get(current_dir) != new_dir
