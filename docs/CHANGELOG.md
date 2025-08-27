# CHANGELOG

---

> These release notes document the changes, improvements and fixes made to the Snake Game project. Each version follows a semantic scheme to make it easier to understand the changes and their impact on the project. It is recommended to review the notes before updating or contributing to the code to ensure compatibility and follow established best practices.

---

## [1.8.0] - 23-08-2025
	Full audio system: dynamic background music and sound effects for most actions.
	Added splash screen with game logo and loading animation.
	Fixed fullscreen and menu.

## [1.7.0] - 20-08-2025
	Obstacles and new UI components.
	Added obstacles system: collisions, generation and management from obstacles.py.
	New file ui_components.py: reusable components for menus and HUD.
	Visual improvements in the interface and menus using the new UI components.
	Minor bug fixes and stability improvements.

## [1.6.0] - 19-08-2025
	License updated from SOL 2.0 to SOL 3.0
	Centralized and documented configuration in settings.py, access helpers and logging in utils.py.
	Advanced logging: detailed logs of events, errors, profiles and system in Data/logs.txt.
	Full compatibility with Python 3.13.5+ and updated dependencies in requirements.txt and pyproject.toml.
	Development and build workflows documented: run (python -m main), install (pip install -r requirements.txt or poetry install), (pyinstaller setup.py or poetry run build).
	License updated to SOL 3.0, clearer and stronger legal protection.
	Expanded technical and testing documentation in docs/ and the README.
	Improved data structure and persistence: profiles, logs and scores organized in Data/.
	Code refactoring and optimization for better maintainability and performance.
	Minor bug fixes and stability improvements.

## [1.5.0] - 17-08-2025
	License updated from SOL 1.0 to SOL 2.0 (more detailed and comprehensive).
	New `pyproject.toml` with full support for Poetry.
	Improvements in project dependency management.
	Optimized and modernized build scripts.
	Cross-platform testing documentation completed and verified.
	Improved build and distribution system.
	Differentiated management of development and production dependencies.
	Integrated configuration for development tools (linting, formatting).
	Support for modern package managers (Poetry + pip).

## [1.4.0] - 17-08-2025
	Stability and optimization release.
	Consolidation of all previous bug fixes.
	General performance optimization.
	Improved memory management.
	Fixes for interpolation and collision issues.
	Stabilization of the particle system.
	Improvements to the logging system.
	Update to the profile system.
	Fixes for minor memory leaks.
	Improved collision accuracy.
	Optimization of animations and visual effects.

## [1.3.3] - 21-08-2025
	Removal of unused variables.
	Fixes for style issues and naming conventions.
	Improved code readability.
	Logic adjustments to avoid potential runtime errors.

## [1.3.2] - 13-08-2025
	Full logging system in console and file (Data/logs.txt`).
	Automatic logging of game events with timestamps.
	Different logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
	Colored logs in console for better readability.
	Recording of game statistics and user actions.

## [1.3.1] - 13-08-2025
	Bug fixes:
	Black rectangles in snake segments.
	Interpolation issues with wrap-around.
	Minor issues with alpha colors in effects.

## [1.3.0] - 13-08-2025
	Full visual effects system with particles.
	Smooth animations and movement interpolation.
	Screen shake and flash effects for greater impact.
	Snake with gradients, shadows and animated eyes.
	Food and powerups with glow effects and animations.
	Improved background with gradients and subtle grid.
	Modern user interface with shadows and effects.

## [1.2.0] - 13-08-2025
	Bug fixes and performance optimization.
	Collision engine optimization.
	Reduced memory usage.
	Fixes in snake growth logic.

## [1.1.0] - 13-08-2025
	Improvements in profile management and score storage.
	User profile system.
	Persistent storage of high score.
	Minor bug fixes.

## [1.0.0] - 12-08-2025
	Basic game implementation.
	Snake movement and collision detection.
	Food generation and snake growth.
