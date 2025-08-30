"""
Manejo de configuración del juego.
Carga la configuración desde archivos y proporciona valores por defecto.
"""

import json
import os

# Configuración por defecto
DEFAULT_CONFIG = {
    "WINDOW": {
        "WIDTH": 800,
        "HEIGHT": 600,
        "TITLE": "Snake Game",
        "FPS": 60,
        "FULLSCREEN": False,
    },
    "GAME": {
        "GRID_SIZE": 20,
        "INITIAL_SPEED": 10,
        "MAX_SPEED": 20,
        "SPEED_INCREASE": 0.5,
    },
    "COLORS": {
        "BACKGROUND": (0, 0, 0),
        "SNAKE_HEAD": (0, 255, 0),
        "SNAKE_BODY": (0, 200, 0),
        "FOOD": (255, 0, 0),
        "TEXT": (255, 255, 255),
        "SCORE": (255, 255, 0),
    },
    "PATHS": {
        "ASSETS": "Data/assets",
        "SAVES": "Data/saves",
        "FONTS": "Data/assets/fonts"
    },
    "FONT": "Data/assets/font.ttf",
}


class Config:
    """Clase que maneja la configuración del juego."""

    _instance = None

    def __init__(self):
        """Inicializa la configuración."""
        self._config = {}
        self._load_config()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = {}
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Carga la configuración desde el archivo o usa los valores por defecto."""
        try:
            # Asegurar que el directorio Data existe
            os.makedirs("Data", exist_ok=True)

            config_path = os.path.join("Data", "config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        loaded_config = json.load(f)
                        # Asegurarse de que la configuración cargada tenga la estructura correcta
                        if not isinstance(loaded_config, dict):
                            raise ValueError("Config file is not a valid JSON object")
                        self._config = self._deep_update(DEFAULT_CONFIG.copy(), loaded_config)
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error al cargar la configuración: {e}. Usando valores por defecto.")
                    self._config = DEFAULT_CONFIG.copy()
                    self._save_config()
            else:
                self._config = DEFAULT_CONFIG.copy()
                self._save_config()

            # Asegurarse de que los valores requeridos existen
            for section, keys in DEFAULT_CONFIG.items():
                if section not in self._config:
                    self._config[section] = {}
                if isinstance(keys, dict):
                    for key, default_value in keys.items():
                        if key not in self._config[section]:
                            self._config[section][key] = default_value

        except ImportError as e:
            print(f"Error inesperado al cargar la configuración: {e}")
            self._config = DEFAULT_CONFIG.copy()

    def _deep_update(self, original, update):
        """Actualiza un diccionario de forma recursiva."""
        for key, value in update.items():
            if (
                isinstance(value, dict)
                and key in original
                and isinstance(original[key], dict)
            ):
                original[key] = self._deep_update(original[key], value)
            else:
                original[key] = value
        return original

    def get(self, section, key, default=None):
        """
        Obtiene un valor de configuración.

        Args:
            section (str): Sección de configuración
            key (str): Clave de configuración
            default: Valor por defecto si no se encuentra la clave

        Returns:
            El valor de la configuración o el valor por defecto
        """
        try:
            # First try to get from current config
            if section in self._config and key in self._config[section]:
                value = self._config[section][key]
                return value if value is not None else default

            # If not found, try to get from default config
            if section in DEFAULT_CONFIG and key in DEFAULT_CONFIG[section]:
                return DEFAULT_CONFIG[section][key]

            return default

        except (KeyError, TypeError, AttributeError):
            return default

    def set(self, section, key, value):
        """
        Establece un valor de configuración.

        Args:
            section (str): Sección de configuración
            key (str): Clave de configuración
            value: Valor a establecer
        """
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        self._save_config()

    def _save_config(self):
        """Guarda la configuración en el archivo."""
        try:
            # Asegurar que el directorio Data existe
            os.makedirs("Data", exist_ok=True)

            config_path = os.path.join("Data", "config.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except ImportError as e:
            print(f"Error al guardar la configuración: {e}")

    def reset_to_defaults(self):
        """Restablece la configuración a los valores por defecto."""
        self._config = DEFAULT_CONFIG.copy()
        self._save_config()

# Instancia global de configuración
config = Config()
