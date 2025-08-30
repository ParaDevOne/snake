"""
Manejo de configuración del juego.
Carga la configuración desde archivos y proporciona valores por defecto.
"""
import os
import json

# Configuración por defecto
DEFAULT_CONFIG = {
    "WINDOW": {
        "WIDTH": 800,
        "HEIGHT": 600,
        "TITLE": "Snake Game",
        "FPS": 60,
        "FULLSCREEN": False
    },
    "GAME": {
        "GRID_SIZE": 20,
        "INITIAL_SPEED": 10,
        "MAX_SPEED": 20,
        "SPEED_INCREASE": 0.5
    },
    "COLORS": {
        "BACKGROUND": (0, 0, 0),
        "SNAKE_HEAD": (0, 255, 0),
        "SNAKE_BODY": (0, 200, 0),
        "FOOD": (255, 0, 0),
        "TEXT": (255, 255, 255),
        "SCORE": (255, 255, 0)
    },
    "PATHS": {
        "ASSETS": "Data/assets",
        "SAVES": "Data/saves"
    }
}

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = {}
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Carga la configuración desde el archivo o usa valores por defecto."""
        config_path = os.path.join('Data', 'config.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self._config = json.load(f)
            else:
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                # Guardar configuración por defecto
                with open(config_path, 'w') as f:
                    json.dump(DEFAULT_CONFIG, f, indent=4)
                self._config = DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            self._config = DEFAULT_CONFIG.copy()

    def get(self, section, key, default=None):
        """Obtiene un valor de configuración."""
        return self._config.get(section, {}).get(key, default)

    def set(self, section, key, value):
        """Establece un valor de configuración."""
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        self._save_config()

    def _save_config(self):
        """Guarda la configuración en el archivo."""
        try:
            config_path = os.path.join('Data', 'config.json')
            with open(config_path, 'w') as f:
                json.dump(self._config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

# Instancia global de configuración
config = Config()
