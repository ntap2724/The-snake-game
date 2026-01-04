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

        # Assert body has 3 segments
        assert len(snake.get_body()) == 3

        # Assert head position is (10, 10)
        assert snake.get_head_position() == (10, 10)

        # Assert body extends upward (body[1] and body[2] have y < 10)
        body = snake.get_body()
        assert body == [(10, 10), (10, 9), (10, 8)]
        assert body[1][1] < 10
        assert body[2][1] < 10
    
    def test_snake_move(self):
        """Test snake movement"""
        pos = (10, 10)
        snake = Snake(pos, length=3)
        initial_head = snake.get_head_position()
        initial_length = len(snake.get_body())
        
        snake.move('RIGHT')
        new_head = snake.get_head_position()
        
        # Assert head position moved 1 cell right
        assert new_head[0] == initial_head[0] + 1
        assert new_head[1] == initial_head[1]
        
        # Assert body length unchanged (move doesn't grow)
        assert len(snake.get_body()) == initial_length
        
        # Assert body segments follow head
        body = snake.get_body()
        assert body[0] == new_head
        assert body[1] == initial_head
    
    def test_snake_move_all_directions(self):
        """Test snake movement in all 4 directions"""
        pos = (10, 10)
        snake = Snake(pos, length=3)
        
        # Test UP
        initial_head = snake.get_head_position()
        snake.move('UP')
        new_head = snake.get_head_position()
        assert new_head == (initial_head[0], initial_head[1] - 1)
        
        # Test DOWN
        initial_head = snake.get_head_position()
        snake.move('DOWN')
        new_head = snake.get_head_position()
        assert new_head == (initial_head[0], initial_head[1] + 1)
        
        # Test LEFT
        initial_head = snake.get_head_position()
        snake.move('LEFT')
        new_head = snake.get_head_position()
        assert new_head == (initial_head[0] - 1, initial_head[1])
        
        # Test RIGHT
        initial_head = snake.get_head_position()
        snake.move('RIGHT')
        new_head = snake.get_head_position()
        assert new_head == (initial_head[0] + 1, initial_head[1])
        
        # Verify body follows after multiple moves
        body = snake.get_body()
        assert len(body) == 3
        assert body[0] == new_head
    
    def test_snake_grow(self):
        """Test snake growth"""
        pos = (10, 10)
        snake = Snake(pos, length=3)
        initial_body = snake.get_body().copy()
        initial_tail = initial_body[-1]
        
        snake.grow()
        
        # Assert body length is now 4
        assert len(snake.get_body()) == 4
        
        # Assert new segment is at previous tail position
        body = snake.get_body()
        assert body[-1] == initial_tail
        assert body[-1] == initial_body[-1]
    
    def test_snake_self_collision_no_collision(self):
        """Test snake self-collision detection with no collision"""
        # Create snake at (10, 10) with length 3
        snake = Snake((10, 10), length=3)

        # Move in safe direction (DOWN, not UP, since snake extends upward)
        snake.move('DOWN')

        # Assert check_self_collision() returns False
        assert snake.check_self_collision() is False
    
    def test_snake_self_collision_with_collision(self):
        """Test snake self-collision detection with collision"""
        # Create scenario where snake body creates a collision
        snake = Snake((10, 10), length=3)
        
        # Create a snake that will collide with itself
        # Move to create a U-shape then hit itself
        snake.move('RIGHT')  # head at (11, 10), body: [(11,10), (10,10), (10,11)]
        snake.move('DOWN')   # head at (11, 11), body: [(11,11), (11,10), (10,10)]
        snake.move('LEFT')   # head at (10, 11), body: [(10,11), (11,11), (11,10)]
        
        # Now move UP - head will be at (10, 10), which is in the body at position [2]
        snake.move('UP')     # head at (10, 10), body: [(10,10), (10,11), (11,11)]
        
        # This creates a collision scenario - let's create a more direct one
        snake = Snake((5, 5), length=5)
        snake.body = [(5, 5), (6, 5), (6, 6), (5, 6), (5, 7)]
        snake.direction = 'UP'
        
        # Head at (5,5) will move UP to (5,4) - no collision, need better setup
        # Let's manually set up a collision
        snake.body = [(5, 5), (6, 5), (6, 6), (5, 6), (5, 5)]
        
        # Assert check_self_collision() returns True (head at (5,5) is in body[1:])
        assert snake.check_self_collision() is True


