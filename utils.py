# utils.py
import json
import sys
import os
import datetime
import threading
from enum import Enum
import random
import settings

# Configurar encoding UTF-8 para Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except ImportError:
        pass  # Si falla, continuar sin UTF-8

def random_free_cell(occupied, extra_forbidden=None):
    occupied_set = set(occupied)
    extra = set(extra_forbidden or [])
    free = [ (x, y)
            for x in range(settings.COLUMNS)
            for y in range(settings.ROWS)
            if (x, y) not in occupied_set and (x, y) not in extra ]
    return random.choice(free) if free else None

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        pass
    return default

def save_json(path, obj):
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f)
    except (OSError, TypeError, ValueError, UnicodeEncodeError) as e:
        # no queremos que falle el juego por un save fallido
        print("No se pudo salvar:", e)

# ===== SISTEMA DE LOGGING =====

class LogLevel(Enum):
    """Niveles de logging"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Logger:
    """Sistema de logging para Snake Game"""

    def __init__(self):
        self.log_file = os.path.join("Data", "logs.txt")
        self.lock = threading.Lock()
        self.console_enabled = True
        self.file_enabled = True
        self.min_console_level = LogLevel.INFO  # Solo INFO y superiores en consola
        self.min_file_level = LogLevel.DEBUG    # Todos los niveles en archivo

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Inicializar archivo de log con header de sesión
        self._write_session_header()

    def _sanitize_text(self, text, for_console=False):
        """Remueve o reemplaza caracteres problemáticos"""
        # Mapeo de emojis a texto
        emoji_map = {
            '🎮': '[GAME]',
            '⚡': '[PERF]',
            '✨': '[VFX]',
            '🖥️': '[SYS]',
            '👤': '[USER]',
            '🐍': '[SNAKE]',
            '📅': '[DATE]'
        }

        result = text

        # Para consola en Windows, siempre reemplazar emojis
        if for_console and os.name == 'nt':
            for emoji, replacement in emoji_map.items():
                result = result.replace(emoji, replacement)
        else:
            # Para archivo, intentar mantener emojis primero
            try:
                # Probar si se pueden codificar los emojis
                result.encode('utf-8')
            except UnicodeEncodeError:
                # Solo si falla, reemplazar emojis
                for emoji, replacement in emoji_map.items():
                    result = result.replace(emoji, replacement)

        # Caracteres especiales españoles solo para archivos
        if not for_console:
            special_chars = {
                'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
                'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
                'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U'
            }

            for char, replacement in special_chars.items():
                result = result.replace(char, replacement)

        return result

    def _sanitize_for_file(self, text):
        """Sanitiza texto para escribir en archivo"""
        return self._sanitize_text(text, for_console=False)

    def _write_session_header(self):
        """Escribe header de nueva sesión en el archivo de log"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            separator = "=" * 60
            header = f"\n{separator}\nSNAKE GAME - NUEVA SESION INICIADA\nFecha: {timestamp}\n{separator}\n"

            with open(self.log_file, "a", encoding="utf-8", errors="replace") as f:
                f.write(header)
        except (OSError, UnicodeEncodeError):
            pass  # No fallar si no se puede escribir

    def _should_log_to_console(self, level):
        """Determina si debe mostrar en consola según el nivel"""
        if not self.console_enabled:
            return False

        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4
        }

        return level_order.get(level, 0) >= level_order.get(self.min_console_level, 1)

    def _should_log_to_file(self, level):
        """Determina si debe escribir en archivo según el nivel"""
        if not self.file_enabled:
            return False

        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4
        }

        return level_order.get(level, 0) >= level_order.get(self.min_file_level, 0)

    def _format_message(self, level, message, module=None):
        """Formatea el mensaje de log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        module_part = f"[{module}]" if module else ""
        return f"[{timestamp}] {level.value:8} {module_part} {message}"

    def _get_console_color(self, level):
        """Retorna código de color ANSI para consola según el nivel"""
        colors = {
            LogLevel.DEBUG: "\033[36m",    # Cian
            LogLevel.INFO: "\033[32m",     # Verde
            LogLevel.WARNING: "\033[33m",  # Amarillo
            LogLevel.ERROR: "\033[31m",    # Rojo
            LogLevel.CRITICAL: "\033[35m"  # Magenta
        }
        return colors.get(level, "\033[0m")  # Default sin color

    def _log(self, level, message, module=None):
        """Función interna de logging"""
        with self.lock:
            formatted_msg = self._format_message(level, message, module)

            # Log a consola (con sanitización para Windows)
            if self._should_log_to_console(level):
                try:
                    color = self._get_console_color(level)
                    reset = "\033[0m"
                    console_msg = self._sanitize_text(formatted_msg, for_console=True)
                    print(f"{color}{console_msg}{reset}")
                except UnicodeEncodeError:
                    # Fallback: mensaje sin colores y sanitizado
                    safe_msg = self._sanitize_text(formatted_msg, for_console=True)
                    print(safe_msg)

            # Log a archivo (con sanitización)
            if self._should_log_to_file(level):
                try:
                    sanitized_msg = self._sanitize_for_file(formatted_msg)
                    with open(self.log_file, "a", encoding="utf-8", errors="replace") as f:
                        f.write(sanitized_msg + "\n")
                except (OSError, UnicodeEncodeError):
                    pass  # No fallar si no se puede escribir

    def debug(self, message, module=None):
        """Log nivel DEBUG"""
        self._log(LogLevel.DEBUG, message, module)

    def info(self, message, module=None):
        """Log nivel INFO"""
        self._log(LogLevel.INFO, message, module)

    def warning(self, message, module=None):
        """Log nivel WARNING"""
        self._log(LogLevel.WARNING, message, module)

    def error(self, message, module=None):
        """Log nivel ERROR"""
        self._log(LogLevel.ERROR, message, module)

    def critical(self, message, module=None):
        """Log nivel CRITICAL"""
        self._log(LogLevel.CRITICAL, message, module)

    def game_event(self, event, details=None):
        """Log específico para eventos del juego"""
        msg = f"🎮 {event}"
        if details:
            msg += f" - {details}"
        self.info(msg, "GAME")

    def performance(self, action, duration_ms):
        """Log de rendimiento"""
        if duration_ms > 16:  # Solo si tarda más de 1 frame (60fps)
            self.warning(f"⚡ {action} tardó {duration_ms:.1f}ms", "PERF")
        else:
            self.debug(f"⚡ {action}: {duration_ms:.1f}ms", "PERF")

    def visual_effect(self, effect, details=None):
        """Log específico para efectos visuales"""
        msg = f"✨ {effect}"
        if details:
            msg += f" - {details}"
        self.debug(msg, "VFX")

    def system_info(self, info):
        """Log de información del sistema"""
        self.info(f"🖥️ {info}", "SYS")

    def user_action(self, action):
        """Log de acciones del usuario"""
        self.info(f"👤 {action}", "USER")

    def close_session(self):
        """Cierra la sesión de logging"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            footer = f"\nSESION TERMINADA: {timestamp}\n{'='*60}\n"

            with open(self.log_file, "a", encoding="utf-8", errors="replace") as f:
                f.write(footer)
        except (OSError, UnicodeEncodeError):
            pass

