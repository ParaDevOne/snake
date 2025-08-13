# 📝 Sistema de Logging - Snake Game

## 📋 Resumen

Se ha implementado un **sistema completo de logging** en el juego Snake que registra eventos tanto en **consola** como en un **archivo de logs** (`Data/logs.txt`). El sistema es flexible, configurable y está diseñado para proporcionar información útil sin afectar el rendimiento del juego.

## 🎯 **IMPLEMENTADO COMPLETAMENTE**

✅ **Archivo de logs en `Data/logs.txt`**  
✅ **Logs en consola con colores**  
✅ **Niveles configurables de logging**  
✅ **Logs automáticos de eventos del juego**  
✅ **Timestamps y formato estructurado**  
✅ **Thread-safe para concurrencia**  
✅ **Sistema de sesiones**  

## 📁 **Ubicación del Archivo de Logs**

```
C:\Users\Usuario\Desktop\snake\Data\logs.txt
```

El archivo se crea automáticamente la primera vez que se ejecuta el juego.

## 🛠️ **Implementación Técnica**

### **Archivo Principal: `utils.py`**
Se ha expandido `utils.py` con un sistema completo de logging que incluye:

```python
# Niveles de logging disponibles
DEBUG    # Información detallada para desarrollo
INFO     # Información general del juego  
WARNING  # Advertencias y situaciones inusuales
ERROR    # Errores no críticos
CRITICAL # Errores críticos que pueden afectar el juego
```

### **Configuración Automática**
- **Consola**: Solo muestra INFO y superiores (con colores)
- **Archivo**: Registra TODO (DEBUG y superiores)
- **Thread-safe**: Seguro para uso concurrente
- **Timestamps**: Formato HH:MM:SS para fácil lectura

## 🎮 **Eventos Registrados Automáticamente**

### **🚀 Sistema y Inicio**
- Inicio del juego y versión de Python
- Carga de menús y configuración de pantalla
- Inicialización de perfiles

### **👤 Acciones del Usuario**
- Navegación entre menús (Jugar, Perfiles, Opciones)
- Inicio de nuevas partidas
- Configuraciones aplicadas

### **🎯 Eventos del Juego**
- Reinicio de juegos
- Comida consumida (con puntos y nueva velocidad)
- Powerups recogidos (tipo específico)
- Nuevos records conseguidos
- Fin del juego (con estadísticas)
- Número de partidas jugadas

### **📊 Ejemplos de Logs Reales**

```
============================================================
🐍 SNAKE GAME - NUEVA SESIÓN INICIADA
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

## 🎨 **Logs con Colores en Consola**

- 🔵 **DEBUG**: Cian - Información técnica detallada
- 🟢 **INFO**: Verde - Información general del juego
- 🟡 **WARNING**: Amarillo - Situaciones inusuales
- 🔴 **ERROR**: Rojo - Errores no críticos  
- 🟣 **CRITICAL**: Magenta - Errores críticos

## 📈 **Funciones Específicas Implementadas**

### **Funciones de Conveniencia**
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

### **Control de Sesiones**
```python
utils.close_logging_session()  # Cierra la sesión correctamente
```

## 🔧 **Configuraciones Disponibles**

### **Niveles de Log por Destino**
```python
# En utils.py - Logger class
min_console_level = LogLevel.INFO    # Solo INFO y superiores en consola
min_file_level = LogLevel.DEBUG      # Todo en archivo
```

### **Activar/Desactivar Destinos**
```python
console_enabled = True   # Mostrar en consola
file_enabled = True      # Escribir en archivo
```

## 🎯 **Integración en el Código**

### **main.py**
- Log de inicio del sistema
- Información de versión de Python
- Manejo de errores críticos
- Cierre limpio de sesión

### **menu.py**
- Navegación entre menús
- Inicio de partidas
- Configuraciones aplicadas

### **logic.py**
- Eventos de juego (comida, powerups, records)
- Reinicio de partidas
- Estadísticas de perfil

### **game.py**
- Efectos visuales (opcionalmente)
- Información de rendimiento

## 📊 **Información Registrada**

### **Para cada evento se registra:**
- ⏰ **Timestamp** exacto (HH:MM:SS)
- 🏷️ **Nivel** de log (INFO, WARNING, etc.)
- 📂 **Módulo** donde ocurrió ([GAME], [USER], [SYS])
- 🎯 **Evento** principal
- 📝 **Detalles** específicos cuando son relevantes

### **Información del Sistema:**
- Versión de Python utilizada
- Resolución de pantalla configurada
- Configuraciones de juego aplicadas

### **Estadísticas de Juego:**
- Puntuación actual y récords
- Velocidad del juego (delay en ms)
- Tipos de powerups recogidos
- Número total de partidas jugadas

## 🚀 **Beneficios del Sistema**

### **Para Desarrollo:**
- **Debug fácil**: Toda la información necesaria en un lugar
- **Seguimiento de eventos**: Historia completa de cada sesión
- **Detección de problemas**: Logs automáticos de errores

### **Para el Usuario:**
- **No intrusivo**: Solo información relevante en consola
- **Histórico completo**: Archivo con toda la actividad
- **Rendimiento**: Sistema optimizado sin impacto en FPS

### **Para Mantenimiento:**
- **Análisis de uso**: Patrones de juego registrados
- **Estadísticas**: Información sobre rendimiento
- **Troubleshooting**: Historia completa para resolver problemas

## 📋 **Ejemplo de Sesión Completa**

```
============================================================
🐍 SNAKE GAME - NUEVA SESIÓN INICIADA
📅 2025-08-13 12:29:58
============================================================
[12:29:58] INFO     [SYS] 🖥️ Iniciando Snake Game
[12:29:58] INFO     [SYS] 🖥️ Python version: 3.13.5
[12:29:58] INFO      Iniciando juego con menú principal
[12:29:58] INFO      Iniciando sistema de menús
[12:29:58] INFO     [SYS] 🖥️ Resolución: 800x600
[12:30:34] INFO     [USER] 👤 Navegó a sección JUGAR
[12:31:02] INFO     [GAME] 🎮 Iniciando nueva partida - Perfil: New
[12:31:02] INFO      Configuraciones - Wrap: True, Obstáculos: False, Velocidad: 120ms
[12:31:02] INFO     [GAME] 🎮 Reiniciando juego
[12:31:04] INFO     [GAME] 🎮 Comida consumida - Puntos: 1, Nueva velocidad: 114ms
[12:31:14] INFO     [GAME] 🎮 Powerup recogido - Tipo: slow
[12:32:04] INFO     [GAME] 🎮 ¡NUEVO RECORD! - Puntuación final: 10 (anterior: 0)
[12:32:04] INFO      Partidas jugadas: 1

📅 SESIÓN TERMINADA: 2025-08-13 12:32:15
============================================================
```

## ✅ **Estado Final**

**SISTEMA DE LOGGING COMPLETAMENTE IMPLEMENTADO Y FUNCIONAL**

- ✅ Archivo `Data/logs.txt` creado automáticamente
- ✅ Logs en consola con información general y colores
- ✅ Registro automático de eventos importantes del juego
- ✅ Sistema thread-safe y optimizado para rendimiento
- ✅ Configuración flexible y expandible
- ✅ Integración completa en todos los módulos principales

¡El sistema de logging está completamente implementado y funcionando perfectamente! 📝✨
