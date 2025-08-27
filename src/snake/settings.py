
"""
settings.py
-------------------
Módulo centralizado para la configuración del juego Snake.
Incluye helpers para obtener configuraciones dinámicas y permite override por variables de entorno.
"""

import os

# ===================
# --- RESOLUCIÓN Y GRID ---
# ===================
WIDTH = int(os.environ.get("SNAKE_WIDTH", 800))
HEIGHT = int(os.environ.get("SNAKE_HEIGHT", 600))
GRID_SIZE = int(os.environ.get("SNAKE_GRID_SIZE", 20))
COLUMNS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

# ===================
# --- MOVIMIENTO Y VELOCIDAD ---
# ===================
INIT_MOVE_DELAY = int(os.environ.get("SNAKE_INIT_MOVE_DELAY", 135))
MIN_MOVE_DELAY = int(os.environ.get("SNAKE_MIN_MOVE_DELAY", 35))
SPEED_STEP = int(os.environ.get("SNAKE_SPEED_STEP", 4))  # cuánto reduce el delay al comer

# ===================
# --- DIRECTORIOS Y ARCHIVOS ---
# ===================
DATA_DIR = os.path.join("Data")
AUDIO_DIR = os.path.join(DATA_DIR, "assets", "audio")
PROFILES_DIR = os.path.join(DATA_DIR, "profiles")
DEFAULT_PROFILE = "default"
PROFILE_FILENAME = "profile.json"  # dentro de la carpeta del perfil

# ===================
# --- OPCIONES GENERALES DEL JUEGO ---
# ===================
WINDOW_TITLE = os.environ.get("SNAKE_WINDOW_TITLE", "Snake Game - Fallback")
MENU_WINDOW_TITLE = os.environ.get("SNAKE_MENU_WINDOW_TITLE", "Snake Game")
WRAP_AROUND = os.environ.get("SNAKE_WRAP_AROUND", "True") == "True"
USE_OBSTACLES = os.environ.get("SNAKE_USE_OBSTACLES", "True") == "True"
OBSTACLE_COUNT = int(os.environ.get("SNAKE_OBSTACLE_COUNT", 12))
OBSTACLE_COLOR = (120, 120, 120)  # Color de los obstáculos (usar paleta o RGB)

# ===================
# --- POWERUPS ---
# ===================
POWERUP_ENABLED = os.environ.get("SNAKE_POWERUP_ENABLED", "True") == "True"
POWERUP_CHANCE = float(os.environ.get("SNAKE_POWERUP_CHANCE", 0.35))
POWERUP_DURATION_MS = int(os.environ.get("SNAKE_POWERUP_DURATION_MS", 5000))

# ===================
# --- MENÚ Y ESTADOS ---
# ===================
HELP_TEXT = "Usa flechas o ratón. Enter/Clic: elegir. M/ESC en juego: volver al menú"
STATE_MAIN = "main"
STATE_PLAY = "play"
STATE_PROFILES = "profiles"
STATE_OPTIONS = "options"
STATE_GAME = "game"
STATE_OPTIONS_GAMEPLAY = "options_gameplay"
STATE_OPTIONS_VISUAL = "options_visual"
STATE_OPTIONS_CONTROLS = "options_controls"
STATE_OPTIONS_ADVANCED = "options_advanced"

"""A module for managing game settings."""

# ===== OPCIONES MEJORADAS =====
# --- Dificultad ---
DIFFICULTY = os.environ.get("SNAKE_DIFFICULTY", "normal")  # "easy", "normal", "hard", "extreme"
DIFFICULTY_SETTINGS = {
    "easy": {
        "init_speed": 165,
        "min_speed": 95,
        "speed_increase": 4,
        "powerup_chance": 0.25,
        "obstacle_count": 0
    },
    "normal": {
        "init_speed": 135,
        "min_speed": 40,
        "speed_increase": 6,
        "powerup_chance": 0.18,
        "obstacle_count": 12
    },
    "hard": {
        "init_speed": 95,
        "min_speed": 30,
        "speed_increase": 8,
        "powerup_chance": 0.08,
        "obstacle_count": 16
    },
    "extreme": {
        "init_speed": 75,
        "min_speed": 5,
        "speed_increase": 10,
        "powerup_chance": 0.05,
        "obstacle_count": 20
    }
}

def get_difficulty_settings(level=None):
    """Devuelve la configuración de dificultad actual o de un nivel dado."""
    lvl = level or DIFFICULTY
    return DIFFICULTY_SETTINGS.get(lvl, DIFFICULTY_SETTINGS["normal"])

# --- Temas visuales ---
THEME = os.environ.get("SNAKE_THEME", "default")  # "default", "neon", "retro", "forest", "ocean"
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

def get_theme_colors(theme=None):
    """Devuelve el diccionario de colores del tema actual o de uno dado."""
    th = theme or THEME
    return THEMES.get(th, THEMES["default"])

# --- Sonido ---

