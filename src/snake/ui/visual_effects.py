"""A module for advanced visual effects in the Snake game."""
# visual_effects.py
# pylint: disable=no-member

import math
import random
import time
from typing import List, Tuple

import pygame

from src.snake.system import settings


class ParticleSystem:
    """Sistema de partículas para efectos visuales"""

    def __init__(self):
        """Initialize the particle system."""
        self.particles: List[dict] = []

    def add_explosion(
        self,
        pos: Tuple[int, int],
        color: Tuple[int, int, int],
        count: int = 15,
        speed_range: Tuple[float, float] = (2, 6),
    ):
        """Añade una explosión de partículas en la posición dada"""
        x, y = pos
        # Convertir coordenadas de grid a pixels si es necesario
        pixel_x = x if x > 100 else x * settings.GRID_SIZE + settings.GRID_SIZE // 2
        pixel_y = y if y > 100 else y * settings.GRID_SIZE + settings.GRID_SIZE // 2

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(
                {
                    "x": pixel_x,
                    "y": pixel_y,
                    "dx": dx,
                    "dy": dy,
                    "color": color,
                    "life": 1.0,
                    "size": random.randint(2, 5),
                }
            )

    def draw(self, surface):
        """Dibuja todas las partículas en la superficie dada."""
        for particle in self.particles:
            # El tamaño y la opacidad dependen de la vida de la partícula
            size = int(particle["size"] * particle["life"])
            if size <= 0:
                continue

            alpha = int(particle["life"] * 255)

            # Crear superficie para la partícula con canal alpha
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

            # Crear color con alpha
            color = list(particle["color"])
            color.append(alpha)

            # Dibujar círculo
            pygame.draw.circle(surf, color, (size, size), size)

            # Dibujar en la superficie principal
            surface.blit(surf, (int(particle["x"] - size), int(particle["y"] - size)))

    def add_trail_effect(
        self, pos: Tuple[int, int], color: Tuple[int, int, int], count: int = 5
    ) -> None:
        """Añade efecto de rastro para movimiento de la serpiente.

        Args:
            pos: Posición (x,y) donde añadir el rastro
            color: Color RGB del rastro
            count: Número de partículas a crear
        """
        x, y = pos
        # Convertir coordenadas de grid a pixels
        pixel_x = x * settings.GRID_SIZE + settings.GRID_SIZE // 2
        pixel_y = y * settings.GRID_SIZE + settings.GRID_SIZE // 2

        for _ in range(count):
            # Añadir aleatoriedad a la posición
            offset_x = random.uniform(-8, 8)
            offset_y = random.uniform(-8, 8)

            # Crear partícula con velocidad aleatoria
            particle = {
                "x": pixel_x + offset_x,
                "y": pixel_y + offset_y,
                "vel_x": random.uniform(-0.5, 0.5),
                "vel_y": random.uniform(-0.5, 0.5),
                "color": color,
                "life": 0.8,
                "decay": 0.02,
                "size": random.uniform(1, 3),
            }

            self.particles.append(particle)

    def update(self):
        """Actualiza todas las partículas"""
        self.particles = [p for p in self.particles if p["life"] > 0]

        for particle in self.particles:
            particle["x"] += particle["vel_x"]
            particle["y"] += particle["vel_y"]
            particle["vel_x"] *= 0.98  # fricción
            particle["vel_y"] *= 0.98
            particle["life"] -= particle["decay"]

    def render(self, screen):
        """Renderiza todas las partículas"""
        for particle in self.particles:
            if particle["life"] <= 0:
                continue

            alpha = int(255 * particle["life"])
            color = (*particle["color"][:3], alpha)
            size = particle["size"] * particle["life"]

            # Crear superficie con alpha para la partícula
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)  # pylint: disable=no-member
            pygame.draw.circle(surf, color, (size, size), size)
            screen.blit(surf, (particle["x"] - size, particle["y"] - size))


class AnimationManager:
    """Gestor de animaciones suaves"""

    def __init__(self):
        self.start_time = time.time()
        self.animations = []

    def get_time(self):
        """Retorna el tiempo transcurrido desde el inicio"""
        return time.time() - self.start_time

    def update(self):
        """Actualiza todas las animaciones activas."""
        current_time = self.get_time()
        # Filtrar animaciones completadas
        self.animations = [
            anim for anim in self.animations if current_time < anim["end_time"]
        ]

    def pulse_scale(self, frequency=2.0, amplitude=0.2, base_scale=1.0):
        """Genera un factor de escala pulsante"""
        return base_scale + amplitude * math.sin(
            self.get_time() * frequency * 2 * math.pi
        )

    def smooth_interpolate(self, start_pos, end_pos, progress):
        """Interpolación suave entre dos posiciones"""
        # Usar easing cubic para movimiento más natural
        t = progress
        smooth_t = t * t * (3 - 2 * t)  # smoothstep

        x1, y1 = start_pos
        x2, y2 = end_pos

        x = x1 + (x2 - x1) * smooth_t
        y = y1 + (y2 - y1) * smooth_t

        return (x, y)


