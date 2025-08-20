"""Configuraciones del juego"""
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

# Directorio de datos y assets
DATA_DIR = os.path.join("Data")
ASSETS_DIR = os.path.join("Data", "assets")

# Directorio para perfiles
PROFILES_DIR = os.path.join("Data", "profiles")
DEFAULT_PROFILE = "default"
PROFILE_FILENAME = "profile.json"  # dentro de la carpeta del perfil

# opciones del juego
# Nombre de la ventana principal (fallback directo)
WINDOW_TITLE = "Snake Game - Fallback"
# Nombre de la ventana del menú principal
MENU_WINDOW_TITLE = "Snake Game"
WRAP_AROUND = True
# Activar/desactivar obstáculos
USE_OBSTACLES = True
# Cantidad de obstáculos aleatorios
OBSTACLE_COUNT = 8
# Color de los obstáculos (usar paleta o RGB)
OBSTACLE_COLOR = (120, 120, 120)

# powerups
POWERUP_ENABLED = True
POWERUP_CHANCE = 0.12  # probabilidad de que aparezca un powerup cuando aparece comida
POWERUP_DURATION_MS = 5000

# --- Constantes y estados de menú ---
HELP_TEXT = "Usa flechas o ratón. Enter/Clic: elegir. M/ESC en juego: volver al menú"

# Estados del menú
STATE_MAIN = "main"
STATE_PLAY = "play"
STATE_PROFILES = "profiles"
STATE_OPTIONS = "options"
STATE_GAME = "game"
STATE_OPTIONS_GAMEPLAY = "options_gameplay"
STATE_OPTIONS_VISUAL = "options_visual"
STATE_OPTIONS_CONTROLS = "options_controls"
STATE_OPTIONS_ADVANCED = "options_advanced"
""""A module for managing game settings."""

# ===== NUEVAS OPCIONES MEJORADAS =====
# Modos de dificultad
DIFFICULTY = "normal"  # "easy", "normal", "hard", "extreme"
DIFFICULTY_SETTINGS = {
    "easy": {
        "init_speed": 160,
        "min_speed": 80,
        "speed_increase": 4,
        "powerup_chance": 0.20,
        "obstacle_count": 0
    },
    "normal": {
        "init_speed": 120,
        "min_speed": 40,
        "speed_increase": 6,
        "powerup_chance": 0.12,
        "obstacle_count": 5
    },
    "hard": {
        "init_speed": 90,
        "min_speed": 30,
        "speed_increase": 8,
        "powerup_chance": 0.08,
        "obstacle_count": 12
    },
    "extreme": {
        "init_speed": 60,
        "min_speed": 20,
        "speed_increase": 10,
        "powerup_chance": 0.05,
        "obstacle_count": 20
    }
}

# Temas visuales
THEME = "default"  # "default", "neon", "retro", "forest", "ocean"
THEMES = {
    "default": {
        "bg_top": (8, 12, 28),
        "bg_bottom": (18, 24, 48),
        "snake_head": (144, 238, 144),
        "snake_body_a": (46, 139, 87),
        "food": (255, 100, 90),
        "powerup": (80, 160, 255)
    },
    "neon": {
        "bg_top": (5, 0, 15),
        "bg_bottom": (15, 0, 30),
        "snake_head": (0, 255, 150),
        "snake_body_a": (0, 200, 100),
        "food": (255, 0, 150),
        "powerup": (150, 0, 255)
    },
    "retro": {
        "bg_top": (40, 30, 20),
        "bg_bottom": (60, 45, 30),
        "snake_head": (255, 215, 0),
        "snake_body_a": (218, 165, 32),
        "food": (255, 69, 0),
        "powerup": (255, 140, 0)
    },
    "forest": {
        "bg_top": (5, 20, 5),
        "bg_bottom": (15, 40, 15),
        "snake_head": (50, 205, 50),
        "snake_body_a": (34, 139, 34),
        "food": (255, 0, 0),
        "powerup": (255, 215, 0)
    },
    "ocean": {
        "bg_top": (0, 15, 30),
        "bg_bottom": (0, 30, 60),
        "snake_head": (0, 206, 209),
        "snake_body_a": (72, 61, 139),
        "food": (255, 127, 80),
        "powerup": (255, 255, 0)
    }
}

# Configuraciones de sonido (para futura implementación)
SOUND_ENABLED = False
MUSIC_ENABLED = False
SOUND_VOLUME = 0.7
MUSIC_VOLUME = 0.5