# Audio y música habilitados por defecto
SOUND_ENABLED = os.environ.get("SNAKE_SOUND_ENABLED", "True") == "True"
MUSIC_ENABLED = os.environ.get("SNAKE_MUSIC_ENABLED", "True") == "True"
SOUND_VOLUME = float(os.environ.get("SNAKE_SOUND_VOLUME", 0.8))
MUSIC_VOLUME = float(os.environ.get("SNAKE_MUSIC_VOLUME", 0.6))

# Configuración centralizada de audio
AUDIO_CONFIG = {
    'sounds': {
        'food': './Data/assets/audio/food.ogg',
        'gameover': './Data/assets/audio/gameover.ogg',
        'powerup': './Data/assets/audio/powerup.ogg',
    },
    'music': {
        'music_game': './Data/assets/audio/music_game.ogg',
        'music_menu': './Data/assets/audio/music_menu.ogg',
    }
}

# --- Efectos visuales ---
VISUAL_EFFECTS = os.environ.get("SNAKE_VISUAL_EFFECTS", "True") == "True"
PARTICLE_EFFECTS = os.environ.get("SNAKE_PARTICLE_EFFECTS", "True") == "True"
SCREEN_SHAKE = os.environ.get("SNAKE_SCREEN_SHAKE", "True") == "True"
SMOOTH_MOVEMENT = os.environ.get("SNAKE_SMOOTH_MOVEMENT", "True") == "True"
SHOW_GRID = os.environ.get("SNAKE_SHOW_GRID", "True") == "True"
GLOW_EFFECTS = os.environ.get("SNAKE_GLOW_EFFECTS", "True") == "True"

# --- Modos de juego especiales ---
GAME_MODE = os.environ.get("SNAKE_GAME_MODE", "classic")  # "classic", "timed", "survival", "zen"
TIME_LIMIT = int(os.environ.get("SNAKE_TIME_LIMIT", 120))  # segundos para modo "timed"
SURVIVAL_SPAWN_RATE = float(os.environ.get("SNAKE_SURVIVAL_SPAWN_RATE", 0.05))
ZEN_NO_WALLS = os.environ.get("SNAKE_ZEN_NO_WALLS", "True") == "True"

# --- Serpiente ---
SNAKE_INITIAL_LENGTH = int(os.environ.get("SNAKE_INITIAL_LENGTH", 3))
SNAKE_GROWTH_RATE = int(os.environ.get("SNAKE_GROWTH_RATE", 1))  # segmentos que crece al comer
SNAKE_MAX_LENGTH = int(os.environ.get("SNAKE_MAX_LENGTH", 200))  # límite máximo de longitud

# --- Comida ---
FOOD_TYPES = os.environ.get("SNAKE_FOOD_TYPES",
                        "True") == "True"  # habilita diferentes tipos de comida
FOOD_SPECIAL_CHANCE = float(os.environ.get("SNAKE_FOOD_SPECIAL_CHANCE",
                                        0.15))  # probabilidad de comida especial
MULTI_FOOD = os.environ.get("SNAKE_MULTI_FOOD",
                        "False") == "True"  # múltiples piezas de comida a la vez
FOOD_COUNT = int(os.environ.get("SNAKE_FOOD_COUNT",
                                3))  # número de piezas de comida cuando MULTI_FOOD es True

# --- Controles ---
CONTROL_SCHEME = os.environ.get("SNAKE_CONTROL_SCHEME", "arrows")  # "arrows", "wasd", "both"
ALLOW_REVERSE = os.environ.get("SNAKE_ALLOW_REVERSE",
                            "False") == "True"  # permitir reversa inmediata

# --- Pantalla y UI ---
FULLSCREEN = os.environ.get("SNAKE_FULLSCREEN", "False") == "True"
FPS_LIMIT = int(os.environ.get("SNAKE_FPS_LIMIT", 60))
SHOW_FPS = os.environ.get("SNAKE_SHOW_FPS", "False") == "True"
SHOW_SCORE_HISTORY = os.environ.get("SNAKE_SHOW_SCORE_HISTORY", "True") == "True"
FONT = os.environ.get("SNAKE_FONT_NAME", "./Data/assets/font.ttf")

# ===== Paleta principal mejorada =====
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

# --- Colores específicos para el menú / UI ---
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

# --- Alias antiguos para compatibilidad (si algo del código usa WHITE/GRAY/DARK...) ---
WHITE = MENU_COLORS["text"]
GRAY = MENU_COLORS["muted"]
DARK = MENU_COLORS["bg"]
ACCENT = MENU_COLORS["accent"]
BAD = MENU_COLORS["bad"]
OK = MENU_COLORS["ok"]
OVERLAY = MENU_COLORS["overlay"]

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
    return {
        "text": (245, 245, 245),
        "muted": (150, 150, 150),
        "bg": (28, 32, 40),
        "accent": (80, 160, 255),
        "bad": (220, 80, 80),
        "ok": (120, 200, 120),
        "overlay": (10, 10, 10, 160),
    }

# ===================
# --- HELPERS GLOBALES ---
# ===================
def get_setting(key, default=None):
    """Permite obtener cualquier setting por clave, útil para acceso dinámico."""
    return globals().get(key, default)
