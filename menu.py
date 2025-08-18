# menu.py -- Menú mejorado con efectos visuales avanzados
# pylint: disable=no-member  # Desactivar warnings para atributos pygame dinámicos
import random
import sys

import pygame

import profiles
import settings
import utils
import video_config
from game import MOVE_EVENT, Game

video_config.configure_video_driver()
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = settings.WIDTH, settings.HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

TITLE_FONT = pygame.font.SysFont(None, 56)
MENU_FONT = pygame.font.SysFont(None, 34)
UI_FONT = pygame.font.SysFont(None, 20)

# colores desde settings (fallback si no están)
_menu_colors = getattr(settings, "MENU_COLORS", None)
if _menu_colors:
    WHITE = _menu_colors.get("text", (245, 245, 245))
    GRAY = _menu_colors.get("muted", (160, 160, 160))
    DARK = _menu_colors.get("bg", (18, 22, 30))
    ACCENT = _menu_colors.get("accent", (80, 160, 255))
    BAD = _menu_colors.get("bad", (220, 80, 80))
    OK = _menu_colors.get("ok", (120, 200, 120))
    OVERLAY = _menu_colors.get("overlay", (10, 10, 10, 160))
else:
    WHITE = (245, 245, 245)
    GRAY = (150, 150, 150)
    DARK = (28, 32, 40)
    ACCENT = (80, 160, 255)
    BAD = (220, 80, 80)
    OK = (120, 200, 120)
    OVERLAY = (10, 10, 10, 160)

HELP_TEXT = "Usa flechas o ratón. Enter/Clic: elegir. M/ESC en juego: volver al menú"

# Estados
STATE_MAIN = "main"
STATE_PLAY = "play"
STATE_PROFILES = "profiles"
STATE_OPTIONS = "options"
STATE_GAME = "game"
STATE_OPTIONS_GAMEPLAY = "options_gameplay"
STATE_OPTIONS_VISUAL = "options_visual"
STATE_OPTIONS_CONTROLS = "options_controls"
STATE_OPTIONS_ADVANCED = "options_advanced"

# helpers
def draw_text(surface, text, font, color, pos):
    surf = font.render(text, True, color)
    surface.blit(surf, pos)
    return surf.get_rect(topleft=pos)

def center_rect(w, h, x_off=0, y_off=0):
    return pygame.Rect((WIDTH - w) // 2 + x_off, (HEIGHT - h) // 2 + y_off, w, h)

class Button:

    """A fancy button with a background and centered text."""

    def __init__(self, rect, text, font=MENU_FONT):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, surf, hover=False, selected=False):
        # Panel bg
        panel_col = (30, 30, 40)
        border_col = (70, 70, 80)
        highlight_col = ACCENT if hover or selected else WHITE
        # Slightly darker when not hovered
        bg = panel_col
        pygame.draw.rect(surf, bg, self.rect)
        pygame.draw.rect(surf, border_col, self.rect, 2)
        # text
        text_surf = self.font.render(self.text, True, highlight_col)
        tx = self.rect.x + (self.rect.w - text_surf.get_width()) // 2
        ty = self.rect.y + (self.rect.h - text_surf.get_height()) // 2
        surf.blit(text_surf, (tx, ty))

    def is_hover(self, pos):
        return self.rect.collidepoint(pos)

class InputOverlay:

    """Overlay for text input, used for creating profiles or entering text."""

    def __init__(self, prompt="Introduce texto"):
        self.prompt = prompt
        self.text = ""
        self.active = True
        self.result = None

    def handle_event(self, event):
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
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        surf.blit(overlay, (0, 0))
        box = center_rect(620, 160)
        pygame.draw.rect(surf, (24, 24, 32), box)
        pygame.draw.rect(surf, (100, 100, 110), box, 2)
        draw_text(surf, self.prompt, MENU_FONT, WHITE, (box.x + 20, box.y + 16))
        draw_text(surf, self.text + "|", MENU_FONT, ACCENT, (box.x + 20, box.y + 70))
        draw_text(surf, "Enter = confirmar   Esc = cancelar", UI_FONT, GRAY, (box.x + 20, box.y + 118))


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
    """Aplicar todas las configuraciones al módulo settings"""
    # Configuraciones básicas
    settings.WRAP_AROUND = bool(opt_wrap)
    settings.USE_OBSTACLES = bool(opt_obs)
    settings.INIT_MOVE_DELAY = int(opt_speed)

    # Configuraciones avanzadas
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

    # Aplicar configuraciones de dificultad
    if opt_difficulty in settings.DIFFICULTY_SETTINGS:
        diff_config = settings.DIFFICULTY_SETTINGS[opt_difficulty]
        settings.INIT_MOVE_DELAY = diff_config["init_speed"]
        settings.MIN_MOVE_DELAY = diff_config["min_speed"]
        settings.SPEED_STEP = diff_config["speed_increase"]
        settings.POWERUP_CHANCE = diff_config["powerup_chance"]

        # Generar obstáculos automáticamente según la dificultad
        if bool(opt_obs) and diff_config["obstacle_count"] > 0:

            obstacles = []
            for _ in range(diff_config["obstacle_count"]):
                x = random.randint(5, settings.COLUMNS - 6)
                y = random.randint(5, settings.ROWS - 6)
                obstacles.append((x, y))
            settings.OBSTACLES = obstacles
        elif not bool(opt_obs):
            settings.OBSTACLES = []

    # Aplicar tema visual
    if opt_theme in settings.THEMES:
        settings.PALETTE.update(settings.THEMES[opt_theme])

    utils.log_info(
        f"Configuraciones aplicadas - Dificultad: {opt_difficulty}, Tema: {opt_theme}, Modo: {opt_game_mode}"
    )