class VisualEffects:
    """Clase principal para efectos visuales avanzados"""

    def __init__(self, screen: pygame.Surface):
        """Inicializa el sistema de efectos visuales.

        Args:
            screen: Superficie de pygame donde renderizar los efectos
        """
        self.screen = screen
        self.particle_system = ParticleSystem()
        self.animation_manager = AnimationManager()
        self.screen_shake: int = 0
        self.flash_alpha: int = 0
        self.flash_color: tuple[int, int, int] = (255, 255, 255)

    def show_game_over(self):
        """Muestra efectos visuales de Game Over."""
        # Efecto de pantalla roja parpadeante
        self.flash_color = (255, 0, 0)
        self.flash_alpha = 128

        # Efecto de sacudida de pantalla
        self.screen_shake = 20

        # Explosión de partículas
        center = (settings.WINDOW_SIZE[0] // 2, settings.WINDOW_SIZE[1] // 2)
        self.particle_system.add_explosion(center, (255, 0, 0), count=30)

    def show_food_effect(self, pos):
        """Muestra efectos al recoger comida.

        Args:
            pos: Posición (x, y) donde mostrar el efecto
        """
        # Convertir posición de grid a píxeles
        pixel_pos = (
            pos[0] * settings.GRID_SIZE + settings.GRID_SIZE // 2,
            pos[1] * settings.GRID_SIZE + settings.GRID_SIZE // 2,
        )

        # Explosión pequeña de partículas verdes
        self.particle_system.add_explosion(pixel_pos, (0, 255, 0), count=10)

        # Flash suave verde
        self.flash_color = (0, 255, 0)
        self.flash_alpha = 64

    def show_powerup_effect(self, pos):
        """Muestra efectos al recoger un power-up.

        Args:
            pos: Posición (x, y) donde mostrar el efecto
        """
        # Convertir posición de grid a píxeles
        pixel_pos = (
            pos[0] * settings.GRID_SIZE + settings.GRID_SIZE // 2,
            pos[1] * settings.GRID_SIZE + settings.GRID_SIZE // 2,
        )

        # Explosión grande de partículas amarillas
        self.particle_system.add_explosion(pixel_pos, (255, 255, 0), count=20)

        # Flash brillante amarillo
        self.flash_color = (255, 255, 0)
        self.flash_alpha = 96

    def update(self):
        """Actualiza todos los efectos visuales."""
        # Actualizar partículas
        self.particle_system.update()

        # Actualizar animaciones
        self.animation_manager.update()

        # Reducir la intensidad del flash
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - 8)

        # Reducir la intensidad de la sacudida
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - 1)

    def draw(self):
        """Dibuja todos los efectos visuales."""
        # Aplicar sacudida de pantalla
        if self.screen_shake > 0:
            offset = (
                random.randint(-self.screen_shake, self.screen_shake),
                random.randint(-self.screen_shake, self.screen_shake),
            )
            self.screen.blit(self.screen, offset)

        # Dibujar partículas
        self.particle_system.draw(self.screen)

        # Dibujar flash
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface(settings.WINDOW_SIZE)
            flash_surface.fill(self.flash_color)
            flash_surface.set_alpha(self.flash_alpha)
            self.screen.blit(flash_surface, (0, 0))

    def show_splash_screen(self, logo_path, duration=2.5):
        """Muestra una pantalla de presentación con logo y animación de carga.

        Args:
            logo_path: Ruta al archivo de imagen del logo
            duration: Duración en segundos de la pantalla de carga
        """
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        logo = pygame.image.load(logo_path).convert_alpha()
        center_x = settings.WINDOW_SIZE[0] // 2
        center_y = settings.WINDOW_SIZE[1] // 2
        logo_rect = logo.get_rect(center=(center_x, center_y - 40))

        try:
            font = pygame.font.Font(settings.FONT, 32)
        except Exception:
            font = pygame.font.SysFont("arial", 32)

        loading_text = font.render("Loading...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(center_x, center_y + 80))
        dot_count = 0

        while (pygame.time.get_ticks() - start_time) < duration * 1000:
            self.screen.fill((0, 0, 0))
            self.screen.blit(logo, logo_rect)

            # Animación de puntos
            dots = "." * ((dot_count // 20) % 4)
            loading_anim = font.render(f"Loading{dots}", True, (255, 255, 255))
            self.screen.blit(loading_anim, text_rect)

            pygame.display.flip()
            clock.tick(60)
            dot_count += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def add_screen_shake(self, intensity=5):
        """Añade efecto de temblor de pantalla"""
        self.screen_shake = intensity

    def add_flash(self, color=(255, 255, 255), intensity=100):
        """Añade efecto de flash en pantalla"""
        self.flash_color = color
        self.flash_alpha = intensity

    def get_screen_offset(self):
        """Retorna el offset para el efecto de screen shake"""
        if self.screen_shake <= 0:
            return (0, 0)
        offset_x = random.uniform(-self.screen_shake, self.screen_shake)
        offset_y = random.uniform(-self.screen_shake, self.screen_shake)
        return (int(offset_x), int(offset_y))

    def render_flash(self, screen):
        """Renderiza el efecto de flash"""
        if self.flash_alpha > 0:
            flash_surf = pygame.Surface(
                (settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA
            )  # pylint: disable=no-member
            color_with_alpha = (*self.flash_color, int(self.flash_alpha))
            flash_surf.fill(color_with_alpha)
            screen.blit(flash_surf, (0, 0))

    def draw_gradient_rect(self, surface, rect, color1, color2, vertical=True):
        """Dibuja un rectángulo con gradiente"""
        x, y, w, h = rect

        if vertical:
            for i in range(h):
                ratio = i / h if h > 0 else 0
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w - 1, y + i))
        else:
            for i in range(w):
                ratio = i / w if w > 0 else 0
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (x + i, y), (x + i, y + h - 1))

    def draw_glow_circle(self, surface, pos, radius, color, glow_radius=None):
        """Dibuja un círculo con efecto de brillo"""
        if glow_radius is None:
            glow_radius = radius * 2

        # Crear superficie para el brillo
        glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)  # pylint: disable=no-member

        # Dibujar múltiples círculos con alpha decreciente para el efecto de brillo
        for i in range(int(glow_radius), 0, -2):
            alpha = int(30 * (i / glow_radius))
            glow_color = (*color[:3], alpha)
            pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), i)

        # Dibujar el círculo principal
        pygame.draw.circle(glow_surf, color, (glow_radius, glow_radius), radius)

        # Posicionar y dibujar en la superficie principal
        surface.blit(glow_surf, (pos[0] - glow_radius, pos[1] - glow_radius))

    def draw_enhanced_snake_segment(
        self, surface, pos, is_head=False, direction=None, scale=1.0
    ):
        """Dibuja un segmento de serpiente mejorado con efectos"""
        x, y = pos
        pixel_x = int(x * settings.GRID_SIZE)
        pixel_y = int(y * settings.GRID_SIZE)
        size = int(settings.GRID_SIZE * scale)

        # Colores mejorados con gradiente
        if is_head:
            color1 = (180, 255, 180)  # Verde claro
            color2 = (120, 200, 120)  # Verde más oscuro
            glow_color = (144, 238, 144)
        else:
            color1 = (80, 160, 80)
            color2 = (40, 120, 40)
            glow_color = (46, 139, 87)

        # Dibujar sombra sin alpha (causa problemas)
        shadow_offset = 2
        shadow_rect = pygame.Rect(
            pixel_x + shadow_offset, pixel_y + shadow_offset, size, size
        )
        pygame.draw.rect(surface, (20, 20, 20), shadow_rect)  # Sombra sólida

        # Crear superficie temporal para el gradiente
        segment_surface = pygame.Surface((size, size))
        self.draw_gradient_rect(segment_surface, (0, 0, size, size), color1, color2)

        # Dibujar la superficie en la posición correcta
        surface.blit(segment_surface, (pixel_x, pixel_y))

        # Añadir brillo si es la cabeza
        if is_head:
            center = (pixel_x + size // 2, pixel_y + size // 2)
            self.draw_glow_circle(surface, center, size // 3, glow_color)

            # Dibujar "ojos" en la cabeza
            if direction:
                dx, dy = direction
                eye_offset = size // 4
                if dx != 0:  # Movimiento horizontal
                    eye1_pos = (
                        center[0] + dx * eye_offset,
                        center[1] - eye_offset // 2,
                    )
                    eye2_pos = (
                        center[0] + dx * eye_offset,
                        center[1] + eye_offset // 2,
                    )
                else:  # Movimiento vertical
                    eye1_pos = (
                        center[0] - eye_offset // 2,
                        center[1] + dy * eye_offset,
                    )
                    eye2_pos = (
                        center[0] + eye_offset // 2,
                        center[1] + dy * eye_offset,
                    )

                pygame.draw.circle(surface, (255, 255, 255), eye1_pos, 3)
                pygame.draw.circle(surface, (255, 255, 255), eye2_pos, 3)
                pygame.draw.circle(surface, (0, 0, 0), eye1_pos, 2)
                pygame.draw.circle(surface, (0, 0, 0), eye2_pos, 2)

    def draw_enhanced_food(self, surface, pos, pulse_scale=1.0):
        """Dibuja comida mejorada con efectos"""
        x, y = pos
        pixel_x = int(x * settings.GRID_SIZE + settings.GRID_SIZE // 2)
        pixel_y = int(y * settings.GRID_SIZE + settings.GRID_SIZE // 2)

        radius = int((settings.GRID_SIZE // 2 - 2) * pulse_scale)

        # Colores con gradiente radial
        colors = [
            (255, 100, 90, 80),  # Exterior con alpha
            (255, 120, 110, 120),
            (255, 140, 130, 160),
            (255, 160, 150, 200),  # Interior más sólido
        ]

        # Dibujar múltiples círculos para efecto de brillo
        for i, color in enumerate(colors):
            current_radius = radius - i * 2
            if current_radius > 0:
                glow_surf = pygame.Surface(
                    (current_radius * 4, current_radius * 4), pygame.SRCALPHA
                )
                pygame.draw.circle(
                    glow_surf,
                    color,
                    (current_radius * 2, current_radius * 2),
                    current_radius,
                )
                surface.blit(
                    glow_surf,
                    (pixel_x - current_radius * 2, pixel_y - current_radius * 2),
                )

        # Añadir brillo especial
        self.draw_glow_circle(surface, (pixel_x, pixel_y), radius // 2, (255, 200, 100))

    def draw_enhanced_powerup(self, surface, pos, powerup_type, rotation=0):
        """Dibuja powerup mejorado con efectos específicos por tipo"""
        x, y = pos
        pixel_x = int(x * settings.GRID_SIZE + settings.GRID_SIZE // 2)
        pixel_y = int(y * settings.GRID_SIZE + settings.GRID_SIZE // 2)

        size = settings.GRID_SIZE // 2 - 1

        # Colores por tipo de powerup
        type_colors = {
            "slow": [(100, 150, 255), (150, 200, 255)],
            "speed": [(255, 180, 100), (255, 220, 150)],
            "grow": [(200, 150, 255), (230, 180, 255)],
            "score": [(255, 220, 100), (255, 240, 150)],
        }

        colors = type_colors.get(powerup_type, [(200, 200, 200), (240, 240, 240)])

        # Dibujar forma específica según el tipo
        if powerup_type == "speed":
            # Triángulo para velocidad
            points = []
            for i in range(3):
                angle = rotation + i * 2 * math.pi / 3
                x_point = pixel_x + size * math.cos(angle)
                y_point = pixel_y + size * math.sin(angle)
                points.append((x_point, y_point))
            pygame.draw.polygon(surface, colors[0], points)

        elif powerup_type == "grow":
            # Hexágono para crecimiento
            points = []
            for i in range(6):
                angle = rotation + i * math.pi / 3
                x_point = pixel_x + size * math.cos(angle)
                y_point = pixel_y + size * math.sin(angle)
                points.append((x_point, y_point))
            pygame.draw.polygon(surface, colors[0], points)

        elif powerup_type == "score":
            # Estrella para puntos
            outer_radius = size
            inner_radius = size * 0.6
            points = []
            for i in range(10):
                angle = rotation + i * math.pi / 5
                if i % 2 == 0:
                    radius = outer_radius
                else:
                    radius = inner_radius
                x_point = pixel_x + radius * math.cos(angle)
                y_point = pixel_y + radius * math.sin(angle)
                points.append((x_point, y_point))
            pygame.draw.polygon(surface, colors[0], points)

        else:  # slow - círculo con efecto especial
            self.draw_glow_circle(surface, (pixel_x, pixel_y), size, colors[0])

        # Añadir brillo común a todos los tipos
        self.draw_glow_circle(surface, (pixel_x, pixel_y), size + 5, colors[1])


# Función auxiliar para crear gradientes lineales
def create_linear_gradient(surface, rect, color_start, color_end, vertical=True):
    """Crea un gradiente lineal en un rectángulo"""
    x, y, w, h = rect

    if vertical:
        for i in range(h):
            ratio = i / h if h > 0 else 0
            r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
            g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
            b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w - 1, y + i))
    else:
        for i in range(w):
            ratio = i / w if w > 0 else 0
            r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
            g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
            b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (x + i, y), (x + i, y + h - 1))
