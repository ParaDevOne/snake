"""
audio_manager.py
Gestor centralizado para audio y música en el juego Snake.
Utiliza helpers de utils.py y configuración de settings.py.
"""
import pygame

from settings import (AUDIO_CONFIG, MUSIC_ENABLED, MUSIC_VOLUME, SOUND_ENABLED,
                      SOUND_VOLUME)
from utils import log_error, log_info, log_warning


class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
        except ImportError as e:
            log_error(f"Error inicializando pygame.mixer: {e}")
        self.sounds = {}
        self.music_loaded = False
        self.load_sounds()
        # Volumen global
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        for sound in self.sounds.values():
            sound.set_volume(SOUND_VOLUME)

    def load_sounds(self):
        for key, path in AUDIO_CONFIG['sounds'].items():
            if key == 'move':
                continue
            try:
                if SOUND_ENABLED:
                    self.sounds[key] = pygame.mixer.Sound(path)
                    self.sounds[key].set_volume(SOUND_VOLUME)
                    log_info(f"Audio cargado: {key} -> {path}")
            except ImportError as e:
                log_error(f"Error cargando audio {key}: {e}")

    def play_sound(self, key):
        if not SOUND_ENABLED:
            return
        sound = self.sounds.get(key)
        if sound:
            sound.play()
        else:
            log_warning(f"Sonido no encontrado: {key}")

    def play_music(self, path, loop=True):
        import os
        if not MUSIC_ENABLED:
            log_info(f"[AUDIO] Música no habilitada. No se reproduce: {path}")
            return
        log_info(f"[AUDIO] Intentando cargar música: {path}")
        if not os.path.isfile(path):
            log_error(f"[AUDIO] Archivo de música no encontrado: {path}")
            return
        try:
            pygame.mixer.music.load(path)
            log_info(f"[AUDIO] Música cargada correctamente: {path}")
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1 if loop else 0)
            self.music_loaded = True
            log_info(f"Música reproducida: {path}")
        except Exception as e:
            log_error(f"Error reproduciendo música: {e}")

    def stop_music(self):
        if self.music_loaded and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            log_info("Música detenida (stop_music llamado)")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)
        for sound in self.sounds.values():
            sound.set_volume(volume)
        log_info(f"Volumen de audio/música ajustado: {volume}")
