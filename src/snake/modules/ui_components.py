"""Componentes de UI reutilizables para el menú y otras pantallas."""
# pylint: disable=no-member

import random

import pygame

from ..system import settings
from ..system import utils


# --- Lógica de opciones avanzadas ---
def apply_all_settings(
    opt_wrap,
    opt_obs,
    opt_speed,
    opt_difficulty,
    opt_theme,
    opt_game_mode,
    opt_visual_effects,
    opt_particle_effects,
    opt_screen_shake,
    opt_smooth_movement,
    opt_show_grid,
    opt_glow_effects,
    opt_control_scheme,
    opt_allow_reverse,
    opt_powerup_enabled,
    opt_food_types,
    opt_multi_food,
    opt_sound_enabled,
    opt_music_enabled,
    opt_fullscreen,
    opt_show_fps,
):
    """Aplica todas las configuraciones del juego."""
    # settings ya está importado arriba
    settings.WRAP_AROUND = bool(opt_wrap)
    settings.USE_OBSTACLES = bool(opt_obs)
    settings.INIT_MOVE_DELAY = int(opt_speed)
    settings.DIFFICULTY = opt_difficulty
    settings.THEME = opt_theme
    settings.GAME_MODE = opt_game_mode
    settings.VISUAL_EFFECTS = bool(opt_visual_effects)
    settings.PARTICLE_EFFECTS = bool(opt_particle_effects)
    settings.SCREEN_SHAKE = bool(opt_screen_shake)
    settings.SMOOTH_MOVEMENT = bool(opt_smooth_movement)
    settings.SHOW_GRID = bool(opt_show_grid)
    settings.GLOW_EFFECTS = bool(opt_glow_effects)
    settings.CONTROL_SCHEME = opt_control_scheme
    settings.ALLOW_REVERSE = bool(opt_allow_reverse)
    settings.POWERUP_ENABLED = bool(opt_powerup_enabled)
    settings.FOOD_TYPES = bool(opt_food_types)
    settings.MULTI_FOOD = bool(opt_multi_food)
    settings.SOUND_ENABLED = bool(opt_sound_enabled)
    settings.MUSIC_ENABLED = bool(opt_music_enabled)
    settings.FULLSCREEN = bool(opt_fullscreen)
    settings.SHOW_FPS = bool(opt_show_fps)

    if opt_difficulty in settings.DIFFICULTY_SETTINGS:
        diff_config = settings.DIFFICULTY_SETTINGS[opt_difficulty]
        settings.INIT_MOVE_DELAY = diff_config["init_speed"]
        settings.MIN_MOVE_DELAY = diff_config["min_speed"]
        settings.SPEED_STEP = diff_config["speed_increase"]
        settings.POWERUP_CHANCE = diff_config["powerup_chance"]
        if bool(opt_obs) and diff_config["obstacle_count"] > 0:
            obstacles = []
            for _ in range(diff_config["obstacle_count"]):
                x = random.randint(5, settings.COLUMNS - 6)
                y = random.randint(5, settings.ROWS - 6)
                obstacles.append((x, y))
            settings.OBSTACLES = obstacles
        elif not bool(opt_obs):
            settings.OBSTACLES = []
    if opt_theme in settings.THEMES:
        settings.PALETTE.update(settings.THEMES[opt_theme])
    utils.log_info(
        f"Configuraciones aplicadas - Dificultad: {opt_difficulty}, Tema: {opt_theme}, Modo: {opt_game_mode}"
    )

WIDTH, HEIGHT = settings.WIDTH, settings.HEIGHT


# Colores centralizados desde settings
_menu_colors = settings.get_menu_colors()
WHITE = _menu_colors["text"]
GRAY = _menu_colors["muted"]
DARK = _menu_colors["bg"]
ACCENT = _menu_colors["accent"]
BAD = _menu_colors["bad"]
OK = _menu_colors["ok"]
OVERLAY = _menu_colors["overlay"]




def draw_text(surface, text, font, color, pos):
    """Dibuja texto en la superficie dada."""
    surf = font.render(text, True, color)
    surface.blit(surf, pos)
    return surf.get_rect(topleft=pos)

def center_rect(w, h, x_off=0, y_off=0):
    """Centrar un rectángulo en la pantalla."""
    return pygame.Rect((WIDTH - w) // 2 + x_off, (HEIGHT - h) // 2 + y_off, w, h)

class Button:
    """Un botón con fondo y texto centrado."""
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, surf, hover=False, selected=False):
        """Dibuja el botón con colores y efectos según estado."""
        panel_col = (30, 30, 40)
        border_col = (70, 70, 80)
        highlight_col = ACCENT if hover or selected else WHITE
        bg = panel_col
        pygame.draw.rect(surf, bg, self.rect)
        pygame.draw.rect(surf, border_col, self.rect, 2)
        text_surf = self.font.render(self.text, True, highlight_col)
        tx = self.rect.x + (self.rect.w - text_surf.get_width()) // 2
        ty = self.rect.y + (self.rect.h - text_surf.get_height()) // 2
        surf.blit(text_surf, (tx, ty))

    def is_hover(self, pos):
        """Verifica si el ratón está sobre el botón."""
        return self.rect.collidepoint(pos)

class InputOverlay:
    """Overlay para entrada de texto (crear perfiles, etc)."""
    def __init__(self, prompt="Introduce texto", menu_font=None, ui_font=None):
        self.prompt = prompt
        self.text = ""
        self.active = True
        self.result = None
        self.menu_font = menu_font
        self.ui_font = ui_font

    def handle_event(self, event):
        """Maneja eventos de entrada."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.result = self.text.strip()
                self.active = False
                return True
            elif event.key == pygame.K_ESCAPE:
                self.result = None
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return True
            else:
                ch = event.unicode
                if ch:
                    self.text += ch
                    return True
        return False

    def render(self, surf):
        """Dibuja el overlay de entrada."""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        surf.blit(overlay, (0, 0))
        box = center_rect(620, 160)
        pygame.draw.rect(surf, (24, 24, 32), box)
        pygame.draw.rect(surf, (100, 100, 110), box, 2)
        draw_text(surf, self.prompt, self.menu_font, WHITE, (box.x + 20, box.y + 16))
        draw_text(surf, self.text + "|", self.menu_font, ACCENT, (box.x + 20, box.y + 70))
        draw_text(surf, "Enter = confirmar   Esc = cancelar", self.ui_font, GRAY, (box.x + 20, box.y + 118))
