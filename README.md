# The Snake Game

A classic Snake game implementation in Python.

## Description
A simple but complete Snake game where players control a snake to eat food and grow longer while avoiding collisions with walls and the snake's own body.

## Installation

1. Clone the repository
2. Create a virtual environment:
   **Windows (PowerShell or CMD):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Mac/Linux (Bash/Zsh):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the package:
   ```bash
   pip install -e .
   ```

## How to Run

```bash
python -m src.main
```

Or:
```bash
snakegame
```

## Game Controls

- **Arrow Keys**: Move the snake (Up, Down, Left, Right)
- **Q**: Quit the game

## Game Mechanics

- Control the snake to eat food
- Each food eaten increases your score by 1
- Snake grows longer with each food eaten
- Game ends if snake collides with walls or itself
- Game speed increases as score increases

## Project Structure

```
src/
  ├── main.py        - Game entry point
  ├── game.py        - Core game engine
  ├── snake.py       - Snake class
  ├── food.py        - Food class
  ├── game_board.py  - Game board/arena
  ├── config.py      - Configuration constants
  └── utils.py       - Utility functions

tests/
  └── test_game.py   - Unit tests
```

## Development

Run tests:
```bash
pytest tests/
```

## Requirements

- Python 3.10+
- Pygame 2.5.3+ (for rendering)
- Pytest 7.4.3 (for testing)
- setuptools
- wheel

## Future Enhancements

- Sound effects
- Multiple difficulty levels
- Highscore tracking
- Power-ups and obstacles
