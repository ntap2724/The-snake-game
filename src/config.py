# Game Configuration
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
GRID_SIZE = 20
GAME_SPEED_INITIAL = 0.1  # seconds per move (10 moves per second)
GAME_SPEED_MIN = 0.04  # fastest allowed speed (25 moves per second)
GAME_SPEED_STEP = 0.005  # speed increase per food eaten
INITIAL_SNAKE_LENGTH = 3

# Game States
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_PAUSED = "paused"

# Colors (for pygame)
COLOR_SNAKE_HEAD = (0, 255, 0)
COLOR_SNAKE_BODY = (0, 200, 0)
COLOR_FOOD = (255, 0, 0)
COLOR_BACKGROUND = (0, 0, 0)
COLOR_BORDER = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (0, 150, 0)
COLOR_BUTTON_HOVER = (0, 200, 0)
COLOR_BUTTON_TEXT = (255, 255, 255)
COLOR_TITLE = (255, 255, 255)
COLOR_SUBTITLE = (200, 200, 200)
COLOR_HIGHLIGHT = (255, 255, 0)

# UI Configuration
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

# Window Configuration
MIN_WINDOW_WIDTH = 300
MIN_WINDOW_HEIGHT = 300
