# 🐍 Snake Game Version 1.8.1

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green)
![License](https://img.shields.io/badge/license-SOL%203.0-orange)
![Status](https://img.shields.io/badge/status-stable-success)
![Version](https://img.shields.io/badge/version-1.8.1-brightgreen)

> **Snake, modular, cross-platform with advanced visual effects, persistent profiles and developer workflows.**

---

## 🎯 Key Features

**Key Features**

- 🎨 Modern visual effects: particle system, gradients, smooth transitions, shadows, animated elements
- 🐍 Advanced snake rendering: gradient body, dynamic shadows, animated eyes, smooth movement
- 🍎 Dynamic food & powerups: multiple shapes, animated effects, powerup system
- 🌅 Customizable backgrounds: gradient fills, grid overlays, volumetric obstacles
- 📝 Robust logging: console and file output, log levels, colorized logs ([details](./docs/SISTEMA_LOGGING.md))
- 👤 Persistent multi-user profiles: per-user data, high scores, stored in `Data/profiles/`
- ⚙️ Centralized configuration: all settings in `settings.py`, easy customization
- 🖥️ Cross-platform: Windows, Linux, macOS support
- 🔧 Developer workflows: run, install, build, logging, and packaging documented
- 📄 Technical documentation: inline comments, guides, and examples
- 📦 Ready for distribution: build scripts, packaging, release management
- 🔍 Performance tools: metrics, analysis utilities
- 🛠️ Maintenance: helper scripts, support tools, automated tasks

---

### Logs & data

- Logs: `Data/logs.txt`
- Profiles: `Data/profiles/`
- Audio: `Data/assets/audio/`
- Assets & Icons: `Data/assets/`

---

## 🗂️ Project Structure

```text
snake/
├── __main__.py                    # Entry point
├── src/                           # Source code
│   └── snake/                     # Main package
│       ├── __init__.py
│       ├── main.py                # Main loop and orchestration
│       ├── core/                  # Core game logic
│       │   ├── __init__.py
│       │   ├── game.py            # Game controller and state
│       │   ├── snake.py           # Snake logic
│       │   ├── food.py            # Food and powerups
│       │   └── logic.py           # Helper functions
│       ├── modules/               # Game modules
│       │   ├── __init__.py
│       │   ├── menu.py            # Menus and navigation
│       │   ├── profiles.py        # Profile and score management
│       │   ├── visual_effects.py  # Visual effects and particle system
│       │   ├── obstacles.py       # Obstacle logic and rendering
│       │   └── ui_components.py   # UI components and widgets
│       └── system/                # System utilities
│           ├── __init__.py
│           ├── settings.py        # Centralized configuration
│           ├── utils.py           # Utilities and logging
│           ├── video_config.py    # Automatic SDL configuration
│           └── audio_manager.py   # Audio system management
├── scripts/                       # Build and utility scripts
│   └── build.py                   # Build script
├── Data/                          # Profiles, logs, persisted data
│   ├── assets/                    # Game assets
│   ├── profiles/                  # User profiles
│   └── logs.txt                   # Game logs
├── docs/                          # Technical documentation
├── requirements.txt               # Dependencies
├── pyproject.toml                 # Poetry / build config
└── pyrightconfig.json             # Type checking config
```

---

## ⚙️ Configuration & Customization

- All options are in `settings.py` (controls, visuals, gameplay)
- Drivers and SDL optimizations in `video_config.py`
- Profiles and scores: `Data/profiles/` (one profile name per user)
- Logging configurable: levels, file, console, warnings, errors
- Assets & Icons: `Data/assets/`
- Audio: `Data/assets/audio/`

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

## [1.8.1] - 27-08-2025

- Fixed bugs related to fullscreen and menu navigation
- Fixed bugs related to music and audio playback
- Improved input handling for smoother gameplay
- Enhanced overall game performance
- Fixed splash screen background color issue.
- Changed splash screen background from blue-gray to black for better visual consistency.
- And new structure for the project.

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

- 🍎 Food: +1
- ⚡ Speed Powerup: +1 and increases speed
- 🔷 Grow Powerup: +5 and increases length
- ⭐ Score Powerup: +20
- 🔵 Slow Powerup: +1 and slows the game

---

## 📋 System Requirements

### Minimum Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows 10+, Linux (Ubuntu 20.04+), macOS 10.14+
- **RAM**: 512 MB available
- **Disk Space**: 124 MB

> [!NOTE]
> These requirements refer to the currently published release or in your already compiled version.
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
python -m __main__
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

## Build to Executable (Optional)

To produce a standalone executable:

### Run the build script

```bash
poetry run build
```

```bash
# The executable will be in:
#   dist/Snake Game.exe    (Windows)
#   dist/Snake Game        (Linux/macOS)
```

> [!NOTE]
> If you need runtime options that exist only in the script (and aren’t packaged into the executable), run the script directly. If you want those options available in the built executable, add them to your build process or pass them through your packaging tool.
> [!WARNING]
> If you want to reduce the executable size, use UPX. Install it globally or place it in `lib/upx.exe`. (UPX may not work reliably on some Linux/macOS environments; it is recommended for Windows builds.)

---

### 🔍 Troubleshooting

If you run into issues:

1. **Check logs:** `Data/logs.txt` contains detailed info
2. **Force driver:** `export SDL_VIDEODRIVER=<driver>`
3. **Verify pygame:** Logs indicate whether pygame is available
4. **Try fallbacks:** The system will attempt multiple drivers automatically
5. **Update dependencies:** Ensure all packages are up to date
6. **Check system requirements:** Verify that your system meets the minimum requirements
7. **Seek help:** If you're still having issues, consider reaching out for help

---

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

---

## 📞 Future Improvements

### Version 1.8.2 - Released

- Add MVC

- 🛠️ **Configuration**
  - Add support for external configuration files
  - Allow loading configs from `./Data/configuration.json`
  - Validate and apply configs at runtime
  - Document available configuration options
  - Add an external app for config management
  - Automatic recorder that spits out GIFs upon breaking a record.
  - "Seed codes": Share a level seed + compact replay (list of inputs) for asynchronous challenges.

### Concept Version

- 🎆 **Additional Game Modes**
  - Time trial
  - Arcade mode
  - & update actual game modes
  - Survival Elements: Transform the game into a survival experience. The snake has an energy bar that depletes over time and can only be recharged by eating. Different types of "food" will be introduced, some nutritious and others poisonous.

- 👥 **Multiplayer Mode**
  - Local split-screen

- 🔧 **Global Translation**
  - Translation of comments, logs, game menus...
  - JSON files with translations under `./Data/lang`
  - Multi-language support

---

### ❓ Quick FAQ

- Does it work offline? **Yes**
- Where are my scores? `Data/profiles/`
- Can I modify graphics? Yes — see `settings.py` and `visual_effects.py`
- Compile for distribution? Yes — use `build.py` or `poetry run build`
- Logs? In `Data/logs.txt`
- How to run the game? `python __main__.py` or `poetry run start`

---

### 📄 License

**Simplified Open License (SOL)**

Free to use for any purpose (personal, educational, commercial). Modification and distribution allowed with attribution. Commercial use permitted. Trademark and patent protections apply. No warranty — use at your own risk. Indemnification required by the user.

See the [`LICENSE.txt`](LICENSE.txt) file for full details.

---

### 📄 Third-party Licenses

This project uses third-party components.
To view third-party licenses, check the [`THIRD-PARTY-LICENSES.md`](./docs/THIRD-PARTY-LICENSES.md) file.

---

**🐍 Made with ❤️ by [ParaDevOne](https://github.com/ParaDevOne)**

*If you like this project, please give it a ⭐ on GitHub!*