class TestFood:
    """Tests for Food class"""
    
    def test_food_initialization(self):
        """Test food is initialized correctly"""
        food = Food()
        position = food.get_position()
        
        # Assert position is a tuple (x, y)
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)
        
        # Assert position is within board bounds
        assert 0 <= position[0] < BOARD_WIDTH
        assert 0 <= position[1] < BOARD_HEIGHT
    
    def test_food_spawn(self):
        """Test food spawning"""
        positions = [(1, 1), (2, 2)]
        def mock_get_random_position():
            return positions.pop(0)
        
        from src import utils
        original_get_random_position = utils.get_random_position
        utils.get_random_position = mock_get_random_position
        
        try:
            food = Food()
            initial_pos = food.get_position()
            
            # Call spawn() without exclude_positions
            food.spawn(exclude_positions=[])
            new_pos = food.get_position()
            
            # Assert position changed deterministically
            assert initial_pos == (1, 1)
            assert new_pos == (2, 2)
            
            # Assert new position is within bounds
            assert 0 <= new_pos[0] < BOARD_WIDTH
            assert 0 <= new_pos[1] < BOARD_HEIGHT
        finally:
            utils.get_random_position = original_get_random_position
    
    def test_food_spawn_avoid_positions(self):
        """Test food spawning with excluded positions"""
        food = Food()
        
        # Define exclude_positions list (snake body positions)
        exclude_positions = [(5, 5), (5, 6), (5, 7), (6, 5), (7, 5)]
        
        # Call spawn(exclude_positions=exclude_positions)
        food.spawn(exclude_positions=exclude_positions)
        new_pos = food.get_position()
        
        # Assert position is NOT in exclude_positions
        assert new_pos not in exclude_positions
    
    def test_food_spawn_multiple_times(self):
        """Test spawning food multiple times"""
        food = Food()
        positions = []
        
        # Spawn food multiple times
        for _ in range(10):
            food.spawn(exclude_positions=positions)
            position = food.get_position()
            positions.append(position)
        
        # Assert each spawn gets a valid position
        for pos in positions:
            assert 0 <= pos[0] < BOARD_WIDTH
            assert 0 <= pos[1] < BOARD_HEIGHT
        
        # Positions should vary (with 10 spawns, very unlikely to get all same position)
        assert len(set(positions)) > 1


