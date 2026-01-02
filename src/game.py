"""Main Game Engine"""

import time
import pygame
from src.snake import Snake
from src.food import Food
from src.game_board import GameBoard
from src.config import (BOARD_WIDTH, BOARD_HEIGHT, GAME_SPEED, INITIAL_SNAKE_LENGTH,
                       GRID_SIZE, COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY, COLOR_FOOD,
                       COLOR_BACKGROUND, COLOR_BORDER)
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
        
        # Initialize pygame display
        pygame.init()
        self.window_width = BOARD_WIDTH * GRID_SIZE
        self.window_height = BOARD_HEIGHT * GRID_SIZE
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 72)
    
    def run(self):
        """Main game loop - continuously update, render, and handle input

        Structure:
            - Loop while game is running
            - Handle user input
            - Update game state
            - Render the game
            - Control game speed with sleep
        """
        while self.game_running and not self.game_over:
            # Handle user input
            self.handle_input()

            # Update game state
            self.update()

            # Render the game
            self.render()

            # Control game speed
            time.sleep(GAME_SPEED)

        # Game over - render final state
        self.render_game_over()

        # Wait for user to close window
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                    (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
                    waiting = False

        pygame.quit()
    
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
        # Fill background
        self.window.fill(COLOR_BACKGROUND)

        # Draw border
        pygame.draw.rect(self.window, COLOR_BORDER, (0, 0, self.window_width, self.window_height), 2)

        # Draw food as red circle
        food_x, food_y = self.food.get_position()
        food_rect = (food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.circle(self.window, COLOR_FOOD,
                          (food_x * GRID_SIZE + GRID_SIZE // 2, food_y * GRID_SIZE + GRID_SIZE // 2),
                          GRID_SIZE // 2 - 2)

        # Draw snake body (lighter green)
        snake_body = self.snake.get_body()
        for i, segment in enumerate(snake_body):
            x, y = segment
            if i == 0:
                # Head (bright green)
                pygame.draw.circle(self.window, COLOR_SNAKE_HEAD,
                                  (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
                                  GRID_SIZE // 2 - 2)
            else:
                # Body (lighter green)
                pygame.draw.circle(self.window, COLOR_SNAKE_BODY,
                                  (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
                                  GRID_SIZE // 2 - 2)

        # Draw score at top
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_BORDER)
        self.window.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()

    def render_game_over(self):
        """Render game over screen with final score"""
        # Fill background
        self.window.fill(COLOR_BACKGROUND)

        # Draw border
        pygame.draw.rect(self.window, COLOR_BORDER, (0, 0, self.window_width, self.window_height), 2)

        # Render "Game Over" text
        game_over_text = self.game_over_font.render("Game Over!", True, COLOR_SNAKE_HEAD)
        game_over_rect = game_over_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))
        self.window.blit(game_over_text, game_over_rect)

        # Render final score
        score_text = self.font.render(f"Final Score: {self.score}", True, COLOR_BORDER)
        score_rect = score_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
        self.window.blit(score_text, score_rect)

        # Render quit instruction
        quit_text = self.font.render("Press Q or ESC to quit", True, COLOR_BORDER)
        quit_rect = quit_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 60))
        self.window.blit(quit_text, quit_rect)

        # Update display
        pygame.display.flip()

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
