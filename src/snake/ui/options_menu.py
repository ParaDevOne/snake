"""
Módulo para el menú de opciones del juego Snake.
"""

import os
import sys

import pygame

# Importaciones locales
from .base_state import GameState
from ..utils.config import config
from ..utils.logger import log_info, log_debug

# Asegurar que el módulo raíz esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class OptionsMenu(GameState):
    """Menú de opciones del juego."""
    
    def cleanup(self):
        """Limpia los recursos del menú de opciones."""
        log_info("Limpiando recursos del menú de opciones", context="OPTIONS")

    def __init__(self, game):
        super().__init__(game)
        self.options = [
            {
                "name": "Pantalla Completa",
                "type": "bool",
                "key": "FULLSCREEN",
                "value": config.get("WINDOW", "FULLSCREEN", False),
                "section": "WINDOW",
            },
            {
                "name": "Volumen Música",
                "type": "range",
                "key": "MUSIC_VOLUME",
                "value": config.get("AUDIO", "MUSIC_VOLUME", 70),
                "min": 0,
                "max": 100,
                "section": "AUDIO",
            },
            {
                "name": "Volumen Efectos",
                "type": "range",
                "key": "SFX_VOLUME",
                "value": config.get("AUDIO", "SFX_VOLUME", 80),
                "min": 0,
                "max": 100,
                "section": "AUDIO",
            },
            {
                "name": "Velocidad Inicial",
                "type": "range",
                "key": "INITIAL_SPEED",
                "value": config.get("GAME", "INITIAL_SPEED", 10),
                "min": 1,
                "max": 30,
                "section": "GAME",
            },
        ]
        self.selected = 0
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.editing = False
        log_info("Menú de opciones inicializado", context="OPTIONS")

    def handle_events(self, event):
        """Handle events for the options menu.
        
        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            self.running = False
            self.game.running = False
        elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if self.editing:
                self._handle_edit_input(event)
            else:
                self._handle_menu_navigation(event)

    def _handle_menu_navigation(self, event):
        """Maneja la navegación por el menú."""
        if event.key == pygame.K_UP:  # pylint: disable=no-member
            self.selected = (self.selected - 1) % len(self.options)
            log_debug(
                f"Opción seleccionada: {self.options[self.selected]['name']}", "OPTIONS"
            )

        elif event.key == pygame.K_DOWN:  # pylint: disable=no-member
            self.selected = (self.selected + 1) % len(self.options)
            log_debug(
                f"Opción seleccionada: {self.options[self.selected]['name']}", "OPTIONS"
            )

        elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):  # pylint: disable=no-member
            self._adjust_setting(-1 if event.key == pygame.K_LEFT else 1)  # pylint: disable=no-member

        elif event.key == pygame.K_RETURN:  # pylint: disable=no-member
            if self.options[self.selected]["type"] == "bool":
                self._toggle_bool_setting()
            else:
                self.editing = True
                log_debug(
                    f"Editando opción: {self.options[self.selected]['name']}", "OPTIONS"
                )

        elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
            self.running = False

    def _handle_edit_input(self, event):
        """Maneja la entrada de texto al editar una opción."""
        if event.key == pygame.K_RETURN:  # pylint: disable=no-member
            self.editing = False
            log_debug("Edición de opción terminada", "OPTIONS")

        elif event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
            self.editing = False
            log_debug("Edición cancelada", "OPTIONS")

        elif event.key == pygame.K_BACKSPACE:  # pylint: disable=no-member
            # Manejar borrado de caracteres si fuera necesario
            pass

    def _toggle_bool_setting(self):
        """Alterna un valor booleano en la configuración."""
        option = self.options[self.selected]
        option["value"] = not option["value"]
        config.set(option["section"], option["key"], option["value"])
        log_info(f"Opción {option['name']} cambiada a {option['value']}", "OPTIONS")

    def _adjust_setting(self, delta):
        """Ajusta un valor numérico en la configuración."""
        option = self.options[self.selected]
        if option["type"] == "range":
            new_value = option["value"] + delta
            if option["min"] <= new_value <= option["max"]:
                option["value"] = new_value
                config.set(option["section"], option["key"], new_value)
                log_info(f"Opción {option['name']} ajustada a {new_value}", "OPTIONS")

    def update(self, dt):
        # Actualizaciones del menú (si son necesarias)
        pass

    def draw(self):
        # Fondo
        self.screen.fill(config.get("COLORS", "BACKGROUND", (0, 0, 0)))

        # Título
        title = self.title_font.render("OPCIONES", True, (255, 255, 255))
        window_width = config.get("WINDOW", "WIDTH") or 800
        title_rect = title.get_rect(
            center=(window_width // 2, 80)
        )
        self.screen.blit(title, title_rect)

        # Instrucciones
        instructions = self.font.render(
            "Usa ↑/↓ para navegar, ←/→ para cambiar valores, ESC para volver",
            True,
            (150, 150, 150),
        )
        # Obtener dimensiones de la ventana con valores por defecto seguros
        window_width = int(config.get("WINDOW", "WIDTH", 800) or 800)
        window_height = int(config.get("WINDOW", "HEIGHT", 600) or 600)

        instructions_rect = instructions.get_rect(
            midbottom=(
                window_width // 2,
                window_height - 30,
            )
        )
        self.screen.blit(instructions, instructions_rect)

        # Opciones
        for i, option in enumerate(self.options):
            y_pos = 180 + i * 60
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)

            # Nombre de la opción
            name_text = self.font.render(option["name"], True, color)
            self.screen.blit(name_text, (200, y_pos))

            # Valor actual
            if option["type"] == "bool":
                value_text = "Activado" if option["value"] else "Desactivado"
            else:
                value_text = str(option["value"])
                if option["type"] == "range":
                    value_text += f" ({option['min']}-{option['max']})"

            value_color = (
                (0, 255, 0) if i == self.selected and self.editing else (200, 200, 200)
            )
            value_render = self.font.render(value_text, True, value_color)
            self.screen.blit(value_render, (500, y_pos))

            # Indicador de edición
            if i == self.selected and self.editing:
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 0),
                    (490, y_pos - 5, value_render.get_width() + 20, 40),
                    2,
                )