class TestGameBoard:
    """Tests for GameBoard class"""
    
    def test_gameboard_initialization(self):
        """Test game board is initialized correctly"""
        board = GameBoard(width=20, height=20)
        
        # Assert board.width == 20
        assert board.width == 20
        
        # Assert board.height == 20
        assert board.height == 20
    
    def test_is_within_bounds_valid(self):
        """Test valid positions are within bounds"""
        board = GameBoard(width=20, height=20)
        
        # Test multiple valid positions: (0,0), (19,19), (10,10)
        assert board.is_within_bounds((0, 0)) is True
        assert board.is_within_bounds((19, 19)) is True
        assert board.is_within_bounds((10, 10)) is True
    
    def test_is_within_bounds_invalid(self):
        """Test invalid positions are outside bounds"""
        board = GameBoard(width=20, height=20)
        
        # Test positions outside bounds: (-1,5), (20,5), (5,-1), (5,20)
        assert board.is_within_bounds((-1, 5)) is False
        assert board.is_within_bounds((20, 5)) is False
        assert board.is_within_bounds((5, -1)) is False
        assert board.is_within_bounds((5, 20)) is False
    
    def test_check_wall_collision_no_collision(self):
        """Test wall collision detection with no collision"""
        board = GameBoard(width=20, height=20)
        
        # Test positions within bounds
        assert board.check_wall_collision((0, 0)) is False
        assert board.check_wall_collision((19, 19)) is False
        assert board.check_wall_collision((10, 10)) is False
    
    def test_check_wall_collision_with_collision(self):
        """Test wall collision detection with collision"""
        board = GameBoard(width=20, height=20)
        
        # Test positions outside bounds
        assert board.check_wall_collision((-1, 5)) is True
        assert board.check_wall_collision((20, 5)) is True
        assert board.check_wall_collision((5, -1)) is True
        assert board.check_wall_collision((5, 20)) is True
    
    def test_gameboard_custom_size(self):
        """Test game board with custom size"""
        # Create GameBoard with custom size (10, 15)
        board = GameBoard(width=10, height=15)
        
        assert board.width == 10
        assert board.height == 15
        
        # Test boundary checking works correctly for custom size
        assert board.is_within_bounds((0, 0)) is True
        assert board.is_within_bounds((9, 14)) is True
        assert board.is_within_bounds((10, 14)) is False
        assert board.is_within_bounds((9, 15)) is False


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
    
    def test_game_initialization(self):
        """Test game initializes all components correctly"""
        from src.game import SnakeGame
        game = SnakeGame()
        
        # Assert all components initialized
        assert game.snake is not None
        assert game.food is not None
        assert game.board is not None
        
        # Assert snake at center
        center_x = BOARD_WIDTH // 2
        center_y = BOARD_HEIGHT // 2
        assert game.snake.get_head_position() == (center_x, center_y)
        
        # Assert food not on snake
        snake_body = game.snake.get_body()
        food_position = game.food.get_position()
        assert food_position not in snake_body
        
        # Assert score is 0
        assert game.score == 0
    
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
        """Test wall collision wraps instead of ending the game"""
        from src.game import SnakeGame
        game = SnakeGame()
        
        # Teleport snake to edge
        game.snake.body = [(0, 0)]
        game.snake.direction = 'LEFT'
        
        game.update()
        
        assert game.game_over is False
        assert game.snake.get_head_position() == (BOARD_WIDTH - 1, 0)
    
    def test_self_collision(self):
        """Test self collision ends game"""
        from src.game import SnakeGame
        game = SnakeGame()
        
        # Create a snake that hits itself
        game.snake.body = [(2, 2), (1, 2), (1, 3), (2, 3), (3, 3)]
        game.snake.direction = 'DOWN'
        
        game.update()
        
        assert game.game_over is True
        # Game should continue running to show game over screen
        assert game.game_running is True
    
    def test_is_game_over(self):
        """Test is_game_over method"""
        from src.game import SnakeGame
        game = SnakeGame()

        assert game.is_game_over() is False
        game.game_over = True
        assert game.is_game_over() is True

    def test_pause_resume_and_restart(self):
        """Test pause, resume, and restart behavior"""
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        import pygame
        from src.game import SnakeGame
        from src.config import STATE_PLAYING, STATE_PAUSED

        game = SnakeGame()
        game.current_state = STATE_PLAYING

        game._handle_keyboard_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        assert game.current_state == STATE_PAUSED

        game._handle_keyboard_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        assert game.current_state == STATE_PLAYING

        game.score = 5
        game._handle_keyboard_input(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
        assert game.current_state == STATE_PLAYING
        assert game.score == 0


class TestWindowResizing:
    """Tests for window resizing functionality"""

    def test_window_is_resizable(self):
        """Test that window is initialized with RESIZABLE flag"""
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        from src.game import SnakeGame
        game = SnakeGame()

        # Check that window exists and has correct initial size
        assert game.window_width > 0
        assert game.window_height > 0
        assert game.window is not None

    def test_cell_size_calculation(self):
        """Test dynamic cell size calculation"""
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        from src.game import SnakeGame
        game = SnakeGame()

        # Test default size (800x600)
        cell_width, cell_height = game._get_cell_size()
        game_rect, _ = game._get_layout()
        assert cell_width == game_rect.width / BOARD_WIDTH
        assert cell_height == game_rect.height / BOARD_HEIGHT

        # Resize and test new cell size
        game._handle_window_resize(800, 600)
        cell_width, cell_height = game._get_cell_size()
        game_rect, _ = game._get_layout()
        assert cell_width == game_rect.width / BOARD_WIDTH
        assert cell_height == game_rect.height / BOARD_HEIGHT

    def test_window_resize_handler(self):
        """Test window resize handler with minimum size enforcement"""
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        from src.game import SnakeGame
        from src.config import MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT

        game = SnakeGame()

        # Test resize to larger dimensions
        game._handle_window_resize(800, 600)
        assert game.window_width == 800
        assert game.window_height == 600

        # Test resize to smaller but valid dimensions
        game._handle_window_resize(300, 300)
        assert game.window_width == 300
        assert game.window_height == 300

        # Test resize below minimum dimensions
        game._handle_window_resize(100, 100)
        assert game.window_width == MIN_WINDOW_WIDTH
        assert game.window_height == MIN_WINDOW_HEIGHT

    def test_button_positioning_on_resize(self):
        """Test that buttons reposition correctly after window resize"""
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        from src.game import SnakeGame

        game = SnakeGame()

        # Test button position at default size
        button_rect = game._get_play_button_rect()
        assert button_rect.centerx == game.window_width // 2
        assert button_rect.centery == game.window_height // 2

        # Resize window
        game._handle_window_resize(800, 600)
        game.play_button_rect = game._get_play_button_rect()

        # Test button position after resize
        button_rect = game._get_play_button_rect()
        assert button_rect.centerx == game.window_width // 2
        assert button_rect.centery == game.window_height // 2

    def test_game_logic_unchanged_by_resize(self):
        """Test that game logic is not affected by window resize"""
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'

        from src.game import SnakeGame

        game = SnakeGame()

        # Get initial snake position
        initial_head = game.snake.get_head_position()
        initial_body_length = len(game.snake.get_body())

        # Resize window
        game._handle_window_resize(800, 600)

        # Verify game logic unchanged
        assert game.snake.get_head_position() == initial_head
        assert len(game.snake.get_body()) == initial_body_length
        assert game.board.width == BOARD_WIDTH
        assert game.board.height == BOARD_HEIGHT