# Configuraciones de efectos visuales
VISUAL_EFFECTS = True
PARTICLE_EFFECTS = True
SCREEN_SHAKE = True
SMOOTH_MOVEMENT = True
SHOW_GRID = True
GLOW_EFFECTS = True

# Modos de juego especiales
GAME_MODE = "classic"  # "classic", "timed", "survival", "zen"
TIME_LIMIT = 120  # segundos para modo "timed"
SURVIVAL_SPAWN_RATE = 0.05  # probabilidad de spawn de obstáculos en modo survival
ZEN_NO_WALLS = True  # en modo zen, no hay paredes

# Configuraciones de la serpiente
SNAKE_INITIAL_LENGTH = 3
SNAKE_GROWTH_RATE = 1  # segmentos que crece al comer
SNAKE_MAX_LENGTH = 200  # límite máximo de longitud

# Configuraciones de comida
FOOD_TYPES = True  # habilita diferentes tipos de comida
FOOD_SPECIAL_CHANCE = 0.15  # probabilidad de comida especial
MULTI_FOOD = False  # múltiples piezas de comida a la vez
FOOD_COUNT = 1  # número de piezas de comida cuando MULTI_FOOD es True

# Configuraciones de control
CONTROL_SCHEME = "arrows"  # "arrows", "wasd", "both"
ALLOW_REVERSE = False  # permitir reversa inmediata

# Configuraciones de pantalla
FULLSCREEN = False
FPS_LIMIT = 60
SHOW_FPS = False
SHOW_SCORE_HISTORY = True

FONT_NAME = "Arial"  # Usa fuente por defecto

# ===== Temas / Colores =====
# Paleta principal mejorada
PALETTE = {
    "bg_top": (8, 12, 28),
    "bg_bottom": (18, 24, 48),
    "grid": (24, 28, 40),
    "snake_head": (144, 238, 144),
    "snake_body_a": (46, 139, 87),
    "snake_body_b": (34, 139, 34),
    "food": (255, 100, 90),
    "powerup": (80, 160, 255),
    "particle": (255, 200, 80),
    "shadow": (0, 0, 0, 80),
    "glow": (255, 255, 255, 40),
    "trail": (100, 255, 150, 60)
}

# Colores específicos para el menú / UI
MENU_COLORS = {
    "bg": (18, 22, 30),         # fondo del menú
    "panel": (30, 30, 40),      # fondo de botones/rectángulos
    "panel_border": (70, 70, 80), # borde de paneles
    "text": (245, 245, 245),    # texto principal
    "muted": (160, 160, 160),   # texto secundario
    "accent": (80, 160, 255),   # color acción / resaltado
    "bad": (220, 80, 80),       # color de error / alerta
    "ok": (120, 200, 120),      # color positivo
    "overlay": (10, 10, 10, 160), # overlay con alpha para modales (r,g,b,a)
}

# Alias antiguos para compatibilidad (si algo del código usa WHITE/GRAY/DARK...)
WHITE = MENU_COLORS["text"]
GRAY = MENU_COLORS["muted"]
DARK = MENU_COLORS["bg"]
ACCENT = MENU_COLORS["accent"]
BAD = MENU_COLORS["bad"]
OK = MENU_COLORS["ok"]
OVERLAY = MENU_COLORS["overlay"]

# --- Paleta de colores para menús y UI ---
def get_menu_colors():
    """Devuelve el diccionario de colores del menú, usando defaults si no está en settings."""
    _menu_colors = globals().get("MENU_COLORS", None)
    if _menu_colors:
        return {
            "text": _menu_colors.get("text", (245, 245, 245)),
            "muted": _menu_colors.get("muted", (160, 160, 160)),
            "bg": _menu_colors.get("bg", (18, 22, 30)),
            "accent": _menu_colors.get("accent", (80, 160, 255)),
            "bad": _menu_colors.get("bad", (220, 80, 80)),
            "ok": _menu_colors.get("ok", (120, 200, 120)),
            "overlay": _menu_colors.get("overlay", (10, 10, 10, 160)),
        }
    if not _menu_colors:
        return {
            "text": (245, 245, 245),
            "muted": (150, 150, 150),
            "bg": (28, 32, 40),
            "accent": (80, 160, 255),
            "bad": (220, 80, 80),
            "ok": (120, 200, 120),
            "overlay": (10, 10, 10, 160),
        }
    return None
