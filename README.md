# 🐍 Snake Game Version 1.7.0

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green)
![License](https://img.shields.io/badge/license-SOL%203.0-orange)
![Status](https://img.shields.io/badge/status-stable-success)
![Version](https://img.shields.io/badge/version-1.7.0-brightgreen)

> **Snake — modular, cross-platform with advanced visual effects, persistent profiles and developer workflows.**

---

## 🎯 Key Features

- 🎨 Advanced visual effects: particles, gradients, smooth animations
- 🐍 Enhanced snake: gradients, shadows, animated eyes
- 🍎 Dynamic food & powerups: shapes, animations, effects
- 🌅 Backgrounds: gradients, grid, volumetric obstacles
- 📝 Logging: console + file, levels, colors [More info](./docs/SISTEMA_LOGGING.md)
- 👤 Persistent profiles: multi-user, stored under `Data/profiles/`
- ⚙️ Centralized configuration: everything in `settings.py`
- 🖥️ Cross-platform support: Windows, Linux, macOS
- 🔧 Workflows: run, install, build and logs documented
- 📄 Technical docs: inline comments, guides and examples
- 📦 Distribution: packaging and release-ready distribution
- 🔍 Performance analysis: tools and metrics
- 🛠️ Maintenance: helper scripts and support tools

---

### Logs & data
- Logs: `Data/logs.txt`
- Profiles: `Data/profiles/`

---

## 🗂️ Project Structure

```
snake/
├── main.py           # Main loop and orchestration
├── game.py           # Game controller and state
├── snake.py          # Snake logic
├── food.py           # Food and powerups
├── menu.py           # Menus and navigation
├── logic.py          # Helper functions
├── settings.py       # Centralized configuration
├── profiles.py       # Profile and score management
├── utils.py          # Utilities and logging
├── visual_effects.py # Visual effects and particle system
├── video_config.py   # Automatic SDL configuration
├── requirements.txt  # Dependencies
├── pyproject.toml    # Poetry / build config
├── setup.py          # PyInstaller build script
├── Data/             # Profiles, logs, persisted data
└── docs/             # Technical documentation
```

---

## ⚙️ Configuration & Customization

- All options are in `settings.py` (controls, visuals, gameplay)
- Drivers and SDL optimizations in `video_config.py`
- Profiles and scores: `Data/profiles/` (one profile name per user)
- Logging configurable: levels, file, console

Example configuration:

```python
OBSTACLES = True
WRAP_AROUND = True
POWERUPS_ENABLED = True
SMOOTH_MOVEMENT = True
LOG_LEVEL = "INFO"
LOG_TO_FILE = True
LOG_TO_CONSOLE = True
```

---

## 📝 Versions & Changes

## [1.7.0] - 2025-08-21
- Obstacles and new UI components.
	- Added obstacles system: collisions, generation and management in `obstacles.py`.
	- New file `ui_components.py`: reusable components for menus and HUD.
	- Visual improvements in the interface and menus using the new UI components.
	- Minor bug fixes and stability improvements.

> [!NOTE]
> **Previous releases can be found in the [`CHANGELOG.md`](./docs/CHANGELOG.md) file.**

---

## 👾 How to Play

- **Move:** ↑ ↓ ← → or WASD
- **Pause:** ESC or SPACE
- **Restart:** R
- **Menus:** ENTER to select, TAB to switch profile
- **Fullscreen:** F11

### Objective
Eat as much food as possible without colliding with yourself or obstacles (or the walls if wrap-around mode is disabled).

### Scoring
- 🍎 Food: +10
- ⚡ Speed Powerup: +1 and increases speed
- 🔷 Grow Powerup: +5 and increases length
- ⭐ Score Powerup: +50
- 🔵 Slow Powerup: +10 and slows the game

---

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.10 or higher
- **Operating System**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM**: 512 MB available
- **Disk Space**: 64 MB

> [!NOTE]
> These requirements refer to the currently published release.
>
>
> This README lists **Python 3.10**, but the [`pyproject.toml`](./pyproject.toml) file specifies **3.13.5**, that is because `PyInstaller` requires version **3.13.5** to build correctly.

---

## 🚀 Installation

### Quick Install

```bash
# 1. Clone the repository
git clone https://github.com/ParaDevOne/snake.git
cd snake

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the game
python -m main
```

### Step-by-step Installation

#### 1. **Clone the repository**
```bash
git clone https://github.com/ParaDevOne/snake.git
cd snake
```

#### 2. **Create a virtual environment (recommended)**
```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\activate.ps1

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Install with Poetry (Recommended)

If you prefer Poetry for dependency management:

```bash
# 1. Install Poetry (if you don't have it)
curl -sSL https://install.python-poetry.org | python3 -

# 2. Clone the repository
git clone https://github.com/ParaDevOne/snake.git
cd snake

# 3. Install dependencies with Poetry
poetry install

# 4. Run the game
poetry run start
```

# Build to Executable (Optional)

To produce a standalone executable:

### Run the build script

#### With bash
```
python setup.py
```

#### With Poetry (bash)
```bash
# Run the build script
poetry run build
```

```bash
# The executable will be in:
#   dist/Snake Game.exe    (Windows)
#   dist/Snake Game        (Linux/macOS)
```

> [!WARNING]
> If you want to reduce the executable size, use UPX. Install it globally or place it in `lib/upx.exe`. (UPX may not work reliably on some Linux/macOS environments; it is recommended for Windows builds.)

## 🎮 Running

### Normal mode
```bash
python -m main
```

### 🔍 Troubleshooting

If you run into issues:

1. **Check logs:** `Data/logs.txt` contains detailed info
2. **Force driver:** `export SDL_VIDEODRIVER=<driver>`
3. **Verify pygame:** Logs indicate whether pygame is available
4. **Try fallbacks:** The system will attempt multiple drivers automatically

## 🛠️ Development & Architecture

### Technologies Used
- **Python 3.10+**: Primary language
- **Pygame 2.6.1**: Game engine and rendering
- **SDL**: Low-level system for graphics and audio
- **JSON**: Profile data storage
- **Logging**: Python native logging system

### Architectural Pattern
- **MVC (Model-View-Controller)**: Clear separation of concerns
- **Component System**: Modular visual effects
- **Event-Driven**: Pygame event-based handling
- **Configuration-First**: Centralized configuration

## 👥 Contributions

Contributions are welcome! This project follows an open development model.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Commit your changes**: `git commit -m 'Add new feature'`
4. **Push the branch**: `git push origin feature-new-feature`
5. **Open a Pull Request**

### Contribution Types

#### Types of contributions
- 🐛 **Bug Fixes**: Fix bugs
- ✨ **Features**: New features
- 🎨 **Graphics**: Visual improvements
- 📄 **Documentation**: Docs and guides
- ⚡ **Performance**: Optimizations
- 🔧 **Refactoring**: Code structure improvements

### Areas That Need Contributions
- 🌍 **Localization**: Translations to other languages
- 🚀 **Optimization**: Performance improvements
- 🎨 **Art**: Better sprites and textures
- 📁 **Documentation**: Guides and tutorials
- 🧪 **Testing**: More automated tests

## 📞 Future Improvements

### Version - 1.8
- 🎵 **Full Audio System**
  - Dynamic background music
  - Sound effects for most actions

### Planned Version
- 🛠️ **Configuration**
  - JSON files with translations under `./Data/lang`
  - Fix fullscreen and menu issues

- 🔧 **Global Translation**
  - Translation of comments, logs, game menus ...
  - Multi-language support

### Concept Version
- 👥 **Multiplayer Mode**
  - Local split-screen

- 🎆 **Additional Game Modes**
  - Time trial
  - Arcade mode

- **Config**
  - Add support for external config files
  - Allow loading configs from `./Data/config.json`
  - Validate and apply configs at runtime
  - Document available configuration options
  - Add an external app for config management

## 🛠️ Development

---

### ❓ Quick FAQ

- Does it work offline? **Yes**
- Where are my scores? `Data/profiles/`
- Can I modify graphics? Yes — see `settings.py` and `visual_effects.py`
- Compile for distribution? Yes — use `setup.py` or `poetry run build`
- Logs? In `Data/logs.txt`

---

### 📄 License

**Simplified Open License (SOL) v3.0**

Free to use for any purpose (personal, educational, commercial). Modification and distribution allowed with attribution. Commercial use permitted. Trademark and patent protections apply. No warranty — use at your own risk. Indemnification required by the user.

See the [`LICENSE.txt`](LICENSE.txt) file for full details.

---

### 📄 Third-party Licenses

This project uses third-party components.
To view third-party licenses, check the [`THIRD-PARTY-LICENSES.md`](./docs/THIRD-PARTY-LICENSES.md) file.

**🐍 Made with ❤️ by [ParaDevOne](https://github.com/ParaDevOne)**

*If you like this project, please give it a ⭐ on GitHub!*
