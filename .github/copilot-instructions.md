# Copilot Instructions for Snake Game

## Overview

Este proyecto es una versión avanzada y modular del clásico Snake en Python. El objetivo es mantener una arquitectura clara, extensible y fácil de mantener, con efectos visuales modernos y gestión persistente de datos.

## Estructura del Proyecto

- `main.py`: Punto de entrada, loop principal y orquestación de componentes.
- `game.py`: Controlador y gestión del estado del juego.
- `snake.py`: Lógica de la serpiente y su movimiento.
- `food.py`: Lógica de comida y powerups.
- `menu.py`: Sistema de menús (si está presente).
- `logic.py`: Funciones auxiliares y utilidades lógicas.
- `settings.py`: Configuración centralizada (controles, visual, gameplay).
- `profiles.py`: Gestión de perfiles y puntajes.
- `utils.py`: Utilidades, sistema de logging, helpers JSON.
- `visual_effects.py`: Efectos visuales, partículas, gradientes.
- `requirements.txt` / `pyproject.toml`: Todas las dependencias.
- `Data/`: Datos persistentes (perfiles, logs, puntajes).

## Dependencias

- Núcleo: `pygame`, `tomlkit`, `platformdirs`, `mccabe`, `dill`, `colorama`, `astroid`
- Desarrollo: `isort`, `pyinstaller`, `flake8`, `pyflakes`, `pycodestyle`, `pygments`
- Consulta `requirements.txt` y `[tool.poetry.dependencies]` en `pyproject.toml` para la lista completa.

## Workflows de Desarrollo

- **Ejecutar el juego:**
  - `python -m main` (desde la raíz del proyecto)
- **Instalar dependencias:**
  - `pip install -r requirements.txt` o `poetry install`
- **Compilar ejecutable:**
  - `pyinstaller setup.py` o el script `build` de `pyproject.toml`
- **Logging:**
  - Todos los logs van a `Data/logs.txt` y consola (ver `utils.py`)
- **Perfiles y puntajes:**
  - En `Data/profiles.json` y `Data/score/highscore.json`

## Convenciones y Patrones

- Toda la configuración está en `settings.py`.
- Logging centralizado vía singleton en `utils.py` (`_logger_instance`).
- Acceso a datos siempre mediante helpers de `utils.py`.
- Efectos visuales modulares y extensibles en `visual_effects.py`.
- El estado del juego se gestiona en `game.py` y se comunica por objetos compartidos y llamadas a funciones.
- Compatibilidad total con Python 3.13.5+.

## Integración y Extensibilidad

- Para nuevas features (powerups, menús), crea un módulo y enlaza desde `main.py` y/o `game.py`.
- Para nuevas configuraciones, añade en `settings.py` y documenta en el README.
- Para nuevas dependencias, actualiza `requirements.txt` y `pyproject.toml`.

## Licencia

El proyecto usa la Simplified Open License (SOL). Consulta `LICENSE.txt` para detalles.

---

Si eres un agente AI, sigue estas convenciones y consulta los archivos clave para ejemplos de patrones específicos del proyecto. Ante la duda, prioriza configuración explícita y diseño modular.
