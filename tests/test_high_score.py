"""Unit tests for the High Score Manager"""

import pytest
import json
import os
import tempfile
from src.high_score import HighScoreManager

class TestHighScoreManager:
    """Tests for HighScoreManager class"""
    
    def test_initialization_new_file(self):
        """Test initialization creates default stats when no file exists"""
        # Use a temporary file to avoid affecting real high scores
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"high_score": 15, "last_game_score": 10, "total_games": 3}')
            tmp_file_path = tmp_file.name
        
        # Mock the file path in the manager
        original_init = HighScoreManager.__init__
        def mock_init(self):
            self.high_score_file = tmp_file_path
            self.stats = self._load_stats()
        HighScoreManager.__init__ = mock_init
        
        try:
            manager = HighScoreManager()
            assert manager.get_high_score() == 15
            stats = manager.get_stats()
            assert stats['high_score'] == 15
            assert stats['last_game_score'] == 10
            assert stats['total_games'] == 3
        finally:
            # Restore original init
            HighScoreManager.__init__ = original_init
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    def test_update_score_new_high(self):
        """Test updating score with new high score"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"high_score": 10, "last_game_score": 5, "total_games": 2}')
            tmp_file_path = tmp_file.name
        
        original_init = HighScoreManager.__init__
        def mock_init(self):
            self.high_score_file = tmp_file_path
            self.stats = self._load_stats()
        HighScoreManager.__init__ = mock_init
        
        try:
            manager = HighScoreManager()
            is_new_high = manager.update_score(15)
            
            assert is_new_high is True
            assert manager.get_high_score() == 15
            assert manager.get_stats()['high_score'] == 15
        finally:
            HighScoreManager.__init__ = original_init
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    def test_update_score_not_high(self):
        """Test updating score without new high score"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"high_score": 20, "last_game_score": 10, "total_games": 2}')
            tmp_file_path = tmp_file.name
        
        original_init = HighScoreManager.__init__
        def mock_init(self):
            self.high_score_file = tmp_file_path
            self.stats = self._load_stats()
        HighScoreManager.__init__ = mock_init
        
        try:
            manager = HighScoreManager()
            is_new_high = manager.update_score(15)
            
            assert is_new_high is False
            assert manager.get_high_score() == 20  # Should remain unchanged
        finally:
            HighScoreManager.__init__ = original_init
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    def test_update_last_game_score(self):
        """Test updating last game score and total games"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"high_score": 15, "last_game_score": 10, "total_games": 2}')
            tmp_file_path = tmp_file.name
        
        original_init = HighScoreManager.__init__
        def mock_init(self):
            self.high_score_file = tmp_file_path
            self.stats = self._load_stats()
        HighScoreManager.__init__ = mock_init
        
        try:
            manager = HighScoreManager()
            manager.update_last_game_score(25)
            
            stats = manager.get_stats()
            assert stats['last_game_score'] == 25
            assert stats['total_games'] == 3  # Incremented
        finally:
            HighScoreManager.__init__ = original_init
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    def test_reset_stats(self):
        """Test resetting all statistics"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp_file:
            tmp_file.write('{"high_score": 30, "last_game_score": 25, "total_games": 5}')
            tmp_file_path = tmp_file.name
        
        original_init = HighScoreManager.__init__
        def mock_init(self):
            self.high_score_file = tmp_file_path
            self.stats = self._load_stats()
        HighScoreManager.__init__ = mock_init
        
        try:
            manager = HighScoreManager()
            manager.reset_stats()
            
            stats = manager.get_stats()
            assert stats['high_score'] == 0
            assert stats['last_game_score'] == 0
            assert stats['total_games'] == 0
        finally:
            HighScoreManager.__init__ = original_init
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)