"""Main Game Engine"""

import time
import pygame
from src.snake import Snake
from src.food import Food
from src.game_board import GameBoard
from src.config import BOARD_WIDTH, BOARD_HEIGHT, GAME_SPEED, INITIAL_SNAKE_LENGTH
from src.utils import is_valid_direction

class SnakeGame:
    """Main game class managing game state and logic"""
    
    def __init__(self):
        """Initialize the game with all components and initial state"""
        # Initialize game board
        self.board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT)
        
        # Initialize snake at center of board
        center_x = BOARD_WIDTH // 2
        center_y = BOARD_HEIGHT // 2
        self.snake = Snake((center_x, center_y), INITIAL_SNAKE_LENGTH)
        
        # Initialize food at random position (excluding snake body)
        self.food = Food()
        self.food.spawn(exclude_positions=self.snake.get_body())
        
        # Initialize game state variables
        self.score = 0
        self.game_over = False
        self.game_running = True
    
    def run(self):
        """Main game loop - continuously update, render, and handle input
        
        Structure:
            - Loop while game is running
            - Handle user input
            - Update game state
            - Render the game
            - Control game speed with sleep
        """
        # Initialize pygame for input handling
        pygame.init()
        
        while self.game_running and not self.game_over:
            # Handle user input
            self.handle_input()
            
            # Update game state
            self.update()
            
            # Render the game
            self.render()
            
            # Control game speed
            time.sleep(GAME_SPEED)
        
        # Game over - display final score
        print(f"\nGame Over! Final Score: {self.score}")
    
    def update(self):
        """Update game state each frame
        
        Logic:
            - Move snake in current direction
            - Check food collision (increase score, respawn food, grow snake)
            - Check wall collision (game over)
            - Check self collision (game over)
        """
        # Move the snake in current direction
        self.snake.move(self.snake.direction)
        
        # Check if snake ate the food
        if self.snake.get_head_position() == self.food.get_position():
            # Snake ate food - grow and increase score
            self.snake.grow()
            self.score += 1
            # Respawn food at new position (excluding snake body)
            self.food.spawn(exclude_positions=self.snake.get_body())
        
        # Check for collisions
        if self.check_collisions():
            self.game_over = True
            self.game_running = False
    
    def render(self):
        """Render the game to display
        
        Display:
            - Clear screen
            - Draw board boundaries
            - Draw snake (head and body)
            - Draw food
            - Display score and game status
        """
        # Clear the screen (using escape sequence for basic rendering)
        print("\033[2J\033[H", end="")
        
        # Create empty board
        board_2d = []
        for y in range(BOARD_HEIGHT):
            row = []
            for x in range(BOARD_WIDTH):
                row.append('.')
            board_2d.append(row)
        
        # Add snake to board
        snake_body = self.snake.get_body()
        for i, segment in enumerate(snake_body):
            x, y = segment
            if i == 0:
                board_2d[y][x] = 'O'  # Head
            else:
                board_2d[y][x] = 'o'  # Body
        
        # Add food to board
        food_x, food_y = self.food.get_position()
        board_2d[food_y][food_x] = '*'
        
        # Print board
        print(f"Score: {self.score}")
        print("+" + "-" * (BOARD_WIDTH) + "+")
        for row in board_2d:
            print("|" + "".join(row) + "|")
        print("+" + "-" * (BOARD_WIDTH) + "+")
    
    def handle_input(self):
        """Handle user keyboard input
        
        Controls:
            - Arrow keys or WASD for direction
            - Q or ESC to quit game
            - Validate direction changes (no 180-degree turns)
        """
        # Get pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                return
            
            if event.type == pygame.KEYDOWN:
                current_dir = self.snake.direction
                new_dir = None
                
                # Handle direction controls (Arrow keys or WASD)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    new_dir = 'UP'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    new_dir = 'DOWN'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    new_dir = 'LEFT'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    new_dir = 'RIGHT'
                
                # Handle quit controls
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.game_running = False
                    return
                
                # Update direction if new direction is valid
                if new_dir is not None and is_valid_direction(current_dir, new_dir):
                    self.snake.direction = new_dir
    
    def check_collisions(self):
        """Check for all collision types that end the game
        
        Returns:
            bool: True if any collision detected (game over), False otherwise
            
        Checks:
            - Wall collision (snake head hits board boundary)
            - Self collision (snake head hits its own body)
        
        Note: Food collision is handled separately in update() as it doesn't end the game
        """
        # Check wall collision
        head_pos = self.snake.get_head_position()
        if self.board.check_wall_collision(head_pos):
            return True
        
        # Check self collision
        if self.snake.check_self_collision():
            return True
        
        return False
    
    def is_game_over(self):
        """Check if the game has ended
        
        Returns:
            bool: Current state of the game_over flag
        """
        return self.game_over
