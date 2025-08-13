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

# Directorio de datos
DATA_DIR = os.path.join("Data", "score")
HIGH_SCORE_FILE = os.path.join(DATA_DIR, "highscore.json")

# Directorio para perfiles
PROFILES_DIR = os.path.join("Data", "profiles")   # guarda perfiles en Data/profiles/<profile_name>/
DEFAULT_PROFILE = "default"
PROFILE_FILENAME = "profile.json"  # dentro de la carpeta del perfil

# opciones del juego
WRAP_AROUND = True
USE_OBSTACLES = False
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


# Animaciones
FOOD_PULSE_FREQ = 6.0        # Hz (veces por segundo de pulso)
FOOD_PULSE_AMPLITUDE = 0.18  # cuánto escala la comida (porcentaje)

HEAD_BOB_FREQ = 4.0          # Hz
HEAD_BOB_AMPL = 0.12         # escala de la cabeza por el 'bob'

BODY_SHIMMER_FREQ = 2.5      # Hz
BODY_SHIMMER_PHASE = 0.45    # desfase entre segmentos (en radianes)

PARTICLE_COUNT = 14
PARTICLE_SPEED = 0.9         # multiplicador
PARTICLE_LIFE_MS = 700       # ms de duración

# ===== Temas / Colores (centralizados) =====
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

# Configuración de efectos visuales
VISUAL_EFFECTS = {
    "enable_particles": True,
    "enable_screen_shake": True,
    "enable_flash_effects": True,
    "enable_smooth_movement": True,
    "enable_glow_effects": True,
    "enable_shadows": True,
    "particle_density": 1.0,  # Multiplicador para cantidad de partículas
    "animation_speed": 1.0,   # Multiplicador para velocidad de animaciones
    "glow_intensity": 0.8     # Intensidad de efectos de brillo (0.0 - 1.0)
}

# Colores específicos para el menú / UI (puedes editarlos aquí)
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

# Opcional: alias antiguos para compatibilidad (si algo del código usa WHITE/GRAY/DARK...)
WHITE = MENU_COLORS["text"]
GRAY = MENU_COLORS["muted"]
DARK = MENU_COLORS["bg"]
ACCENT = MENU_COLORS["accent"]
BAD = MENU_COLORS["bad"]
OK = MENU_COLORS["ok"]
OVERLAY = MENU_COLORS["overlay"]
