# menu.py -- Menú mejorado con efectos visuales avanzados
import pygame
import sys
import math
import time
import settings
import profiles
import utils
from game import Game, MOVE_EVENT
from visual_effects import VisualEffects

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
    WHITE = _menu_colors.get("text", (245,245,245))
    GRAY  = _menu_colors.get("muted", (160,160,160))
    DARK  = _menu_colors.get("bg", (18,22,30))
    ACCENT = _menu_colors.get("accent", (80,160,255))
    BAD   = _menu_colors.get("bad", (220,80,80))
    OK    = _menu_colors.get("ok", (120,200,120))
    OVERLAY = _menu_colors.get("overlay", (10,10,10,160))
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

# helpers
def draw_text(surface, text, font, color, pos):
    surf = font.render(text, True, color)
    surface.blit(surf, pos)
    return surf.get_rect(topleft=pos)

def center_blit(surface, surf_to_blit, center):
    r = surf_to_blit.get_rect(center=center)
    surface.blit(surf_to_blit, r.topleft)
    return r

def center_rect(w, h, x_off=0, y_off=0):
    return pygame.Rect((WIDTH - w) // 2 + x_off, (HEIGHT - h) // 2 + y_off, w, h)

class Button:
    def __init__(self, rect, text, font=MENU_FONT):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font

    def draw(self, surf, hover=False, selected=False):
        # Panel bg
        panel_col = (30, 30, 40)
        border_col = (70,70,80)
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
        surf.blit(overlay, (0,0))
        box = center_rect(620, 160)
        pygame.draw.rect(surf, (24,24,32), box)
        pygame.draw.rect(surf, (100,100,110), box, 2)
        draw_text(surf, self.prompt, MENU_FONT, WHITE, (box.x+20, box.y+16))
        draw_text(surf, self.text + "|", MENU_FONT, ACCENT, (box.x+20, box.y+70))
        draw_text(surf, "Enter = confirmar   Esc = cancelar", UI_FONT, GRAY, (box.x+20, box.y+118))


# ----- run() -----
def run():
    utils.log_info("Iniciando sistema de menús")
    utils.log_system_info(f"Resolución: {WIDTH}x{HEIGHT}")
    
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

    # options state (local)
    opt_wrap = getattr(settings, "WRAP_AROUND", False)
    opt_obs = getattr(settings, "USE_OBSTACLES", True)
    opt_speed = getattr(settings, "INIT_SPEED", None) or getattr(settings, "INIT_MOVE_DELAY", 120)

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
                consumed = input_overlay.handle_event(event)
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
                                play_profile_idx = min(play_profile_idx, max(0, len(profile_list)-1))
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
                        # apply options and start game
                        settings.WRAP_AROUND = bool(opt_wrap)
                        settings.USE_OBSTACLES = bool(opt_obs)
                        settings.INIT_MOVE_DELAY = int(opt_speed)
                        profile_list = profiles.list_profiles()
                        if not profile_list:
                            profiles.create_profile(settings.DEFAULT_PROFILE)
                            profile_list = profiles.list_profiles()
                        profile_name = profile_list[play_profile_idx]
                        utils.log_game_event("Iniciando nueva partida", f"Perfil: {profile_name}")
                        utils.log_info(f"Configuraciones - Wrap: {opt_wrap}, Obstáculos: {opt_obs}, Velocidad: {opt_speed}ms")
                        game = Game(SCREEN)
                        try:
                            game.logic.set_profile(profile_name)
                        except Exception:
                            try:
                                game.logic.profile_name = profile_name
                            except Exception:
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
                    elif event.key == pygame.K_w:
                        opt_wrap = not opt_wrap
                    elif event.key == pygame.K_o:
                        opt_obs = not opt_obs
                    elif event.key == pygame.K_LEFT:
                        opt_speed = min(400, opt_speed + 10)
                    elif event.key == pygame.K_RIGHT:
                        opt_speed = max(40, opt_speed - 10)
                    elif event.key == pygame.K_RETURN:
                        settings.WRAP_AROUND = bool(opt_wrap)
                        settings.USE_OBSTACLES = bool(opt_obs)
                        settings.INIT_MOVE_DELAY = int(opt_speed)
                        state = STATE_MAIN
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
                draw_text(SCREEN, f"Highscore: {profiles.load_profile(prof_name).get('highscore',0)}", UI_FONT, GRAY, (prof_box.x+20, prof_box.y+44))

                start_btn = Button(center_rect(220, 56, 0, 160), "INICIAR (Enter)", MENU_FONT)
                hover = start_btn.is_hover(mouse_pos)
                start_btn.draw(SCREEN, hover=hover)
                if mouse_clicked and hover:
                    # start game via click
                    settings.WRAP_AROUND = bool(opt_wrap)
                    settings.USE_OBSTACLES = bool(opt_obs)
                    settings.INIT_MOVE_DELAY = int(opt_speed)
                    profile_list = profiles.list_profiles()
                    if not profile_list:
                        profiles.create_profile(settings.DEFAULT_PROFILE)
                        profile_list = profiles.list_profiles()
                    profile_name = profile_list[play_profile_idx]
                    game = Game(SCREEN)
                    try:
                        game.logic.set_profile(profile_name)
                    except Exception:
                        try:
                            game.logic.profile_name = profile_name
                        except Exception:
                            pass
                    pygame.time.set_timer(MOVE_EVENT, game.logic.move_delay)
                    state = STATE_GAME

            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_PROFILES:
            draw_text(SCREEN, "PERFILES", TITLE_FONT, ACCENT, (40, 28))
            draw_text(SCREEN, "N = Nuevo   D = Borrar   Y = Confirmar borrado   Enter = Seleccionar", UI_FONT, GRAY, (40, 92))
            profile_list = profiles.list_profiles()
            box = center_rect(560, 320, 0, 20)
            pygame.draw.rect(SCREEN, (20,20,28), box)
            pygame.draw.rect(SCREEN, (80,80,90), box, 2)
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
                draw_text(SCREEN, prof_msg, UI_FONT, ACCENT, (box.x+16, box.y + box.h + 8))

            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

        elif state == STATE_OPTIONS:
            draw_text(SCREEN, "OPCIONES", TITLE_FONT, ACCENT, (40, 28))
            draw_text(SCREEN, "W = Toggle wrap   O = Toggle obstáculos   ← → = ajustar velocidad  Enter = Aplicar", UI_FONT, GRAY, (40, 92))
            draw_text(SCREEN, f"Wrap-around (W): {'ON' if opt_wrap else 'OFF'}", MENU_FONT, WHITE, (40, 150))
            draw_text(SCREEN, f"Obstáculos (O): {'ON' if opt_obs else 'OFF'}", MENU_FONT, WHITE, (40, 210))
            draw_text(SCREEN, f"Velocidad inicial (ms): {opt_speed}", MENU_FONT, WHITE, (40, 270))
            draw_text(SCREEN, "Esc: volver", UI_FONT, GRAY, (16, HEIGHT - 36))

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