class _LoggerSingleton:
    """Singleton para manejar la instancia global del logger"""
    _instance = None

    @classmethod
    def get_instance(cls):
        """Obtiene la instancia única del logger"""
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance

def get_logger():
    """Obtiene la instancia global del logger"""
    return _LoggerSingleton.get_instance()

# Funciones de conveniencia para logging
def log_debug(message, module=None):
    """Log nivel DEBUG"""
    get_logger().debug(message, module)

def log_info(message, module=None):
    """Log nivel INFO"""
    get_logger().info(message, module)

def log_warning(message, module=None):
    """Log nivel WARNING"""
    get_logger().warning(message, module)

def log_error(message, module=None):
    """Log nivel ERROR"""
    get_logger().error(message, module)

def log_critical(message, module=None):
    """Log nivel CRITICAL"""
    get_logger().critical(message, module)

def log_game_event(event, details=None):
    """Log específico para eventos del juego"""
    get_logger().game_event(event, details)

def log_performance(action, duration_ms):
    """Log de rendimiento"""
    get_logger().performance(action, duration_ms)

def log_visual_effect(effect, details=None):
    """Log específico para efectos visuales"""
    get_logger().visual_effect(effect, details)

def log_system_info(info):
    """Log de información del sistema"""
    get_logger().system_info(info)

def log_user_action(action):
    """Log de acciones del usuario"""
    get_logger().user_action(action)

def close_logging_session():
    """Cierra la sesión de logging"""
    instance = _LoggerSingleton.get_instance()
    if instance:
        instance.close_session()
