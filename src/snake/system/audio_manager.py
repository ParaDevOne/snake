"""
audio_manager.py
Gestor centralizado para audio y música en el juego Snake.
Utiliza helpers de utils.py y configuración de settings.py.
"""

import os

import pygame

from src.snake.system import settings
from src.snake.system.utils import log_error, log_info, log_warning


class AudioManager:
    """Gestor de audio para el juego."""
    def __init__(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
        except ImportError as e:
            log_error(f"Error inicializando pygame.mixer: {e}")
        self.sounds = {}
        self.music_loaded = False
        self.load_sounds()
        # Volumen global
        pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
        for sound in self.sounds.values():
            sound.set_volume(settings.SOUND_VOLUME)

    def load_sounds(self):
        """Cargar los sonidos del juego."""
        for key, path in settings.AUDIO_CONFIG['sounds'].items():
            if key == 'move':
                continue
            try:
                # La carga se realiza siempre, la reproducción se condiciona
                self.sounds[key] = pygame.mixer.Sound(path)
                self.sounds[key].set_volume(settings.SOUND_VOLUME)
                log_info(f"Audio cargado: {key} -> {path}")
            except ImportError as e:
                log_error(f"Error cargando audio {key}: {e}")

    def play_sound(self, key):
        """Reproducir un sonido dado por su clave."""
        if not settings.SOUND_ENABLED:
            return
        sound = self.sounds.get(key)
        if sound:
            sound.play()
        else:
            log_warning(f"Sonido no encontrado: {key}")

    def play_music(self, path, loop=True):
        """Reproducir música desde el archivo dado."""
        if not settings.MUSIC_ENABLED:
            log_info(f"[AUDIO] Música no habilitada. No se reproduce: {path}")
            return
        log_info(f"[AUDIO] Intentando cargar música: {path}")
        if not os.path.isfile(path):
            log_error(f"[AUDIO] Archivo de música no encontrado: {path}")
            return
        try:
            pygame.mixer.music.load(path)
            log_info(f"[AUDIO] Música cargada correctamente: {path}")
            pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
            pygame.mixer.music.play(-1 if loop else 0)
            self.music_loaded = True
            log_info(f"Música reproducida: {path}")
        except ImportError as e:
            log_error(f"Error reproduciendo música: {e}")

    def stop_music(self):
        """Detener la música en reproducción."""
        if self.music_loaded and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            log_info("Música detenida (stop_music llamado)")

    def set_volume(self, volume):
        """Ajustar el volumen de audio y música."""
        pygame.mixer.music.set_volume(volume)
        for sound in self.sounds.values():
            sound.set_volume(volume)
        log_info(f"Volumen de audio/música ajustado: {volume}")
        log_info(f"Volumen de audio/música ajustado: {volume}")
