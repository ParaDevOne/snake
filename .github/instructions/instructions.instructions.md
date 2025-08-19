---
applyTo: "**"
---

## Project Context

This repository is a modular, advanced version of the classic Snake game in Python. The architecture is designed for clarity, extensibility, and maintainability, with modern visual effects and persistent data management.

### Key Structure

- `main.py`: Entry point, main loop, component orchestration
- `game.py`: Game state and controller
- `snake.py`: Snake logic and movement
- `food.py`: Food and powerups
- `menu.py`: Menus (if present)
- `logic.py`: Helper logic functions
- `settings.py`: Centralized configuration
- `profiles.py`: Profile and score management
- `utils.py`: Utilities, logging, JSON helpers
- `visual_effects.py`: Visual effects, particles, gradients
- `requirements.txt` / `pyproject.toml`: All dependencies
- `Data/`: Persistent data (profiles, logs, scores)

### Coding Guidelines for AI

- Always use helpers from `utils.py` for file/data access and logging
- All configuration must go through `settings.py`
- Visual effects should be modular and placed in `visual_effects.py`
- Game state is managed in `game.py` and communicated via objects/functions
- Use Python 3.13.5+ features and syntax
- For new features, create a new module and integrate via `main.py`/`game.py`
- Update both `requirements.txt` and `pyproject.toml` for new dependencies
- Follow the patterns and conventions shown in the main modules

### Developer Workflows

- Run: `python -m main`
- Install: `pip install -r requirements.txt` or `poetry install`
- Build: `pyinstaller setup.py` or `poetry run build`
- Logs: `Data/logs.txt` and console (see `utils.py`)
- Profiles/scores: `Data/profiles.json`, `Data/score/highscore.json`

### License

This project uses the Simplified Open License (SOL). See `LICENSE.txt` for details.
