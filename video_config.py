"""
Módulo de configuración de video.

Este módulo proporciona funcionalidades para configurar el controlador de video
según la plataforma y las necesidades específicas del sistema.
"""

import os
import platform
import utils

# Importación opcional de pygame para pruebas de inicialización
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


def configure_additional_env_vars():
    """
    Configura variables de entorno adicionales para optimizar el rendimiento de video.

    Establece variables como SDL_VIDEO_WINDOW_POS, SDL_HINT_RENDER_DRIVER,
    y SDL_HINT_RENDER_SCALE_QUALITY para mejorar el rendimiento y comportamiento
    del sistema de video.

    Returns:
        dict: Diccionario con las variables configuradas y sus valores.

    Raises:
        RuntimeError: Si ocurre un error al configurar las variables de entorno.
    """
    configured_vars = {}

    try:
        # Configurar posición de ventana (centrar)
        window_pos = "centered"
        os.environ['SDL_VIDEO_WINDOW_POS'] = window_pos
        configured_vars['SDL_VIDEO_WINDOW_POS'] = window_pos
        utils.log_debug(f"Variable SDL_VIDEO_WINDOW_POS configurada: {window_pos}", "VIDEO")

        # Configurar driver de render según la plataforma
        system: str = platform.system()
        if system == "Windows":
            render_driver = "direct3d"
        elif system in ["Linux", "Darwin"]:
            render_driver = "opengl"
        else:
            render_driver = "opengl"  # fallback

        os.environ['SDL_HINT_RENDER_DRIVER'] = render_driver
        configured_vars['SDL_HINT_RENDER_DRIVER'] = render_driver
        utils.log_debug(f"Variable SDL_HINT_RENDER_DRIVER configurada: {render_driver}", "VIDEO")

        # Configurar calidad de escalado
        scale_quality = "1"  # Linear filtering
        os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = scale_quality
        configured_vars['SDL_HINT_RENDER_SCALE_QUALITY'] = scale_quality
        utils.log_debug(f"Variable SDL_HINT_RENDER_SCALE_QUALITY configurada: {scale_quality}", "VIDEO")

        # Configurar variables adicionales para mejor rendimiento
        try:
            # Habilitar aceleración por hardware cuando sea posible
            os.environ['SDL_HINT_RENDER_DRIVER_HARDWARE'] = "1"
            configured_vars['SDL_HINT_RENDER_DRIVER_HARDWARE'] = "1"
            utils.log_debug("Variable SDL_HINT_RENDER_DRIVER_HARDWARE configurada: 1", "VIDEO")

            # Optimizar para baja latencia
            os.environ['SDL_HINT_RENDER_VSYNC'] = "0"
            configured_vars['SDL_HINT_RENDER_VSYNC'] = "0"
            utils.log_debug("Variable SDL_HINT_RENDER_VSYNC configurada: 0", "VIDEO")

        except ImportError as e:
            utils.log_warning(f"Error configurando variables de rendimiento adicionales: {e}", "VIDEO")

        utils.log_info(f"Variables de entorno adicionales configuradas exitosamente: {len(configured_vars)} variables", "VIDEO")
        return configured_vars

    except Exception as e:
        error_msg = f"Error general al configurar variables de entorno adicionales: {e}"
        utils.log_warning(error_msg, "VIDEO")
        raise RuntimeError(error_msg) from e


