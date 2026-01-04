"""Main Game Engine"""

import time
import pygame
from src.snake import Snake
from src.food import Food
from src.game_board import GameBoard
from src.high_score import HighScoreManager
from src.config import (BOARD_WIDTH, BOARD_HEIGHT, GAME_SPEED_INITIAL, GAME_SPEED_MIN,
                        GAME_SPEED_STEP, INITIAL_SNAKE_LENGTH,
                        GRID_SIZE, COLOR_SNAKE_HEAD, COLOR_SNAKE_BODY, COLOR_FOOD,
                        COLOR_BACKGROUND, COLOR_BORDER, COLOR_TEXT, COLOR_BUTTON,
                        COLOR_BUTTON_HOVER, COLOR_BUTTON_TEXT, COLOR_TITLE, COLOR_SUBTITLE,
                        COLOR_HIGHLIGHT, STATE_MENU, STATE_PLAYING, STATE_GAME_OVER,
                        STATE_PAUSED,
                        BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN, PANEL_WIDTH,
                        MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
from src.utils import is_valid_direction

class SnakeGame:
    """Main game class managing game state and logic"""
    
    def __init__(self):
        """Initialize the game with all components and initial state"""
        # Initialize game board
        self.board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT)

        # Initialize high score manager
        self.high_score_manager = HighScoreManager()

        # Initialize pygame display with resizable flag
        pygame.init()
        self.window_width = MIN_WINDOW_WIDTH
        self.window_height = MIN_WINDOW_HEIGHT
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption("Snake Game")

        # Initialize fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        self.font_title = pygame.font.Font(None, 96)

        # Initialize game state - start in menu for new behavior
        self.current_state = STATE_MENU
        self.play_button_rect = self._get_play_button_rect()

        # Initialize game objects (for backward compatibility with tests)
        self._initialize_game_objects()

        # Game state variables
        self.score = 0
        self.game_over = False
        self.game_running = True
        self.is_new_high_score = False
        self.game_speed = GAME_SPEED_INITIAL

        # Collision grace period to prevent immediate collision detection
        self.collision_grace_period = 3  # Allow 3 frames before collision detection

    def _get_layout(self):
        """Calculate layout rectangles for game and UI panels"""
        available_width = max(0, self.window_width - PANEL_WIDTH)
        game_size = min(available_width, self.window_height)
        game_size = max(0, game_size)

        game_rect = pygame.Rect(0, 0, game_size, game_size)
        game_rect.y = (self.window_height - game_rect.height) // 2

        ui_rect = pygame.Rect(game_rect.width, 0, self.window_width - game_rect.width, self.window_height)
        return game_rect, ui_rect

    def _get_cell_size(self):
        """Calculate cell size dynamically based on current game area dimensions"""
        game_rect, _ = self._get_layout()
        cell_width = game_rect.width / BOARD_WIDTH if BOARD_WIDTH else 0
        cell_height = game_rect.height / BOARD_HEIGHT if BOARD_HEIGHT else 0
        return cell_width, cell_height

    def _handle_window_resize(self, width, height):
        """Handle window resize event

        Args:
            width: New window width
            height: New window height
        """
        # Enforce minimum window size
        self.window_width = max(width, MIN_WINDOW_WIDTH)
        self.window_height = max(height, MIN_WINDOW_HEIGHT)

        # Update the display surface
        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

    def _get_play_button_rect(self):
        """Get the rectangle for the play button"""
        center_x = self.window_width // 2
        center_y = self.window_height // 2
        return pygame.Rect(
            center_x - BUTTON_WIDTH // 2,
            center_y - BUTTON_HEIGHT // 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
    
    def _initialize_game_objects(self):
        """Initialize snake and food for a new game"""
        # Initialize snake at center of board
        center_x = BOARD_WIDTH // 2
        center_y = BOARD_HEIGHT // 2
        self.snake = Snake((center_x, center_y), INITIAL_SNAKE_LENGTH)
        
        # Set initial direction to something safe to prevent immediate collision
        self.snake.direction = 'RIGHT'  # Safe initial direction
        
        # Initialize food at random position (excluding snake body)
        self.food = Food()
        self.food.spawn(exclude_positions=self.snake.get_body())
        
        # Initialize game state variables
        self.score = 0
        self.game_over = False
        self.is_new_high_score = False
        self.game_speed = GAME_SPEED_INITIAL
        
        # Reset collision grace period for new game
        self.collision_grace_period = 3
    
    def run(self):
        """Main game loop - continuously update, render, and handle input

        Structure:
            - Loop while game is running
            - Handle user input
            - Update game state (only if playing)
            - Render the game (different screens for different states)
            - Control game speed with sleep
        """
        while self.game_running:
            # Handle user input
            self.handle_input()

            # Update game state (only if playing)
            if self.current_state == STATE_PLAYING:
                self.update()

            # Render the game
            self.render()

            # Control game speed (only if playing)
            if self.current_state == STATE_PLAYING:
                time.sleep(self.game_speed)
            else:
                # Small delay for menu and game over screens to reduce CPU usage
                time.sleep(0.016)  # ~60 FPS for UI screens

        pygame.quit()
    
    def update(self):
        """Update game state each frame
        
        Logic:
            - Move snake in current direction
            - Check food collision (increase score, respawn food, grow snake)
            - Check wall collision (game over)
            - Check self collision (game over)
        """
        # Store previous body to check for collision properly
        previous_body = self.snake.get_body().copy()
        
        # Move the snake in current direction
        self.snake.move(self.snake.direction)
        
        # Check if snake ate the food
        if self.snake.get_head_position() == self.food.get_position():
            # Snake ate food - grow and increase score
            self.snake.grow()
            self.score += 1
            self.game_speed = max(GAME_SPEED_MIN, self.game_speed - GAME_SPEED_STEP)
            # Respawn food at new position (excluding snake body)
            self.food.spawn(exclude_positions=self.snake.get_body())

        head_position = self.snake.get_head_position()
        if not self.board.is_within_bounds(head_position):
            self.snake.body[0] = self.board.wrap_position(head_position)

        # Check for collisions using the proper logic
        if self._check_collisions(previous_body):
            self._end_game()
    
    def _check_collisions(self, previous_body):
        """Check for all collision types that end the game
        
        Args:
            previous_body: Body state before the current move
            
        Returns:
            bool: True if any collision detected (game over), False otherwise
            
        Checks:
            - Wall collision (snake head hits board boundary)
            - Self collision (snake head hits its own body, using previous state)
        
        Note: Food collision is handled separately in update() as it doesn't end the game
        """
        # Check self collision using the previous body state
        # Fix: Check if head position is in the body segments that were NOT the head
        # This prevents false collision when snake moves into the space vacated by its tail
        head_position = self.snake.get_head_position()
        # Check against previous body segments excluding what was the previous head
        # This allows the snake to move into the space where its tail was
        body_without_head = previous_body[1:]  # All segments except the previous head
        if head_position in body_without_head:
            return True
        
        return False
    
    def _end_game(self):
        """End the current game and update high scores"""
        self.game_over = True
        self.current_state = STATE_GAME_OVER
        
        # Update high scores
        self.is_new_high_score = self.high_score_manager.update_score(self.score)
        self.high_score_manager.update_last_game_score(self.score)
    
    def render(self):
        """Render the game to display based on current state"""
        # Clear screen
        self.window.fill(COLOR_BACKGROUND)

        # Draw layout borders
        game_rect, ui_rect = self._get_layout()
        pygame.draw.rect(self.window, COLOR_BORDER, game_rect, 2)
        pygame.draw.rect(self.window, COLOR_BORDER, ui_rect, 2)

        # Render based on current state
        if self.current_state == STATE_MENU:
            self._render_menu()
        elif self.current_state == STATE_PLAYING:
            self._render_game()
        elif self.current_state == STATE_PAUSED:
            self._render_paused()
        elif self.current_state == STATE_GAME_OVER:
            self._render_game_over()

        # Update display
        pygame.display.flip()
    
    def _render_menu(self):
        """Render the main menu screen"""
        # Draw title
        title_text = self.font_title.render("SNAKE GAME", True, COLOR_TITLE)
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 4))
        self.window.blit(title_text, title_rect)
        
        # Draw subtitle (instructions) - moved to center area
        subtitle_text = self.font_small.render(
            "Use Arrow Keys/WASD to move, P to pause, Q/ESC to quit",
            True,
            COLOR_SUBTITLE
        )
        subtitle_rect = subtitle_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 60))
        self.window.blit(subtitle_text, subtitle_rect)
        
        # Draw play button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_color = COLOR_BUTTON_HOVER if self.play_button_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        
        pygame.draw.rect(self.window, button_color, self.play_button_rect)
        pygame.draw.rect(self.window, COLOR_BORDER, self.play_button_rect, 2)
        
        # Draw button text
        button_text = self.font_medium.render("PLAY", True, COLOR_BUTTON_TEXT)
        button_text_rect = button_text.get_rect(center=self.play_button_rect.center)
        self.window.blit(button_text, button_text_rect)
        
        # Draw high score - moved to bottom area
        high_score = self.high_score_manager.get_high_score()
        high_score_text = self.font_medium.render(f"Best Score: {high_score}", True, COLOR_TEXT)
        high_score_rect = high_score_text.get_rect(center=(self.window_width // 2, self.window_height - 80))
        self.window.blit(high_score_text, high_score_rect)
        
        # Draw instructions
        instruction_text = self.font_small.render(
            "Click PLAY or press ENTER to start",
            True,
            COLOR_SUBTITLE
        )
        instruction_rect = instruction_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + BUTTON_HEIGHT + 30))
        self.window.blit(instruction_text, instruction_rect)
    
    def _render_game(self):
        """Render the active game screen"""
        game_rect, ui_rect = self._get_layout()

        # Get dynamic cell size
        cell_width, cell_height = self._get_cell_size()

        # Draw food as red circle
        food_x, food_y = self.food.get_position()
        pygame.draw.circle(self.window, COLOR_FOOD,
                          (game_rect.x + food_x * cell_width + cell_width / 2,
                           game_rect.y + food_y * cell_height + cell_height / 2),
                          min(cell_width, cell_height) / 2 - 2)

        # Draw snake body (lighter green)
        snake_body = self.snake.get_body()
        for i, segment in enumerate(snake_body):
            x, y = segment
            if i == 0:
                # Head (bright green)
                pygame.draw.circle(self.window, COLOR_SNAKE_HEAD,
                                  (game_rect.x + x * cell_width + cell_width / 2,
                                   game_rect.y + y * cell_height + cell_height / 2),
                                  min(cell_width, cell_height) / 2 - 2)
            else:
                # Body (lighter green)
                pygame.draw.circle(self.window, COLOR_SNAKE_BODY,
                                  (game_rect.x + x * cell_width + cell_width / 2,
                                   game_rect.y + y * cell_height + cell_height / 2),
                                  min(cell_width, cell_height) / 2 - 2)

        self._render_ui_panel(ui_rect)

    def _render_ui_panel(self, ui_rect):
        """Render score and controls inside the UI panel"""
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLOR_TEXT)
        score_rect = score_text.get_rect(topleft=(ui_rect.x + 20, ui_rect.y + 20))
        self.window.blit(score_text, score_rect)

        high_score = self.high_score_manager.get_high_score()
        high_score_text = self.font_small.render(f"Best: {high_score}", True, COLOR_TEXT)
        high_score_rect = high_score_text.get_rect(topleft=(ui_rect.x + 20, ui_rect.y + 60))
        self.window.blit(high_score_text, high_score_rect)

        speed_text = self.font_small.render(f"Speed: {self.game_speed:.3f}s", True, COLOR_TEXT)
        speed_rect = speed_text.get_rect(topleft=(ui_rect.x + 20, ui_rect.y + 85))
        self.window.blit(speed_text, speed_rect)

        button_y = ui_rect.y + 140
        button_width = max(0, ui_rect.width - 40)

        pause_label = "RESUME" if self.current_state == STATE_PAUSED else "PAUSE"
        pause_rect = pygame.Rect(ui_rect.x + 20, button_y, button_width, BUTTON_HEIGHT)
        restart_rect = pygame.Rect(ui_rect.x + 20, button_y + BUTTON_HEIGHT + 16, button_width, BUTTON_HEIGHT)
        menu_rect = pygame.Rect(ui_rect.x + 20, button_y + 2 * (BUTTON_HEIGHT + 16), button_width, BUTTON_HEIGHT)

        mouse_pos = pygame.mouse.get_pos()
        for rect, label in [
            (pause_rect, pause_label),
            (restart_rect, "RESTART"),
            (menu_rect, "MENU"),
        ]:
            color = COLOR_BUTTON_HOVER if rect.collidepoint(mouse_pos) else COLOR_BUTTON
            pygame.draw.rect(self.window, color, rect)
            pygame.draw.rect(self.window, COLOR_BORDER, rect, 2)
            text = self.font_medium.render(label, True, COLOR_BUTTON_TEXT)
            text_rect = text.get_rect(center=rect.center)
            self.window.blit(text, text_rect)

        self._current_button_rects = {
            'pause': pause_rect,
            'restart': restart_rect,
            'menu': menu_rect
        }
    
    def _render_game_over(self):
        """Render game over screen with final score and high score"""
        # Render "Game Over" text
        game_over_text = self.font_large.render("GAME OVER", True, COLOR_SNAKE_HEAD)
        game_over_rect = game_over_text.get_rect(center=(self.window_width // 2, self.window_height // 3))
        self.window.blit(game_over_text, game_over_rect)

        # Render final score
        score_text = self.font_medium.render(f"Your Score: {self.score}", True, COLOR_TEXT)
        score_rect = score_text.get_rect(center=(self.window_width // 2, self.window_height // 3 + 80))
        self.window.blit(score_text, score_rect)

        # Render high score (highlight if it was beaten)
        high_score = self.high_score_manager.get_high_score()
        if self.is_new_high_score:
            high_score_text = self.font_medium.render(f"NEW BEST SCORE! {high_score}", True, COLOR_HIGHLIGHT)
        else:
            high_score_text = self.font_medium.render(f"Best Score: {high_score}", True, COLOR_TEXT)
        
        high_score_rect = high_score_text.get_rect(center=(self.window_width // 2, self.window_height // 3 + 120))
        self.window.blit(high_score_text, high_score_rect)

        # Render buttons
        button_y = self.window_height // 3 + 180
        
        # Play Again button
        play_again_rect = pygame.Rect(
            self.window_width // 2 - BUTTON_WIDTH - BUTTON_MARGIN // 2,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        
        # Menu button
        menu_rect = pygame.Rect(
            self.window_width // 2 + BUTTON_MARGIN // 2,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        
        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        # Play Again button
        play_again_color = COLOR_BUTTON_HOVER if play_again_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(self.window, play_again_color, play_again_rect)
        pygame.draw.rect(self.window, COLOR_BORDER, play_again_rect, 2)
        
        # Menu button
        menu_color = COLOR_BUTTON_HOVER if menu_rect.collidepoint(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(self.window, menu_color, menu_rect)
        pygame.draw.rect(self.window, COLOR_BORDER, menu_rect, 2)
        
        # Draw button text
        play_again_text = self.font_medium.render("PLAY AGAIN", True, COLOR_BUTTON_TEXT)
        play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)
        self.window.blit(play_again_text, play_again_text_rect)
        
        menu_text = self.font_medium.render("MENU", True, COLOR_BUTTON_TEXT)
        menu_text_rect = menu_text.get_rect(center=menu_rect.center)
        self.window.blit(menu_text, menu_text_rect)

        # Render instructions
        instruction_text = self.font_small.render(
            "SPACE=Play Again, M=Menu, Q/ESC=Quit",
            True,
            COLOR_SUBTITLE
        )
        instruction_rect = instruction_text.get_rect(center=(self.window_width // 2, button_y + BUTTON_HEIGHT + 40))
        self.window.blit(instruction_text, instruction_rect)
        
        # Store button rects for click detection
        self._current_button_rects = {'play_again': play_again_rect, 'menu': menu_rect}

    def _render_paused(self):
        """Render paused state overlay"""
        self._render_game()

        overlay_text = self.font_large.render("PAUSED", True, COLOR_HIGHLIGHT)
        game_rect, _ = self._get_layout()
        overlay_rect = overlay_text.get_rect(center=game_rect.center)
        self.window.blit(overlay_text, overlay_rect)
    
    def handle_input(self):
        """Handle user keyboard input and mouse clicks based on current state"""
        # Get pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                return

            if event.type == pygame.VIDEORESIZE:
                self._handle_window_resize(event.w, event.h)
                # Update button positions after resize
                self.play_button_rect = self._get_play_button_rect()

            if event.type == pygame.KEYDOWN:
                self._handle_keyboard_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                self._handle_mouse_click(event.pos)
    
    def _handle_keyboard_input(self, event):
        """Handle keyboard input based on current state"""
        if self.current_state == STATE_MENU:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self._start_game()
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                self.game_running = False
                
        elif self.current_state == STATE_PLAYING:
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
            elif event.key == pygame.K_p:
                self.current_state = STATE_PAUSED
                return
            elif event.key == pygame.K_r:
                self._start_game()
                return
            
            # Update direction if new direction is valid
            if new_dir is not None and is_valid_direction(current_dir, new_dir):
                self.snake.direction = new_dir
                
        elif self.current_state == STATE_GAME_OVER:
            if event.key == pygame.K_SPACE:
                self._start_game()
            elif event.key == pygame.K_m:
                self._go_to_menu()
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                self.game_running = False
        elif self.current_state == STATE_PAUSED:
            if event.key == pygame.K_p or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.current_state = STATE_PLAYING
            elif event.key == pygame.K_r:
                self._start_game()
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                self.game_running = False
    
    def _handle_mouse_click(self, pos):
        """Handle mouse clicks for button interaction"""
        if self.current_state == STATE_MENU:
            if self.play_button_rect.collidepoint(pos):
                self._start_game()
                
        elif self.current_state == STATE_GAME_OVER:
            if hasattr(self, '_current_button_rects'):
                if self._current_button_rects['play_again'].collidepoint(pos):
                    self._start_game()
                elif self._current_button_rects['menu'].collidepoint(pos):
                    self._go_to_menu()
        elif self.current_state in {STATE_PLAYING, STATE_PAUSED}:
            if hasattr(self, '_current_button_rects'):
                if self._current_button_rects['pause'].collidepoint(pos):
                    self.current_state = STATE_PLAYING if self.current_state == STATE_PAUSED else STATE_PAUSED
                elif self._current_button_rects['restart'].collidepoint(pos):
                    self._start_game()
                elif self._current_button_rects['menu'].collidepoint(pos):
                    self._go_to_menu()
    
    def _start_game(self):
        """Start a new game"""
        self._initialize_game_objects()
        self.current_state = STATE_PLAYING
        self.game_running = True  # Ensure game_running is True for new game
    
    def _go_to_menu(self):
        """Return to the main menu"""
        self.current_state = STATE_MENU
        self.game_running = True  # Ensure game_running is True when going to menu
    
    def is_game_over(self):
        """Check if the game has ended (for backward compatibility)
        
        Returns:
            bool: Current state of the game_over flag
        """
        return self.game_over
