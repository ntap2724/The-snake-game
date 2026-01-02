"""Unit tests for the Snake Game"""

import pytest
from src.snake import Snake
from src.food import Food
from src.game_board import GameBoard
from src.config import BOARD_WIDTH, BOARD_HEIGHT

class TestSnake:
    """Tests for Snake class"""
    
    def test_snake_initialization(self):
        """Test snake is initialized correctly"""
        pos = (10, 10)
        snake = Snake(pos, length=3)
        assert snake.get_head_position() == (10, 10)
        assert len(snake.get_body()) == 3
        assert snake.get_body() == [(10, 10), (10, 11), (10, 12)]
    
    def test_snake_move(self):
        """Test snake movement"""
        pos = (10, 10)
        snake = Snake(pos, length=3)
        snake.move('UP')
        assert snake.get_head_position() == (10, 9)
        assert len(snake.get_body()) == 3
        assert (10, 12) not in snake.get_body()
    
    def test_snake_grow(self):
        """Test snake growth"""
        pos = (10, 10)
        snake = Snake(pos, length=3)
        initial_body = snake.get_body().copy()
        snake.grow()
        assert len(snake.get_body()) == 4
        # Tail should be duplicated
        assert snake.get_body()[-1] == initial_body[-1]

class TestFood:
    """Tests for Food class"""
    
    def test_food_spawn(self):
        """Test food spawning"""
        food = Food()
        initial_pos = food.get_position()
        food.spawn(exclude_positions=[initial_pos])
        assert food.get_position() != initial_pos
        
    def test_food_spawn_exclude(self):
        """Test food spawning with excluded positions"""
        food = Food()
        # Exclude some positions
        initial_pos = food.get_position()
        exclude = [initial_pos, (0, 0), (0, 1), (1, 0), (1, 1)]
        food.spawn(exclude_positions=exclude)
        assert food.get_position() not in exclude

class TestGameBoard:
    """Tests for GameBoard class"""
    
    def test_bounds_checking(self):
        """Test bounds checking"""
        board = GameBoard(10, 10)
        assert board.is_within_bounds((0, 0)) is True
        assert board.is_within_bounds((9, 9)) is True
        assert board.is_within_bounds((10, 10)) is False
        assert board.is_within_bounds((-1, 0)) is False
    
    def test_wall_collision(self):
        """Test wall collision"""
        board = GameBoard(10, 10)
        assert board.check_wall_collision((0, 0)) is False
        assert board.check_wall_collision((10, 0)) is True

class TestSnakeGame:
    """Tests for SnakeGame class"""
    
    def test_initial_state(self):
        """Test initial game state"""
        from src.game import SnakeGame
        game = SnakeGame()
        assert game.score == 0
        assert game.game_over is False
        assert game.game_running is True
        assert len(game.snake.get_body()) > 0
        
    def test_snake_eating_food(self):
        """Test snake eating food logic"""
        from src.game import SnakeGame
        game = SnakeGame()
        initial_score = game.score
        initial_length = len(game.snake.get_body())
        
        center_x = BOARD_WIDTH // 2
        center_y = BOARD_HEIGHT // 2
        
        # Place food directly in front of snake
        game.food.position = (center_x, center_y + 1)
        game.snake.direction = 'DOWN'
        
        game.update()
        
        assert game.score == initial_score + 1
        assert len(game.snake.get_body()) == initial_length + 1
        
    def test_wall_collision(self):
        """Test wall collision ends game"""
        from src.game import SnakeGame
        game = SnakeGame()
        # Teleport snake to edge
        game.snake.body = [(0, 0)]
        game.snake.direction = 'LEFT'
        
        game.update()
        
        assert game.game_over is True
        assert game.game_running is False
        
    def test_self_collision(self):
        """Test self collision ends game"""
        from src.game import SnakeGame
        game = SnakeGame()
        # Create a snake that hits itself
        game.snake.body = [(2, 2), (1, 2), (1, 3), (2, 3), (3, 3)]
        game.snake.direction = 'DOWN'
        
        game.update()
        
        assert game.game_over is True
        assert game.game_running is False
        
    def test_is_game_over(self):
        """Test is_game_over method"""
        from src.game import SnakeGame
        game = SnakeGame()
        assert game.is_game_over() is False
        game.game_over = True
        assert game.is_game_over() is True