def configure_video_driver():
    """
    Configura el controlador de video según la plataforma y configuración del sistema.

    Esta función determina la configuración óptima del controlador de video
    basándose en el sistema operativo, hardware disponible y preferencias del usuario.

    Returns:
        dict: Configuración del controlador de video aplicada.

    Raises:
        RuntimeError: Si no se puede configurar un controlador de video válido.
    """
    # Obtener información de la plataforma
    system = platform.system()

    # Configuración base
    video_config = {
        'platform': system,
        'pygame_available': PYGAME_AVAILABLE,
        'driver': None,
        'initialized': False
    }

    # Definir listas de drivers preferidos por plataforma
    platform_drivers = {
        'Windows': ['windows', 'windib'],
        'Linux': ['x11', 'wayland', 'fbcon'],
        'Darwin': ['cocoa']  # macOS
    }

    # Obtener la lista de drivers para la plataforma actual
    preferred_drivers = platform_drivers.get(system, [])

    if not preferred_drivers:
        utils.log_warning(f"Plataforma no soportada: {system}", "VIDEO")
        raise RuntimeError(f"Plataforma no soportada: {system}")

    # Iterar por los drivers preferidos e intentar configurar cada uno
    selected_driver = None
    for driver in preferred_drivers:
        try:
            # Configurar la variable de entorno SDL
            os.environ['SDL_VIDEODRIVER'] = driver
            utils.log_info(f"Intentando driver de video: {driver}", "VIDEO")

            # Si pygame está disponible, probar la inicialización
            if PYGAME_AVAILABLE:
                try:
                    pygame.display.init()
                    # Si llegamos aquí, la inicialización fue exitosa
                    selected_driver = driver
                    video_config['driver'] = driver
                    video_config['initialized'] = True
                    utils.log_info(f"Driver de video configurado exitosamente: {driver}", "VIDEO")
                    break
                except ImportError as e:
                    utils.log_warning(f"Falló la inicialización con driver {driver}: {e}", "VIDEO")
                    continue
            else:
                # Si pygame no está disponible, simplemente configurar el driver
                selected_driver = driver
                video_config['driver'] = driver
                utils.log_info(f"Driver de video configurado (sin prueba pygame): {driver}", "VIDEO")
                break

        except ImportError as e:
            utils.log_warning(f"Error configurando driver {driver}: {e}", "VIDEO")
            continue

    # Verificar si se pudo configurar algún driver
    if selected_driver is None:
        utils.log_warning(f"No se pudo configurar ningún driver para {system}. Usando fallback.", "VIDEO")
        # Como fallback, no establecer SDL_VIDEODRIVER y dejar que SDL elija
        if 'SDL_VIDEODRIVER' in os.environ:
            del os.environ['SDL_VIDEODRIVER']
        video_config['driver'] = 'default'

    return video_config


def _detect_available_drivers():
    """
    Detecta los controladores de video disponibles en el sistema.
    """
    # Implementar detección de controladores
    return []


def _initialize_pygame_test():
    """
    Realiza una prueba de inicialización con pygame si está disponible.
    """

    if not PYGAME_AVAILABLE:
        return False

    try:
        # Implementar prueba de inicialización con pygame
        return True
    except ImportError:
        return False


def configure_video_complete():
    """
    Esta función combina la configuración del driver de video principal con
    las variables de entorno adicionales para proporcionar una configuración
    completa y optimizada del sistema de video.
    """

    complete_config = {}

    try:
        utils.log_info("Iniciando configuración completa del sistema de video", "VIDEO")

        # Configurar driver principal
        driver_config = configure_video_driver()
        complete_config['driver_config'] = driver_config

        # Configurar variables de entorno adicionales
        env_vars_config = configure_additional_env_vars()
        complete_config['additional_env_vars'] = env_vars_config

        # Obtener información completa del sistema
        video_info = get_video_info()
        complete_config['system_info'] = video_info

        utils.log_info("Configuración completa del sistema de video finalizada exitosamente", "VIDEO")
        return complete_config

    except Exception as e:
        error_msg = f"Error en configuración completa del sistema de video: {e}"
        utils.log_warning(error_msg, "VIDEO")
        raise RuntimeError(error_msg) from e


def get_video_info():
    """
    Obtiene información detallada sobre la configuración de video actual.
    """
    # Variables SDL relevantes para video
    sdl_video_vars = [
        'SDL_VIDEODRIVER', 'SDL_VIDEO_WINDOW_POS', 'SDL_HINT_RENDER_DRIVER',
        'SDL_HINT_RENDER_SCALE_QUALITY', 'SDL_HINT_RENDER_DRIVER_HARDWARE',
        'SDL_HINT_RENDER_VSYNC'
    ]

    info = {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'pygame_available': PYGAME_AVAILABLE,
        'environment_vars': {
            key: value for key, value in os.environ.items()
            if 'video' in key.lower() or 'display' in key.lower() or key in sdl_video_vars
        },
        'sdl_video_config': {
            var: os.environ.get(var, 'No configurado') for var in sdl_video_vars
        }
    }

    return info
