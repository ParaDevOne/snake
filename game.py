# game.py (renderer mejorado para pygame con efectos visuales avanzados)
import math
import time
import random
import pygame
import settings
from logic import GameLogic
from visual_effects import VisualEffects

MOVE_EVENT = pygame.USEREVENT + 1  # pylint: disable=no-member

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(settings.FONT_NAME, 20)
        self.bigfont = pygame.font.Font(settings.FONT_NAME, 48)
        self.title_font = pygame.font.Font(settings.FONT_NAME, 32)
        self.logic = GameLogic(load_highscore=True)

        # Efectos visuales
        self.visual_effects = VisualEffects()

        # Variables para animaciones suaves
        self.interpolation_progress = 0.0
        self.last_move_time = time.time()
        self.powerup_rotation = 0.0

        # Eventos pendientes para efectos
        self.pending_food_explosion = False
        self.pending_powerup_explosion = None
        self.pending_game_over_shake = False

        # start timer with current delay
        pygame.time.set_timer(MOVE_EVENT, self.logic.move_delay)

    def reset_all(self):
        self.logic.reset()
        self.visual_effects = VisualEffects()  # Reset efectos
        self.interpolation_progress = 0.0
        self.pending_food_explosion = False
        self.pending_powerup_explosion = None
        self.pending_game_over_shake = False
        pygame.time.set_timer(MOVE_EVENT, self.logic.move_delay)

    def handle_move(self):
        events = self.logic.handle_move()

        # Manejar efectos basados en eventos
        if events.get('ate_food'):
            self.pending_food_explosion = True

        if events.get('picked_powerup'):
            self.pending_powerup_explosion = events['picked_powerup']

        if events['status'] in ('wall', 'self', 'obstacle'):
            self.pending_game_over_shake = True

        # Reset interpolation para movimiento suave
        self.interpolation_progress = 0.0
        self.last_move_time = time.time()

        # if move_delay changed, update timer
        pygame.time.set_timer(MOVE_EVENT, self.logic.move_delay)
        return events

    def update(self):
        self.logic.update()
        self.visual_effects.update()

        # Actualizar interpolación para movimiento suave
        if not self.logic.game_over and not self.logic.paused:
            elapsed = (time.time() - self.last_move_time) * 1000  # ms
            self.interpolation_progress = min(1.0, elapsed / self.logic.move_delay)

        # Rotar powerups
        self.powerup_rotation += 0.05
        if self.powerup_rotation > 2 * math.pi:
            self.powerup_rotation -= 2 * math.pi

        # Procesar efectos pendientes
        if self.pending_food_explosion:
            state = self.logic.get_state()
            if state['food']:
                self.visual_effects.particle_system.add_explosion(
                    state['food'], (255, 150, 100), count=20, speed_range=(3, 8)
                )
                self.visual_effects.add_flash((255, 200, 100), 50)
            self.pending_food_explosion = False

        if self.pending_powerup_explosion:
            state = self.logic.get_state()
            colors = {
                'slow': (100, 150, 255),
                'speed': (255, 180, 100),
                'grow': (200, 150, 255),
                'score': (255, 220, 100)
            }
            color = colors.get(self.pending_powerup_explosion, (200, 200, 200))

            # Encontrar posición de la cabeza para el efecto
            if state['snake']:
                head_pos = state['snake'][0]
                self.visual_effects.particle_system.add_explosion(
                    head_pos, color, count=25, speed_range=(4, 10)
                )
                self.visual_effects.add_flash(color, 70)

            self.pending_powerup_explosion = None

        if self.pending_game_over_shake:
            self.visual_effects.add_screen_shake(15)
            self.visual_effects.add_flash((255, 50, 50), 120)
            self.pending_game_over_shake = False

    def draw_enhanced_background(self):
        """Dibuja un fondo mejorado con gradiente"""
        # Gradiente de fondo
        bg_top = getattr(settings, 'PALETTE', {}).get('bg_top', (8, 12, 28))
        bg_bottom = getattr(settings, 'PALETTE', {}).get('bg_bottom', (18, 24, 48))

        self.visual_effects.draw_gradient_rect(
            self.screen,
            (0, 0, settings.WIDTH, settings.HEIGHT),
            bg_top, bg_bottom, vertical=True
        )

        # Líneas de grid sutiles
        grid_color = getattr(settings, 'PALETTE', {}).get('grid', (24, 28, 40))
        for x in range(0, settings.WIDTH, settings.GRID_SIZE):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, settings.HEIGHT))
        for y in range(0, settings.HEIGHT, settings.GRID_SIZE):
            pygame.draw.line(self.screen, grid_color, (0, y), (settings.WIDTH, y))

    def draw_enhanced_obstacles(self, obstacles):
        """Dibuja obstáculos mejorados"""
        for ox, oy in obstacles:
            x = ox * settings.GRID_SIZE
            y = oy * settings.GRID_SIZE
            size = settings.GRID_SIZE

            # Sombra
            shadow_rect = pygame.Rect(x + 2, y + 2, size, size)
            pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect)

            # Obstáculo con gradiente
            obstacle_rect = pygame.Rect(x, y, size, size)
            self.visual_effects.draw_gradient_rect(
                self.screen, obstacle_rect,
                (140, 140, 150), (80, 80, 90)
            )

            # Borde
            pygame.draw.rect(self.screen, (160, 160, 170), obstacle_rect, 2)

    def render(self):
        state = self.logic.get_state()

        # Obtener offset para screen shake
        shake_offset = self.visual_effects.get_screen_offset()

        # Crear superficie temporal para el shake effect
        if shake_offset != (0, 0):
            temp_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))
            render_surface = temp_surface
        else:
            render_surface = self.screen

        # Fondo mejorado
        self.draw_enhanced_background()

        # Obstáculos mejorados
        if settings.USE_OBSTACLES:
            self.draw_enhanced_obstacles(state["obstacles"])

        # Comida con animación pulsante
        if state["food"]:
            pulse_scale = self.visual_effects.animation_manager.pulse_scale(3.0, 0.15, 1.0)
            self.visual_effects.draw_enhanced_food(render_surface, state["food"], pulse_scale)

            # Añadir efecto de rastro ocasional
            if random.random() < 0.1:
                self.visual_effects.particle_system.add_trail_effect(
                    state["food"], (255, 200, 100), count=3
                )

        # Powerup con rotación y efectos
        if state["powerup"]:
            ptype, ppos = state["powerup"]
            self.visual_effects.draw_enhanced_powerup(
                render_surface, ppos, ptype, self.powerup_rotation
            )

        # Serpiente con interpolación suave y efectos
        snake_segments = state["snake"]
        prev_snake = state.get("prev_snake", snake_segments)

        for i, seg in enumerate(snake_segments):
            is_head = (i == 0)

            # Interpolación suave del movimiento (con corrección para wrap-around)
            if i < len(prev_snake) and not self.logic.game_over:
                prev_pos = prev_snake[i]
                current_pos = seg

                # Detectar si hubo wrap-around y ajustar la interpolación
                if settings.WRAP_AROUND:
                    dx = abs(current_pos[0] - prev_pos[0])
                    dy = abs(current_pos[1] - prev_pos[1])

                    # Si la distancia es muy grande, probablemente hubo wrap
                    if dx > settings.COLUMNS / 2 or dy > settings.ROWS / 2:
                        # No interpolar cuando hay wrap-around
                        interpolated_pos = current_pos
                    else:
                        interpolated_pos = self.visual_effects.animation_manager.smooth_interpolate(
                            prev_pos, current_pos, self.interpolation_progress
                        )
                else:
                    interpolated_pos = self.visual_effects.animation_manager.smooth_interpolate(
                        prev_pos, current_pos, self.interpolation_progress
                    )
            else:
                interpolated_pos = seg

            # Escala animada para la cabeza
            if is_head:
                head_scale = self.visual_effects.animation_manager.pulse_scale(4.0, 0.08, 1.0)
                direction = self.logic.snake.direction
            else:
                head_scale = 1.0
                direction = None

            # Dibujar segmento mejorado
            self.visual_effects.draw_enhanced_snake_segment(
                render_surface, interpolated_pos, is_head, direction, head_scale
            )

            # Añadir efecto de rastro ocasional para la cabeza
            if is_head and not self.logic.game_over and random.random() < 0.05:
                trail_color = (144, 238, 144) if is_head else (46, 139, 87)
                self.visual_effects.particle_system.add_trail_effect(
                    interpolated_pos, trail_color, count=2
                )

        # Renderizar partículas
        self.visual_effects.particle_system.render(render_surface)

        # HUD mejorado con sombras
        hud_texts = [
            f"Puntos: {state['score']}",
            f"Mejor: {state['highscore']}",
            f"Velocidad: {state['move_delay']}ms"
        ]

        if state['paused']:
            hud_texts.append("[PAUSADO]")
        if state['active_power']:
            hud_texts.append(f"Power: {state['active_power'].upper()}")

        hud = "  |  ".join(hud_texts)

        # Sombra del texto
        shadow_text = self.font.render(hud, True, (0, 0, 0))
        render_surface.blit(shadow_text, (10, 10))

        # Texto principal
        main_text = self.font.render(hud, True, (240, 240, 240))
        render_surface.blit(main_text, (8, 8))

        # Game Over mejorado
        if state['game_over']:
            # Overlay semi-transparente
            overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)  # pylint: disable=no-member
            overlay.fill((0, 0, 0, 150))
            render_surface.blit(overlay, (0, 0))

            # Game Over con efectos
            go_text = "GAME OVER"
            shadow_go = self.bigfont.render(go_text, True, (0, 0, 0))
            main_go = self.bigfont.render(go_text, True, (255, 100, 100))

            center_x = settings.WIDTH // 2
            center_y = settings.HEIGHT // 2

            # Sombra
            shadow_rect = shadow_go.get_rect(center=(center_x + 3, center_y - 37))
            render_surface.blit(shadow_go, shadow_rect)

            # Texto principal
            main_rect = main_go.get_rect(center=(center_x, center_y - 40))
            render_surface.blit(main_go, main_rect)

            # Subtítulo
            sub_text = f"Puntos: {state['score']} — Presiona R para reiniciar"
            shadow_sub = self.font.render(sub_text, True, (0, 0, 0))
            main_sub = self.font.render(sub_text, True, (200, 200, 200))

            shadow_sub_rect = shadow_sub.get_rect(center=(center_x + 2, center_y + 12))
            render_surface.blit(shadow_sub, shadow_sub_rect)

            main_sub_rect = main_sub.get_rect(center=(center_x, center_y + 10))
            render_surface.blit(main_sub, main_sub_rect)

        # Aplicar screen shake si es necesario
        if shake_offset != (0, 0) and render_surface != self.screen:
            self.screen.fill((0, 0, 0))
            self.screen.blit(temp_surface, shake_offset)

        # Renderizar flash effect
        self.visual_effects.render_flash(self.screen)
