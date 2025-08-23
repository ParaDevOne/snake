

# Copilot Instructions for Snake Game

## Overview

This project is an advanced and modular version of the classic Snake game in Python. The architecture is designed to be clear, extensible, and easy to maintain, featuring modern visual effects and persistent data management.

## Project Structure

- `main.py`: Entry point, main loop, and component orchestration.
- `game.py`: Game controller and state management.
- `snake.py`: Snake logic and movement.
- `food.py`: Food and powerups logic.
- `menu.py`: Menu system (if present).
- `logic.py`: Helper logic functions and utilities.
- `settings.py`: Centralized configuration (controls, visuals, gameplay).
- `profiles.py`: Profile and score management.
- `utils.py`: Utilities, logging system, JSON helpers.
- `visual_effects.py`: Visual effects, particles, gradients.
- `requirements.txt` / `pyproject.toml`: All dependencies.
- `Data/`: Persistent data (profiles, logs, scores).

## Dependencies

- Core: `pygame`, `tomlkit`, `platformdirs`, `mccabe`, `dill`, `colorama`, `astroid`
- Development: `isort`, `pyinstaller`, `flake8`, `pyflakes`, `pycodestyle`, `pygments`
- See `requirements.txt` and `[tool.poetry.dependencies]` in `pyproject.toml` for the full list.

## Development Workflows

- **Run the game:**
  `python -m main` (from the project root)
- **Install dependencies:**
  `pip install -r requirements.txt` or `poetry install`
- **Build executable:**
  `pyinstaller setup.py` or the `build` script in `pyproject.toml`
- **Logging:**
  All logs go to `Data/logs.txt` and console (see `utils.py`)
- **Profiles and scores:**
  Stored in `Data/profiles.json` and `Data/score/highscore.json`

## Conventions and Patterns

- All configuration is in `settings.py`.
- Centralized logging via singleton in `utils.py` (`_logger_instance`).
- Data access always through helpers in `utils.py`.
- Modular and extensible visual effects in `visual_effects.py`.
- Game state managed in `game.py` and communicated via objects and functions.
- Full compatibility with Python 3.13.5+.

## Integration and Extensibility

- For new features (powerups, menus), create a module and link it from `main.py` and/or `game.py`.
- For new configurations, add them to `settings.py` and document in the README.
- For new dependencies, update both `requirements.txt` and `pyproject.toml`.

## License

This project uses the Simplified Open License (SOL). See `LICENSE.txt` for details.

---

**Nota para agentes AI:**
Sigue estas convenciones y consulta los archivos clave para ejemplos de patrones específicos. Prioriza configuración explícita y diseño modular. Ante cualquier duda, revisa la documentación y los módulos principales.
