"""Game settings and configuration."""

from typing import Final, Tuple

# Display settings
WINDOW_SIZE: Final[Tuple[int, int]] = (800, 600)
WIDTH: Final[int] = WINDOW_SIZE[0]
HEIGHT: Final[int] = WINDOW_SIZE[1]
GRID_SIZE: Final[int] = 20
CELL_SIZE: Final[int] = 32
COLUMNS: Final[int] = WIDTH // GRID_SIZE
ROWS: Final[int] = HEIGHT // GRID_SIZE
FPS: Final[int] = 60
SPEED: Final[int] = 5
VSYNC: Final[bool] = True
SHOW_FPS: Final[bool] = True
FULLSCREEN: Final[bool] = False

# Asset paths
# Font path - relative to project root
FONT: Final[str] = "Data/assets/font.ttf"

# File paths
SETTINGS_FILE: Final[str] = "Data/config.json"

# Game settings
INIT_MOVE_DELAY = 150  # Initial movement delay in milliseconds
MIN_MOVE_DELAY = 50  # Minimum movement delay (maximum speed)
SPEED_STEP = 5  # How much to decrease delay when eating food
WRAP_AROUND = False  # Whether snake can wrap around screen edges
USE_OBSTACLES = True  # Whether to generate obstacles
INITIAL_SNAKE_SIZE = 3  # Initial length of the snake
POWERUP_ENABLED = True  # Whether power-ups are enabled
POWERUP_CHANCE = 0.2  # Chance of spawning a power-up when eating food
POWERUP_DURATION = 5000  # Duration of power-ups in milliseconds

# Power-up types and their effects
POWERUP_TYPES = ["speed", "grow", "invincible", "score"]
POWERUP_EFFECTS = {
    "speed": {"duration": 5000, "multiplier": 2.0},
    "grow": {"amount": 3},
    "invincible": {"duration": 3000},
    "score": {"points": 5},
}

# Visual settings
BACKGROUND_COLOR = (0, 0, 0)  # Black
SNAKE_COLOR = (0, 255, 0)  # Green
FOOD_COLOR = (255, 0, 0)  # Red
OBSTACLE_COLOR = (128, 128, 128)  # Gray
GRID_COLOR = (50, 50, 50)  # Dark gray
POWERUP_COLORS = {
    "speed": (255, 255, 0),  # Yellow
    "grow": (0, 255, 255),  # Cyan
    "invincible": (255, 0, 255),  # Magenta
    "score": (255, 215, 0),  # Gold
}

# Audio settings
MUSIC_VOLUME = 0.5
EFFECTS_VOLUME = 0.7
MUSIC_ENABLED = True
EFFECTS_ENABLED = True

# Profile settings
DEFAULT_PROFILE = "default"
SAVE_HIGHSCORES = True
MAX_HIGHSCORES = 10

# Debug settings
DEBUG_MODE = False
SHOW_GRID = True
LOG_LEVEL = "INFO"
