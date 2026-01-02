"""High Score Manager for Snake Game"""

import json
import os
from src.config import BOARD_WIDTH, BOARD_HEIGHT

class HighScoreManager:
    """Manages high score persistence and statistics"""
    
    def __init__(self):
        """Initialize high score manager and load existing scores"""
        self.high_score_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'high_scores.json')
        self.stats = self._load_stats()
    
    def _load_stats(self):
        """Load high score stats from file"""
        try:
            if os.path.exists(self.high_score_file):
                with open(self.high_score_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    "high_score": 0,
                    "last_game_score": 0,
                    "total_games": 0
                }
        except (json.JSONDecodeError, IOError):
            # Return default stats if file is corrupted or can't be read
            return {
                "high_score": 0,
                "last_game_score": 0,
                "total_games": 0
            }
    
    def _save_stats(self):
        """Save high score stats to file"""
        try:
            with open(self.high_score_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError:
            # Silently fail if we can't save (not critical)
            pass
    
    def get_high_score(self):
        """Return current high score"""
        return self.stats.get("high_score", 0)
    
    def update_score(self, new_score):
        """Update high score if new_score is higher"""
        current_high = self.get_high_score()
        if new_score > current_high:
            self.stats["high_score"] = new_score
            self._save_stats()
            return True  # New high score!
        return False  # No new high score
    
    def update_last_game_score(self, score):
        """Update last game score and increment total games"""
        self.stats["last_game_score"] = score
        self.stats["total_games"] += 1
        self._save_stats()
    
    def get_stats(self):
        """Return all statistics as dictionary"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset all statistics (for testing or admin purposes)"""
        self.stats = {
            "high_score": 0,
            "last_game_score": 0,
            "total_games": 0
        }
        self._save_stats()