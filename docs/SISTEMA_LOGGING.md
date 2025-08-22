# 📝 Logging System - Snake Game

## 📋 Summary

A **complete logging system** has been implemented in the Snake game that records events both to the **console** and to a **log file** (`Data/logs.txt`). The system is flexible, configurable, and designed to provide useful information without affecting the game's performance.

## 🎯 **FULLY IMPLEMENTED**

✅ **Log file at `Data/logs.txt`**
✅ **Colored console logs**
✅ **Configurable logging levels**
✅ **Automatic game event logging**
✅ **Timestamps and structured format**
✅ **Thread-safe for concurrency**
✅ **Session system**

## 📁 **Log File Location**

```
./Data/logs.txt
```

The file is created automatically the first time the game runs.

## 🛠️ **Technical Implementation**

### **Main File: `utils.py`**
`utils.py` has been expanded with a full logging system that includes:

```python
# Niveles de logging disponibles
DEBUG    # Información detallada para desarrollo
INFO     # Información general del juego
WARNING  # Advertencias y situaciones inusuales
ERROR    # Errores no críticos
CRITICAL # Errores críticos que pueden afectar el juego
```

### **Automatic Configuration**
- **Console**: Shows only INFO and above (with colors)
- **File**: Records EVERYTHING (DEBUG and above)
- **Thread-safe**: Safe for concurrent use
- **Timestamps**: HH:MM:SS format for easy reading

## 🎮 **Automatically Logged Events**

### **🚀 System & Startup**
- Game start and Python version
- Loading of menus and screen configuration
- Profile initialization

### **👤 User Actions**
- Navigation between menus (Play, Profiles, Options)
- Starting new games
- Applied settings

### **🎯 Game Events**
- Game resets
- Food consumed (with points and new speed)
- Powerups collected (specific type)
- New high scores achieved
- Game over (with statistics)
- Number of games played

### **📊 Real Log Examples**

```
============================================================
🐍 SNAKE GAME - NEW SESSION STARTED
📅 2025-08-13 12:29:58
============================================================
[12:29:58] INFO     [SYS] 🖥️ Iniciando Snake Game
[12:29:58] INFO     [SYS] 🖥️ Python version: 3.13.5
[12:31:02] INFO     [GAME] 🎮 Iniciando nueva partida - Perfil: New
[12:31:02] INFO      Configuraciones - Wrap: True, Obstáculos: False, Velocidad: 120ms
[12:31:04] INFO     [GAME] 🎮 Comida consumida - Puntos: 1, Nueva velocidad: 114ms
[12:31:14] INFO     [GAME] 🎮 Powerup recogido - Tipo: slow
[12:32:04] INFO     [GAME] 🎮 ¡NUEVO RECORD! - Puntuación final: 10 (anterior: 0)
[12:32:04] INFO      Partidas jugadas: 1
```

> **Note:** The above example log block is shown as-is (preserved from the original) to illustrate format and content.

## 🎨 **Colored Console Logs**

- 🔵 **DEBUG**: Cyan — Detailed technical information
- 🟢 **INFO**: Green — General game information
- 🟡 **WARNING**: Yellow — Unusual situations
- 🔴 **ERROR**: Red — Non-critical errors
- 🟣 **CRITICAL**: Magenta — Critical errors

## 📈 **Specific Functions Implemented**

### **Convenience Functions**
```python
utils.log_info("Mensaje general")
utils.log_warning("Advertencia")
utils.log_error("Error ocurrido")

# Funciones especializadas
utils.log_game_event("Evento", "Detalles opcionales")
utils.log_user_action("Acción del usuario")
utils.log_system_info("Información del sistema")
utils.log_visual_effect("Efecto", "Detalles")
utils.log_performance("Acción", duracion_ms)
```

### **Session Control**
```python
utils.close_logging_session()  # Cierra la sesión correctamente
```

## 🔧 **Available Configurations**

### **Log Levels per Destination**
```python
# En utils.py - Logger class
min_console_level = LogLevel.INFO    # Solo INFO y superiores en consola
min_file_level = LogLevel.DEBUG      # Todo en archivo
```

### **Enable/Disable Destinations**
```python
console_enabled = True   # Mostrar en consola
file_enabled = True      # Escribir en archivo
```

## 🎯 **Code Integration**

### **main.py**
- System startup logging
- Python version info
- Critical error handling
- Clean session shutdown

### **menu.py**
- Menu navigation logging
- Game start logging
- Applied configurations

### **logic.py**
- Game events (food, powerups, records)
- Game resets
- Profile statistics

### **game.py**
- Visual effects (optional)
- Performance information

## 📊 **Recorded Information**

### **For each event we log:**
- ⏰ **Exact timestamp** (HH:MM:SS)
- 🏷️ **Log level** (INFO, WARNING, etc.)
- 📂 **Module** where it occurred ([GAME], [USER], [SYS])
- 🎯 **Main event**
- 📝 **Specific details** when relevant

### **System Information:**
- Python version used
- Configured screen resolution
- Applied game settings

### **Game Statistics:**
- Current score and records
- Game speed (delay in ms)
- Types of powerups collected
- Total number of games played

## 🚀 **Benefits of the System**

### **For Development:**
- **Easy debugging**: All needed information in one place
- **Event tracking**: Full session history
- **Issue detection**: Automatic error logging

### **For the Player:**
- **Non-intrusive**: Only relevant info in console
- **Complete history**: File with full activity log
- **Performance**: Optimized system with no FPS impact

### **For Maintenance:**
- **Usage analysis**: Recorded gameplay patterns
- **Statistics**: Performance information
- **Troubleshooting**: Complete history to resolve issues

## ✅ **Final Status**

**LOGGING SYSTEM FULLY IMPLEMENTED AND OPERATIONAL**

- ✅ `Data/logs.txt` file created automatically
- ✅ Console logs with general information and colors
- ✅ Automatic recording of important game events
- ✅ Thread-safe system optimized for performance
- ✅ Flexible and extensible configuration
- ✅ Full integration across main modules

The logging system is fully implemented and working perfectly! 📝✨
