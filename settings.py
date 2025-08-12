# settings.py
import os

WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
COLUMNS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

# movimiento (delay en ms entre pasos de la serpiente)
INIT_MOVE_DELAY = 120
MIN_MOVE_DELAY = 40
SPEED_STEP = 6  # cuánto reduce el delay al comer

DATA_DIR = os.path.join("Data", "score")
HIGH_SCORE_FILE = os.path.join(DATA_DIR, "highscore.json")

# opciones del juego
WRAP_AROUND = False
USE_OBSTACLES = True
OBSTACLES = [(10,8), (11,8), (12,8), (15,12), (15,13)]  # coordenadas en celdas

# powerups
POWERUP_ENABLED = True
POWERUP_CHANCE = 0.12  # probabilidad de que aparezca un powerup cuando aparece comida
POWERUP_DURATION_MS = 7000

# colores
BG_COLOR = (10, 10, 10)
SNAKE_HEAD = (140, 255, 140)
SNAKE_BODY = (46, 139, 87)
FOOD_COLOR = (255, 80, 80)
POWERUP_COLORS = {
    "slow": (80, 160, 255),
    "speed": (255, 160, 80),
    "grow": (200, 120, 255),
    "score": (255, 230, 80)
}

FONT_NAME = None  # usa fuente por defecto
