#!/usr/bin/env python3
"""Snake Game Entry Point"""

from src.game import SnakeGame

def run():
    """Run the game"""
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    run()