# ----- run() -----
def run():
    """Iniciar el sistema de menús"""

    utils.log_info("Iniciando sistema de menús")

    # ensure default profile exists
    if not profiles.list_profiles():
        utils.log_info("Creando perfil por defecto")
        profiles.create_profile(settings.DEFAULT_PROFILE)

    state = STATE_MAIN
    selected_main = 0  # 0=Jugar,1=Perfiles,2=Opciones
    main_items = ["Jugar", "Perfiles", "Opciones"]

    # profiles state
    profile_list = profiles.list_profiles()
    prof_selected = 0
    prof_msg = ""
    prof_msg_until = 0

    # options state (local) - todas las opciones mejoradas
    opt_wrap = getattr(settings, "WRAP_AROUND", False)
    opt_obs = getattr(settings, "USE_OBSTACLES", True)
    opt_speed = getattr(settings, "INIT_SPEED", None) or getattr(settings, "INIT_MOVE_DELAY", 120)

    # Nuevas opciones avanzadas
    opt_difficulty = getattr(settings, "DIFFICULTY", "normal")
    opt_theme = getattr(settings, "THEME", "default")
    opt_game_mode = getattr(settings, "GAME_MODE", "classic")
    opt_visual_effects = getattr(settings, "VISUAL_EFFECTS", True)
    opt_particle_effects = getattr(settings, "PARTICLE_EFFECTS", True)
    opt_screen_shake = getattr(settings, "SCREEN_SHAKE", True)
    opt_smooth_movement = getattr(settings, "SMOOTH_MOVEMENT", True)
    opt_show_grid = getattr(settings, "SHOW_GRID", True)
    opt_glow_effects = getattr(settings, "GLOW_EFFECTS", True)
    opt_control_scheme = getattr(settings, "CONTROL_SCHEME", "arrows")
    opt_allow_reverse = getattr(settings, "ALLOW_REVERSE", False)
    opt_powerup_enabled = getattr(settings, "POWERUP_ENABLED", True)
    opt_food_types = getattr(settings, "FOOD_TYPES", True)
    opt_multi_food = getattr(settings, "MULTI_FOOD", False)
    opt_sound_enabled = getattr(settings, "SOUND_ENABLED", True)
    opt_music_enabled = getattr(settings, "MUSIC_ENABLED", True)
    opt_fullscreen = getattr(settings, "FULLSCREEN", False)
    opt_show_fps = getattr(settings, "SHOW_FPS", False)

    # Variables para navegación de opciones
    options_selected = 0
    options_category_items = [
        "Jugabilidad",
        "Visual",
        "Controles",
        "Avanzado",
        "← Volver",
    ]

    gameplay_selected = 0
    gameplay_items = [
        "Dificultad",
        "Modo de Juego",
        "Wrap-around",
        "Obstáculos",
        "Velocidad",
        "PowerUps",
        "Comida Especial",
        "← Volver",
    ]

    visual_selected = 0
    visual_items = [
        "Tema Visual",
        "Efectos Visuales",
        "Partículas",
        "Temblor Pantalla",
        "Movimiento Suave",
        "Mostrar Grid",
        "Efectos Brillo",
        "Pantalla Completa",
        "Mostrar FPS",
        "← Volver",
    ]

    controls_selected = 0
    controls_items = ["Esquema Control", "Permitir Reversa", "← Volver"]

    advanced_selected = 0
    advanced_items = ["Sonido", "Música", "Multi-Comida", "Resetear Todo", "← Volver"]

    # play state
    profile_list = profiles.list_profiles()
    if settings.DEFAULT_PROFILE in profile_list:
        play_profile_idx = profile_list.index(settings.DEFAULT_PROFILE)
    else:
        play_profile_idx = 0

    input_overlay = None
    game = None

    # build main buttons centered vertically with safe spacing
    btn_w, btn_h = 360, 70
    spacing = 20
    total_h = len(main_items) * btn_h + (len(main_items)-1) * spacing
    start_y = (HEIGHT - total_h) // 2  + 40  # slight shift down to make space for title/subtitle

    btns = []
    for i, label in enumerate(main_items):
        x = (WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + spacing)
        btns.append(Button((x, y, btn_w, btn_h), label))

    # main loop
    running = True
    while running:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.time.set_timer(MOVE_EVENT, 0)
                pygame.quit()
                sys.exit()

            # overlay input captures events first
            if input_overlay and input_overlay.active:
                input_overlay.handle_event(event)
                # when overlay finishes we will handle result below in context
                if not input_overlay.active:
                    res = input_overlay.result
                    # context-sensitive handling
                    if state == STATE_PROFILES:
                        if res:
                            safe = res.replace("/", "_").replace("\\", "_").strip()
                            if not safe:
                                prof_msg = "Nombre inválido"
                                prof_msg_until = now + 1800
                            elif profiles.profile_exists(safe):
                                prof_msg = "Perfil ya existe"
                                prof_msg_until = now + 1800
                            else:
                                profiles.create_profile(safe)
                                profile_list = profiles.list_profiles()
                                prof_selected = profile_list.index(safe) if safe in profile_list else 0
                                prof_msg = f"Perfil '{safe}' creado"
                                prof_msg_until = now + 2200
                        input_overlay = None
                continue

            # state-specific event handling
            if state == STATE_MAIN:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_main = (selected_main - 1) % len(main_items)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_main = (selected_main + 1) % len(main_items)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if selected_main == 0:
                            utils.log_user_action("Navegó a sección JUGAR")
                            state = STATE_PLAY
                            profile_list = profiles.list_profiles()
                            play_profile_idx = min(play_profile_idx, max(0, len(profile_list)-1))
                        elif selected_main == 1:
                            utils.log_user_action("Navegó a sección PERFILES")
                            state = STATE_PROFILES
                            profile_list = profiles.list_profiles()
                            prof_selected = min(prof_selected, max(0, len(profile_list)-1))
                        elif selected_main == 2:
                            utils.log_user_action("Navegó a sección OPCIONES")
                            state = STATE_OPTIONS
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True
                    for i, b in enumerate(btns):
                        if b.is_hover(mouse_pos):
                            selected_main = i
                            # trigger action
                            if i == 0:
                                state = STATE_PLAY
                                profile_list = profiles.list_profiles()
                                play_profile_idx = min(
                                    play_profile_idx, max(0, len(profile_list) - 1)
                                )
                            elif i == 1:
                                state = STATE_PROFILES
                                profile_list = profiles.list_profiles()
                                prof_selected = min(prof_selected, max(0, len(profile_list)-1))
                            elif i == 2:
                                state = STATE_OPTIONS

            elif state == STATE_PLAY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MAIN
                    elif event.key == pygame.K_LEFT:
                        play_profile_idx = max(0, play_profile_idx - 1)
                    elif event.key == pygame.K_RIGHT:
                        play_profile_idx = min(len(profile_list)-1, play_profile_idx + 1) if profile_list else 0
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        # apply all options and start game
                        apply_all_settings(
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
                        )
                        profile_list = profiles.list_profiles()
                        if not profile_list:
                            profiles.create_profile(settings.DEFAULT_PROFILE)
                            profile_list = profiles.list_profiles()
                        profile_name = profile_list[play_profile_idx]
                        utils.log_game_event("Iniciando nueva partida", f"Perfil: {profile_name}")
                        utils.log_info(
                            f"Configuraciones - Wrap: {opt_wrap},Obstáculos: {opt_obs}, Velocidad: {opt_speed}ms"
                        )
                        game = Game(SCREEN)
                        try:
                            game.logic.set_profile(profile_name)
                        except (AttributeError, OSError):
                            try:
                                game.logic.profile_name = profile_name
                            except AttributeError:
                                pass
                        pygame.time.set_timer(MOVE_EVENT, game.logic.move_delay)
                        state = STATE_GAME
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            elif state == STATE_PROFILES:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MAIN
                    elif event.key == pygame.K_UP:
                        prof_selected = max(0, prof_selected - 1)
                    elif event.key == pygame.K_DOWN:
                        prof_selected = min(max(0, len(profile_list)-1), prof_selected + 1)
                    elif event.key == pygame.K_n:
                        input_overlay = InputOverlay("Nuevo perfil - escribe nombre")
                    elif event.key == pygame.K_d:
                        if profile_list:
                            cur = profile_list[prof_selected]
                            if cur == settings.DEFAULT_PROFILE:
                                prof_msg = "No se puede borrar el perfil por defecto"
                                prof_msg_until = now + 1800
                            else:
                                prof_msg = f"Pulsa Y para borrar '{cur}'"
                                prof_msg_until = now + 5000
                    elif event.key == pygame.K_y:
                        if profile_list:
                            cur = profile_list[prof_selected]
                            if cur != settings.DEFAULT_PROFILE:
                                profiles.delete_profile(cur)
                                profile_list = profiles.list_profiles()
                                prof_selected = min(prof_selected, max(0, len(profile_list)-1))
                                prof_msg = f"Perfil '{cur}' borrado"
                                prof_msg_until = now + 1800
                            else:
                                prof_msg = "No se puede borrar el perfil por defecto"
                                prof_msg_until = now + 1800
                    elif event.key == pygame.K_RETURN:
                        # go to play with selected profile
                        state = STATE_PLAY
                        profile_list = profiles.list_profiles()
                        play_profile_idx = min(prof_selected, max(0, len(profile_list)-1))
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True
                    # compute click within list area will be handled in render section

            elif state == STATE_OPTIONS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_MAIN
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        options_selected = (options_selected - 1) % len(
                            options_category_items
                        )
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        options_selected = (options_selected + 1) % len(
                            options_category_items
                        )
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if options_selected == 0:
                            state = STATE_OPTIONS_GAMEPLAY
                        elif options_selected == 1:
                            state = STATE_OPTIONS_VISUAL
                        elif options_selected == 2:
                            state = STATE_OPTIONS_CONTROLS
                        elif options_selected == 3:
                            state = STATE_OPTIONS_ADVANCED
                        elif options_selected == 4:
                            state = STATE_MAIN
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            elif state == STATE_OPTIONS_GAMEPLAY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_OPTIONS
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        gameplay_selected = (gameplay_selected - 1) % len(
                            gameplay_items
                        )
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        gameplay_selected = (gameplay_selected + 1) % len(
                            gameplay_items
                        )
                    elif event.key in (
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                        pygame.K_RETURN,
                        pygame.K_SPACE,
                    ):
                        if gameplay_selected == 0:  # Dificultad
                            difficulties = list(settings.DIFFICULTY_SETTINGS.keys())
                            current_idx = (
                                difficulties.index(opt_difficulty)
                                if opt_difficulty in difficulties
                                else 0
                            )
                            if event.key == pygame.K_LEFT:
                                current_idx = (current_idx - 1) % len(difficulties)
                            elif event.key == pygame.K_RIGHT:
                                current_idx = (current_idx + 1) % len(difficulties)
                            opt_difficulty = difficulties[current_idx]
                            # Aplicar configuraciones de dificultad
                            diff_config = settings.DIFFICULTY_SETTINGS[opt_difficulty]
                            opt_speed = diff_config["init_speed"]
                            settings.POWERUP_CHANCE = diff_config["powerup_chance"]
                        elif gameplay_selected == 1:  # Modo de juego
                            modes = ["classic", "timed", "survival", "zen"]
                            current_idx = (
                                modes.index(opt_game_mode)
                                if opt_game_mode in modes
                                else 0
                            )
                            if event.key == pygame.K_LEFT:
                                current_idx = (current_idx - 1) % len(modes)
                            elif event.key == pygame.K_RIGHT:
                                current_idx = (current_idx + 1) % len(modes)
                            opt_game_mode = modes[current_idx]
                        elif gameplay_selected == 2:  # Wrap-around
                            opt_wrap = not opt_wrap
                        elif gameplay_selected == 3:  # Obstáculos
                            opt_obs = not opt_obs
                        elif gameplay_selected == 4:  # Velocidad
                            if event.key == pygame.K_LEFT:
                                opt_speed = min(400, opt_speed + 10)
                            elif event.key == pygame.K_RIGHT:
                                opt_speed = max(40, opt_speed - 10)
                        elif gameplay_selected == 5:  # PowerUps
                            opt_powerup_enabled = not opt_powerup_enabled
                        elif gameplay_selected == 6:  # Comida especial
                            opt_food_types = not opt_food_types
                        elif gameplay_selected == 7:  # Volver
                            state = STATE_OPTIONS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            elif state == STATE_OPTIONS_VISUAL:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_OPTIONS
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        visual_selected = (visual_selected - 1) % len(visual_items)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        visual_selected = (visual_selected + 1) % len(visual_items)
                    elif event.key in (
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                        pygame.K_RETURN,
                        pygame.K_SPACE,
                    ):
                        if visual_selected == 0:  # Tema visual
                            themes = list(settings.THEMES.keys())
                            current_idx = (
                                themes.index(opt_theme) if opt_theme in themes else 0
                            )
                            if event.key == pygame.K_LEFT:
                                current_idx = (current_idx - 1) % len(themes)
                            elif event.key == pygame.K_RIGHT:
                                current_idx = (current_idx + 1) % len(themes)
                            opt_theme = themes[current_idx]
                            # Aplicar tema inmediatamente
                            if opt_theme in settings.THEMES:
                                settings.PALETTE.update(settings.THEMES[opt_theme])
                        elif visual_selected == 1:  # Efectos visuales
                            opt_visual_effects = not opt_visual_effects
                        elif visual_selected == 2:  # Partículas
                            opt_particle_effects = not opt_particle_effects
                        elif visual_selected == 3:  # Temblor pantalla
                            opt_screen_shake = not opt_screen_shake
                        elif visual_selected == 4:  # Movimiento suave
                            opt_smooth_movement = not opt_smooth_movement
                        elif visual_selected == 5:  # Mostrar grid
                            opt_show_grid = not opt_show_grid
                        elif visual_selected == 6:  # Efectos brillo
                            opt_glow_effects = not opt_glow_effects
                        elif visual_selected == 7:  # Pantalla completa
                            opt_fullscreen = not opt_fullscreen
                            # Aplicar cambio de pantalla completa inmediatamente
                            #if opt_fullscreen:
                            #    SCREEN = pygame.display.set_mode(
                            #        (WIDTH, HEIGHT), pygame.FULLSCREEN
                            #    )
                            #else:
                            #    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
                        elif visual_selected == 8:  # Mostrar FPS
                            opt_show_fps = not opt_show_fps
                        elif visual_selected == 9:  # Volver
                            state = STATE_OPTIONS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            elif state == STATE_OPTIONS_CONTROLS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_OPTIONS
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        controls_selected = (controls_selected - 1) % len(
                            controls_items
                        )
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        controls_selected = (controls_selected + 1) % len(
                            controls_items
                        )
                    elif event.key in (
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                        pygame.K_RETURN,
                        pygame.K_SPACE,
                    ):
                        if controls_selected == 0:  # Esquema de control
                            schemes = ["arrows", "wasd", "both"]
                            current_idx = (
                                schemes.index(opt_control_scheme)
                                if opt_control_scheme in schemes
                                else 0
                            )
                            if event.key == pygame.K_LEFT:
                                current_idx = (current_idx - 1) % len(schemes)
                            elif event.key == pygame.K_RIGHT:
                                current_idx = (current_idx + 1) % len(schemes)
                            opt_control_scheme = schemes[current_idx]
                        elif controls_selected == 1:  # Permitir reversa
                            opt_allow_reverse = not opt_allow_reverse
                        elif controls_selected == 2:  # Volver
                            state = STATE_OPTIONS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            elif state == STATE_OPTIONS_ADVANCED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = STATE_OPTIONS
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        advanced_selected = (advanced_selected - 1) % len(
                            advanced_items
                        )
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        advanced_selected = (advanced_selected + 1) % len(
                            advanced_items
                        )
                    elif event.key in (
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                        pygame.K_RETURN,
                        pygame.K_SPACE,
                    ):
                        if advanced_selected == 0:  # Sonido
                            opt_sound_enabled = not opt_sound_enabled
                        elif advanced_selected == 1:  # Música
                            opt_music_enabled = not opt_music_enabled
                        elif advanced_selected == 2:  # Multi-comida
                            opt_multi_food = not opt_multi_food
                        elif advanced_selected == 3:  # Resetear todo
                            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                                # Resetear todas las configuraciones a valores por defecto
                                opt_wrap = True
                                opt_obs = False
                                opt_speed = 120
                                opt_difficulty = "normal"
                                opt_theme = "default"
                                opt_game_mode = "classic"
                                opt_visual_effects = True
                                opt_particle_effects = True
                                opt_screen_shake = True
                                opt_smooth_movement = True
                                opt_show_grid = True
                                opt_glow_effects = True
                                opt_control_scheme = "arrows"
                                opt_allow_reverse = False
                                opt_powerup_enabled = True
                                opt_food_types = True
                                opt_multi_food = False
                                opt_sound_enabled = True
                                opt_music_enabled = True
                                opt_fullscreen = False
                                opt_show_fps = False
                                # Aplicar configuraciones al settings
                                settings.PALETTE = {
                                    "bg_top": (8, 12, 28),
                                    "bg_bottom": (18, 24, 48),
                                    "snake_head": (144, 238, 144),
                                    "snake_body_a": (46, 139, 87),
                                    "food": (255, 100, 90),
                                    "powerup": (80, 160, 255),
                                }
                                # No necesitamos redefinir SCREEN aquí
                        elif advanced_selected == 4:  # Volver
                            state = STATE_OPTIONS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            elif state == STATE_GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_m, pygame.K_ESCAPE):
                        pygame.time.set_timer(MOVE_EVENT, 0)
                        game = None
                        state = STATE_MAIN
                        profile_list = profiles.list_profiles()
                        prof_selected = 0
                        continue
                    elif event.key == pygame.K_r:
                        if game:
                            game.reset_all()
                    elif event.key == pygame.K_SPACE:
                        if game:
                            game.logic.toggle_pause()
                if event.type == MOVE_EVENT and game:
                    game.handle_move()

        # ---------- Drawing ----------
        SCREEN.fill(DARK)

        if state == STATE_MAIN:
            # Title centered
            title_surf = TITLE_FONT.render("SNAKE", True, ACCENT)
            subtitle_surf = UI_FONT.render("Selecciona una opción", True, WHITE)
            # center them horizontally and position above buttons
            title_center = (WIDTH // 2, start_y - 80)
            subtitle_center = (WIDTH // 2, start_y - 40)
            SCREEN.blit(title_surf, title_surf.get_rect(center=title_center))
            SCREEN.blit(subtitle_surf, subtitle_surf.get_rect(center=subtitle_center))

            # draw buttons
            for i, b in enumerate(btns):
                hover = b.is_hover(mouse_pos)
                selected = (i == selected_main)
                b.draw(SCREEN, hover=hover, selected=selected)

            # help text below buttons (guaranteed not to overlap)
            help_surf = UI_FONT.render(HELP_TEXT, True, GRAY)
            help_pos = (WIDTH//2 - help_surf.get_width()//2, start_y + total_h + 18)
            SCREEN.blit(help_surf, help_pos)

            draw_text(SCREEN, "Q: salir", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_PLAY:
            draw_text(SCREEN, "JUGAR", TITLE_FONT, ACCENT, (40, 28))
            draw_text(SCREEN, "Perfil seleccionado (← → para cambiar)", UI_FONT, WHITE, (40, 100))
            profile_list = profiles.list_profiles()
            if not profile_list:
                draw_text(SCREEN, "No hay perfiles. Crea uno en Perfiles.", UI_FONT, BAD, (40, 160))
            else:
                prof_name = profile_list[play_profile_idx]
                prof_box = center_rect(520, 72, 0, -20)
                pygame.draw.rect(SCREEN, (20,20,28), prof_box)
                pygame.draw.rect(SCREEN, (80,80,90), prof_box, 2)
                draw_text(SCREEN, prof_name, MENU_FONT, WHITE, (prof_box.x+20, prof_box.y+12))
                draw_text(
                    SCREEN,
                    f"Highscore:{profiles.load_profile(prof_name).get('highscore',0)}",
                    UI_FONT,
                    GRAY,
                    (prof_box.x + 20, prof_box.y + 44),
                )

                start_btn = Button(center_rect(220, 56, 0, 160), "INICIAR (Enter)", MENU_FONT)
                hover = start_btn.is_hover(mouse_pos)
                start_btn.draw(SCREEN, hover=hover)
                if mouse_clicked and hover:
                    # start game via click - apply all options
                    apply_all_settings(
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
                    )
                    profile_list = profiles.list_profiles()
                    if not profile_list:
                        profiles.create_profile(settings.DEFAULT_PROFILE)
                        profile_list = profiles.list_profiles()
                    profile_name = profile_list[play_profile_idx]
                    game = Game(SCREEN)
                    try:
                        game.logic.set_profile(profile_name)
                    except (AttributeError, OSError):
                        try:
                            game.logic.profile_name = profile_name
                        except AttributeError:
                            pass
                    pygame.time.set_timer(MOVE_EVENT, game.logic.move_delay)
                    state = STATE_GAME

            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_PROFILES:
            draw_text(SCREEN, "PERFILES", TITLE_FONT, ACCENT, (40, 28))
            draw_text(
                SCREEN,
                "N = Nuevo   "
                "D = Borrar   "
                "Y = Confirmar borrado   "
                "Enter = Seleccionar",
                UI_FONT,
                GRAY,
                (40, 92),
            )
            profile_list = profiles.list_profiles()
            box = center_rect(560, 320, 0, 20)
            pygame.draw.rect(SCREEN, (20, 20, 28), box)
            pygame.draw.rect(SCREEN, (80, 80, 90), box, 2)
            y = box.y + 16
            for idx, name in enumerate(profile_list):
                color = WHITE if idx == prof_selected else GRAY
                prefix = "▶ " if idx == prof_selected else "   "
                draw_text(SCREEN, prefix + name, UI_FONT, color, (box.x+16, y))
                y += 34

            if mouse_clicked and profile_list:
                mx, my = mouse_pos
                if box.collidepoint(mx,my):
                    rel_y = my - (box.y + 16)
                    idx = rel_y // 34
                    if 0 <= idx < len(profile_list):
                        prof_selected = idx

            if input_overlay:
                input_overlay.render(SCREEN)

            if prof_msg and now < prof_msg_until:
                draw_text(
                    SCREEN, prof_msg, UI_FONT, ACCENT, (box.x + 16, box.y + box.h + 8)
                )

            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_OPTIONS:
            draw_text(SCREEN, "OPCIONES - CATEGORÍAS", TITLE_FONT, ACCENT, (40, 28))
            draw_text(
                SCREEN,
                "Selecciona una categoría de opciones:",
                UI_FONT,
                WHITE,
                (40, 90),
            )

            y_start = 140
            for i, item in enumerate(options_category_items):
                color = ACCENT if i == options_selected else WHITE
                prefix = "▶ " if i == options_selected else "  "
                draw_text(
                    SCREEN, prefix + item, MENU_FONT, color, (60, y_start + i * 40)
                )

            draw_text(
                SCREEN,
                "↑↓ navegar  " \
                "Enter: seleccionar  " \
                "Esc: volver",
                UI_FONT,
                GRAY,
                (40, y_start + len(options_category_items) * 40 + 20),
            )
            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_OPTIONS_GAMEPLAY:
            draw_text(SCREEN, "OPCIONES - JUGABILIDAD", TITLE_FONT, ACCENT, (40, 28))
            draw_text(
                SCREEN, "Configura las opciones de gameplay:", UI_FONT, WHITE, (40, 90)
            )

            y_start = 130
            options_values = [
                f"Dificultad: {opt_difficulty.upper()}",
                f"Modo: {opt_game_mode.upper()}",
                f"Wrap-around: {'ON' if opt_wrap else 'OFF'}",
                f"Obstáculos: {'ON' if opt_obs else 'OFF'}",
                f"Velocidad: {opt_speed}ms",
                f"PowerUps: {'ON' if opt_powerup_enabled else 'OFF'}",
                f"Comida Especial: {'ON' if opt_food_types else 'OFF'}",
                "← Volver",
            ]

            for i, (item, value) in enumerate(zip(gameplay_items, options_values)):
                color = ACCENT if i == gameplay_selected else WHITE
                prefix = "▶ " if i == gameplay_selected else "  "
                draw_text(
                    SCREEN, prefix + value, MENU_FONT, color, (60, y_start + i * 32)
                )

            draw_text(
                SCREEN,
                "↑↓ navegar  " \
                "←→ cambiar  Enter/Space: toggle  " \
                "Esc: volver",
                UI_FONT,
                GRAY,
                (40, y_start + len(gameplay_items) * 32 + 20),
            )
            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_OPTIONS_VISUAL:
            draw_text(SCREEN, "OPCIONES - VISUALES", TITLE_FONT, ACCENT, (40, 28))
            draw_text(
                SCREEN, "Configura los efectos visuales:", UI_FONT, WHITE, (40, 90)
            )

            y_start = 130
            visual_values = [
                f"Tema: {opt_theme.upper()}",
                f"Efectos Visuales: {'ON' if opt_visual_effects else 'OFF'}",
                f"Partículas: {'ON' if opt_particle_effects else 'OFF'}",
                f"Temblor Pantalla: {'ON' if opt_screen_shake else 'OFF'}",
                f"Movimiento Suave: {'ON' if opt_smooth_movement else 'OFF'}",
                f"Mostrar Grid: {'ON' if opt_show_grid else 'OFF'}",
                f"Efectos Brillo: {'ON' if opt_glow_effects else 'OFF'}",
                f"Pantalla Completa: {'ON' if opt_fullscreen else 'OFF'}",
                f"Mostrar FPS: {'ON' if opt_show_fps else 'OFF'}",
                "← Volver",
            ]

            for i, (item, value) in enumerate(zip(visual_items, visual_values)):
                color = ACCENT if i == visual_selected else WHITE
                prefix = "▶ " if i == visual_selected else "  "
                draw_text(
                    SCREEN, prefix + value, MENU_FONT, color, (60, y_start + i * 28)
                )

            draw_text(
                SCREEN,
                "↑↓ navegar  ←→ cambiar  Enter/Space: toggle  Esc: volver",
                UI_FONT,
                GRAY,
                (40, y_start + len(visual_items) * 28 + 20),
            )
            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_OPTIONS_CONTROLS:
            draw_text(SCREEN, "OPCIONES - CONTROLES", TITLE_FONT, ACCENT, (40, 28))
            draw_text(
                SCREEN, "Configura los controles del juego:", UI_FONT, WHITE, (40, 90)
            )

            y_start = 140
            controls_values = [
                f"Esquema: {opt_control_scheme.upper()}",
                f"Reversa Inmediata: {'ON' if opt_allow_reverse else 'OFF'}",
                "← Volver",
            ]

            for i, (item, value) in enumerate(zip(controls_items, controls_values)):
                color = ACCENT if i == controls_selected else WHITE
                prefix = "▶ " if i == controls_selected else "  "
                draw_text(
                    SCREEN, prefix + value, MENU_FONT, color, (60, y_start + i * 40)
                )

            # Mostrar descripción del esquema seleccionado
            y_desc = y_start + len(controls_items) * 40 + 20
            if opt_control_scheme == "arrows":
                draw_text(
                    SCREEN, "Solo flechas del teclado", UI_FONT, GRAY, (60, y_desc)
                )
            elif opt_control_scheme == "wasd":
                draw_text(SCREEN, "Solo teclas WASD", UI_FONT, GRAY, (60, y_desc))
            elif opt_control_scheme == "both":
                draw_text(
                    SCREEN, "Flechas y WASD funcionan", UI_FONT, GRAY, (60, y_desc)
                )

            draw_text(
                SCREEN,
                "↑↓ navegar  " \
                "←→ cambiar  " \
                "Enter/Space: toggle  " \
                "Esc: volver",
                UI_FONT,
                GRAY,
                (40, y_desc + 30),
            )
            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_OPTIONS_ADVANCED:
            draw_text(SCREEN, "OPCIONES - AVANZADAS", TITLE_FONT, ACCENT, (40, 28))
            draw_text(SCREEN, "Configuraciones avanzadas:", UI_FONT, WHITE, (40, 90))

            y_start = 140
            advanced_values = [
                f"Sonido: {'ON' if opt_sound_enabled else 'OFF'}",
                f"Música: {'ON' if opt_music_enabled else 'OFF'}",
                f"Multi-Comida: {'ON' if opt_multi_food else 'OFF'}",
                "RESETEAR TODO",
                "← Volver",
            ]

            for i, (item, value) in enumerate(zip(advanced_items, advanced_values)):
                if i == 3:  # Resetear todo en rojo
                    color = BAD if i == advanced_selected else GRAY
                else:
                    color = ACCENT if i == advanced_selected else WHITE
                prefix = "▶ " if i == advanced_selected else "  "
                draw_text(
                    SCREEN, prefix + value, MENU_FONT, color, (60, y_start + i * 40)
                )

            if advanced_selected == 3:
                draw_text(
                    SCREEN,
                    "¡ADVERTENCIA! Esto restaurará TODAS las configuraciones",
                    UI_FONT,
                    BAD,
                    (60, y_start + len(advanced_items) * 40 + 10),
                )
                draw_text(
                    SCREEN,
                    "a los valores por defecto. Presiona Enter para confirmar.",
                    UI_FONT,
                    BAD,
                    (60, y_start + len(advanced_items) * 40 + 30),
                )

            draw_text(
                SCREEN,
                "↑↓ navegar  " \
                "Enter/Space: toggle/ejecutar  " \
                "Esc: volver",
                UI_FONT,
                GRAY,
                (40, y_start + len(advanced_items) * 40 + 60),
            )
            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        # Controles del juego
        elif state == STATE_GAME and game:
            # continuous key holds
            keys = pygame.key.get_pressed()
            if not game.logic.game_over:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    game.logic.set_direction((0, -1))
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    game.logic.set_direction((0, 1))
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    game.logic.set_direction((-1, 0))
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    game.logic.set_direction((1, 0))

            # update & render game
            game.update()
            game.render()

        # overlay if needed
        if input_overlay and input_overlay.active and state != STATE_PROFILES:
            input_overlay.render(SCREEN)

        pygame.display.flip()
        CLOCK.tick(60)
