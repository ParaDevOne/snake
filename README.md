# 🐍 Snake Game - Versión 1.5

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green)
![License](https://img.shields.io/badge/license-SOL%202.0-orange)
![Status](https://img.shields.io/badge/status-stable-success)
![Version](https://img.shields.io/badge/version-1.5.0-brightgreen)

**Una implementación moderna del clásico juego Snake con efectos visuales avanzados, sistema de logging completo y soporte multiplataforma.**

## 🎯 Características Principales

- 🎨 **Efectos Visuales Avanzados**: Sistema completo de partículas, animaciones suaves y gradientes
- 🐍 **Serpiente Mejorada**: Con gradientes, sombras, ojos animados y efectos de brillo
- 🍎 **Comida y Powerups Dinámicos**: Formas únicas, animaciones pulsantes y efectos rotativos
- 🌅 **Ambiente Visual Moderno**: Fondos con gradientes, grid sutil y obstáculos volumétricos
- 📝 **Sistema de Logging Completo**: Logs en consola y archivo con diferentes niveles
- 🖥️ **Soporte Multiplataforma**: Configuración automática SDL para Windows, Linux y macOS
- 👤 **Gestión de Perfiles**: Sistema persistente de puntajes y configuraciones
- ⚙️ **Altamente Configurable**: Todas las opciones modificables desde `settings.py`

## 📁 Estructura del Proyecto

```
snake/
├── 🎮 Núcleo del Juego
│   ├── main.py              # Punto de entrada principal
│   ├── game.py              # Controlador principal del juego
│   ├── snake.py             # Lógica de la serpiente
│   ├── food.py              # Lógica de comida y powerups
│   ├── menu.py              # Sistema de menús
│   └── logic.py             # Funciones auxiliares de lógica
│
├── 🎨 Sistema Visual
│   └── visual_effects.py    # Sistema completo de efectos visuales
│
├── 🔧 Configuración
│   ├── settings.py          # Configuración del juego
│   ├── video_config.py      # Configuración automática SDL
│   ├── profiles.py          # Gestión de perfiles de usuario
│   └── utils.py             # Utilidades generales
│
├── 🧪 Desarrollo
│   ├── setup.py                # Script de compilación PyInstaller
│   ├── pyproject.toml          # Configuración del proyecto (Poetry/Build)
│   └── requirements.txt        # Dependencias del proyecto
│
├── 📚 Documentación
│   ├── README.md              # Este archivo
│   ├── LICENSE.txt            # Licencia SOL 3.0
│   └── docs/                  # Documentación técnica
│
└── 📊 Datos del Juego
    └── Data/
        ├── profiles.json      # Perfiles de usuario (generado)
        └── logs.txt          # Archivo de logs (generado)
```

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.10 o superior
- **Sistema Operativo**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM**: 512 MB disponible
- **Espacio en Disco**: 64 MB

> [!NOTE]
> Aqui pone **Python 3.10** pero en el archivo [pyproject.toml](pyproject.toml) **pone 3.13.5**,
> eso es porque `Pyinstaller` necesita la version **3.13.5** para funcionar.

### Dependencias Python
Todas las dependencias están especificadas en `requirements.txt`:

```txt
Ejemplo: pygame==2.6.1
```

## 🚀 Instalación

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/ParaDevOne/snake.git
cd snake

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el juego
python -m main
```

### Instalación Paso a Paso

#### 1. **Clonar el Repositorio**
```bash
git clone https://github.com/ParaDevOne/snake.git
cd snake
```

#### 2. **Crear Entorno Virtual (Recomendado)**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. **Instalar Dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Instalación con Poetry (Recomendado)

Si prefieres usar Poetry para un mejor manejo de dependencias:

```bash
# 1. Instalar Poetry (si no lo tienes)
curl -sSL https://install.python-poetry.org | python3 -

# 2. Clonar el repositorio
git clone https://github.com/ParaDevOne/snake.git
cd snake

# 3. Instalar dependencias con Poetry
poetry install

# 4. Ejecutar el juego
poetry run python -m main
```

### Compilación a Ejecutable (Opcional)

Para crear un ejecutable independiente:

# Ejecutar script de compilación
```
#### Con bash
python setup.py
```
```

#### Con Poetry:
```bash

# Ejecutar script de compilación
poetry run build
```

```bash
# El ejecutable estará en dist/SnakeGame.exe (Windows) o dist/SnakeGame (Linux/macOS)
```

> [!WARNING]
> Si quieres que el tamaño del ejecutable se reduzca usa UPX,
> instalalo de forma global o en lib/upx.exe.
> (Puede que en entorno Linux/MacOS no funcione bien esta herramienta)

## 🎮 Ejecución

### Modo Normal
```bash
python -m main
```

### Opciones de Línea de Comandos
```bash
# Ejecutar con logging en modo DEBUG
python -m main --debug
```

## ⚙️ Configuración y Personalización

### Archivo de Configuración Principal

Modifica `settings.py` para personalizar:

```python
# Configuración de juego
OBSTACULES = True              # Velocidad del juego (1-20)
WRAP_AROUND = True          # Permitir atravesar paredes
POWERUPS_ENABLED = True     # Habilitar power-ups

# Configuración visual
PARTICLE_COUNT = 20         # Número de partículas en explosiones
SCREEN_SHAKE_INTENSITY = 5  # Intensidad del screen shake
SMOOTH_MOVEMENT = True      # Animaciones suaves

# Configuración de logging
LOG_LEVEL = "INFO"          # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE = True          # Guardar logs en archivo
LOG_TO_CONSOLE = True       # Mostrar logs en consola
```

### Configuración Avanzada de Video

Modifica `video_config.py` para personalizar drivers SDL:

```python
# Drivers por plataforma
VIDEO_DRIVERS = {
    'Windows': ['windows', 'windib'],
    'Linux': ['x11', 'wayland', 'fbcon'],
    'Darwin': ['cocoa']
}

# Variables de optimización
SDL_HINTS = {
    'SDL_HINT_RENDER_SCALE_QUALITY': '1',  # Filtrado lineal
    'SDL_HINT_RENDER_VSYNC': '0',          # Sin VSync
    'SDL_HINT_RENDER_DRIVER_HARDWARE': '1' # Aceleración HW
}
```

### Gestión de Perfiles

Los perfiles de usuario se guardan automáticamente en `Data/profiles.json`:

```json
{
  "default": {
    "high_score": 150,
    "total_games": 25,
    "total_food_eaten": 380,
    "settings": {
      "wrap_around": true,
      "game_speed": 8
    }
  }
}
```

## Versiones

- **v1.0.0: Versión inicial del juego clásico Snake.**

  - Implementación básica del juego.
  - Movimiento de la serpiente y detección de colisiones.
  - Generación de comida y aumento de tamaño de la serpiente.

- **v1.1.0: Mejoras en la gestión de perfiles y almacenamiento de puntajes.**

  - Sistema de perfiles de usuario.
  - Almacenamiento persistente del puntaje más alto.
  - Correcciones menores de bugs.

- **v1.2.0: Corrección de bugs y optimización de rendimiento.**
  - Optimización del motor de colisiones.
  - Reducción del uso de memoria.
  - Corrección de errores en la lógica de crecimiento de la serpiente.
- **v1.3.0: Mejoras gráficas avanzadas.** ✨

  - Sistema completo de efectos visuales con partículas.
  - Animaciones suaves e interpolación de movimientos.
  - Efectos de screen shake y flash para mayor impacto.
  - Serpiente con gradientes, sombras y ojos animados.
  - Comida y powerups con efectos de brillo y animaciones.
  - Fondo mejorado con gradientes y grid sutil.
  - Interfaz de usuario moderna con sombras y efectos.

- **v1.3.1: Corrección de bugs.** 🐛

  - Arreglado: Rectángulos negros en segmentos de la serpiente.
  - Arreglado: Problemas de interpolación con wrap-around.
  - Arreglado: Problemas menores con colores alpha en efectos.

- **v1.3.2: Sistema de logging completo.** 📝

  - Sistema completo de logging en consola y archivo (`Data/logs.txt`).
  - Logs automáticos de eventos del juego con timestamps.
  - Diferentes niveles de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
  - Logs con colores en consola para mejor legibilidad.
  - Registro de estadísticas de juego y acciones del usuario.

- **v1.3.3: Corrección de bugs detectados por pylint.** 🛠️
  - Eliminación de variables no utilizadas.
  - Corrección de errores de estilo y convenciones de nombres.
  - Mejora en la legibilidad del código.
  - Ajustes en la lógica para evitar posibles errores en tiempo de ejecución.

- **v1.4.0: Release de estabilidad y optimización.** 🚀
  - Consolidación de todas las correcciones de bugs anteriores.
  - Optimización general del rendimiento.
  - Mejora en la gestión de memoria.
  - Corrección de problemas de interpolación y colisiones.
  - Estabilización del sistema de partículas.
  - Mejora en el sistema de logging.
  - Actualización del sistema de perfiles.
  - Corrección de fugas de memoria menores.
  - Mejora en la precisión de las colisiones.
  - Optimización de las animaciones y efectos visuales.

- **v1.5.0: Modernización del sistema de construcción y gestión de dependencias.** 🔧
  - Licencia actualizada de SOL 1.0 a SOL 2.0 (más detallada y completa).
  - Nuevo archivo `pyproject.toml` con soporte completo para Poetry.
  - Mejoras en la gestión de dependencias del proyecto.
  - Scripts de construcción optimizados y modernizados.
  - Documentación de pruebas multiplataforma completadas y verificadas.
  - Sistema de builds y distribución mejorado.
  - Gestión diferenciada de dependencias de desarrollo y producción.
  - Configuración de herramientas de desarrollo integrada (linting, formatting).
  - Soporte para gestores de paquetes modernos (Poetry + pip).

## Características Gráficas Nuevas 🎨

### Efectos Visuales Avanzados:

- **Sistema de partículas** para explosiones y efectos de rastro
- **Screen shake** en colisiones para mayor impacto
- **Efectos de flash** sincronizados con eventos del juego
- **Animaciones suaves** con interpolación cúbica
- **Gradientes dinámicos** en todos los elementos del juego

### Elementos Mejorados:

- 🐍 **Serpiente**: Gradientes, sombras, ojos animados, escala pulsante
- 🍎 **Comida**: Animación pulsante continua con efectos de brillo
- ⚡ **Powerups**: Formas únicas que rotan (triángulos, hexágonos, estrellas)
- 🎨 **Fondo**: Gradiente vertical con grid sutil y obstáculos volumétricos
- 💫 **Partículas**: Explosiones reactivas al comer y recoger items

## Configuración automática de drivers SDL 🔧

El juego incluye un sistema automático de configuración de drivers de video SDL que optimiza el rendimiento según tu sistema operativo y hardware disponible.

### Detección de Sistema Operativo

El sistema detecta automáticamente tu plataforma y configura los drivers apropiados:

- **Windows**: Configura drivers `windows` y `windib` como opciones primarias
- **Linux**: Intenta drivers `x11`, `wayland`, y `fbcon` en orden de preferencia
- **macOS**: Utiliza el driver nativo `cocoa`
- **Otros SO**: Usa configuración por defecto de SDL como fallback

### Mensajes de Logging

Durante la configuración automática, el sistema genera los siguientes tipos de mensajes en `Data/logs.txt`:

```
[INFO] [VIDEO] Iniciando configuración completa del sistema de video
[INFO] [VIDEO] Intentando driver de video: windows
[INFO] [VIDEO] Driver de video configurado exitosamente: windows
[DEBUG] [VIDEO] Variable SDL_VIDEO_WINDOW_POS configurada: centered
[DEBUG] [VIDEO] Variable SDL_HINT_RENDER_DRIVER configurada: direct3d
[DEBUG] [VIDEO] Variable SDL_HINT_RENDER_SCALE_QUALITY configurada: 1
[DEBUG] [VIDEO] Variable SDL_HINT_RENDER_DRIVER_HARDWARE configurada: 1
[DEBUG] [VIDEO] Variable SDL_HINT_RENDER_VSYNC configurada: 0
[INFO] [VIDEO] Variables de entorno adicionales configuradas exitosamente: 5 variables
[INFO] [VIDEO] Configuración completa del sistema de video finalizada exitosamente
```

#### Modificar variables de renderizado:
```bash
# Habilitar VSync
set SDL_HINT_RENDER_VSYNC=1

# Cambiar calidad de escalado (0=nearest, 1=linear, 2=anisotropic)
set SDL_HINT_RENDER_SCALE_QUALITY=2

# Deshabilitar aceleración por hardware
set SDL_HINT_RENDER_DRIVER_HARDWARE=0
```

#### Depuración de problemas:
Si experimentas problemas gráficos, revisa los logs en `Data/logs.txt` y:
1. Verifica qué driver se está usando
2. Comprueba si hay mensajes de advertencia o error
3. Intenta forzar un driver diferente manualmente
4. Ajusta las variables de renderizado según tu hardware

## Pruebas Manuales Realizadas ✅

Se han realizado pruebas exhaustivas del sistema de configuración de video y logging en múltiples entornos.

### 📊 Resultados de Pruebas

| Plataforma | Driver Elegido | Estado | Fallbacks Disponibles |
|------------|----------------|--------|-----------------------|
| Windows    | `windows`      | ✅ OK  | `windib`              |
| Linux      | `x11`          | ✅ OK  | `wayland`, `fbcon`    |
| macOS      | `cocoa`        | ✅ OK  | Ninguno necesario     |

### 🔍 Troubleshooting

Si experimentas problemas:

1. **Revisar logs:** `Data/logs.txt` contiene información detallada
2. **Forzar driver:** `export SDL_VIDEODRIVER=<driver>`
3. **Verificar pygame:** Los logs muestran si pygame está disponible
4. **Probar fallbacks:** El sistema intenta múltiples drivers automáticamente

## 🎮 Controles del Juego

### Controles Básicos
- **↑ ↓ ← →** - Mover la serpiente
- **WASD** - Controles alternativos de movimiento
- **ESC** - Pausar el juego / Volver al menú
- **ENTER** - Confirmar selección en menús
- **ESPACIO** - Pausar/Reanudar durante el juego

### Menús de Navegación
- **↑ ↓** - Navegar por las opciones del menú
- **ENTER** - Seleccionar opción
- **ESC** - Volver al menú anterior
- **TAB** - Cambiar entre perfiles (en selección de perfil)

### Atajos Especiales
- **F11** - Alternar pantalla completa (si está disponible)
- **F10** - Captura de pantalla (si está implementada)

## 👾 Cómo Jugar

### Objetivo
Controla la serpiente para comer la mayor cantidad de comida posible sin chocar contigo mismo o con los obstáculos.

### Puntuación
- 🍎 **Comida Normal**: +10 puntos
- ⚡ **Speed Powerup**: +15 puntos + velocidad temporal
- 🔷 **Grow Powerup**: +20 puntos + crecimiento extra
- ⭐ **Score Powerup**: +50 puntos
- 🔵 **Slow Powerup**: +15 puntos + ralentización temporal

### Configuraciones Especiales
- **Wrap Around**: Permite atravesar paredes para aparecer en el lado opuesto
- **Obstáculos**: Bloques que debes evitar en algunos niveles
- **Velocidad Adaptativa**: El juego se acelera gradualmente

## 🛠️ Desarrollo y Arquitectura

### Tecnologías Utilizadas
- **Python 3.10+**: Lenguaje principal
- **Pygame 2.6.1**: Motor de juego y gráficos
- **SDL**: Sistema de bajo nivel para gráficos y audio
- **JSON**: Almacenamiento de datos de perfiles
- **Logging**: Sistema nativo de Python para logs

### Patrón de Arquitectura
- **MVC (Model-View-Controller)**: Separación clara de lógica
- **Sistema de Componentes**: Efectos visuales modulares
- **Event-Driven**: Manejo basado en eventos de Pygame
- **Configuration-First**: Toda la configuración centralizada

## 👥 Contribuciones

¡Las contribuciones son bienvenidas! Este proyecto sigue un modelo de desarrollo abierto.

### Cómo Contribuir

1. **Fork el repositorio**
2. **Crear una rama para tu feature**: `git checkout -b feature/nueva-caracteristica`
3. **Hacer commit de tus cambios**: `git commit -m 'Añadir nueva característica'`
4. **Push a la rama**: `git push origin feature/nueva-caracteristica`
5. **Abrir un Pull Request**

### Guías de Contribución

#### Estándares de Código
```bash
# Ejecutar linters antes de contribuir
pylint *.py
flake8 *.py
isort *.py --check-only
```

#### Tipos de Contribución
- 🐛 **Bug Fixes**: Corrección de errores
- ✨ **Features**: Nuevas características
- 🎨 **Graphics**: Mejoras visuales
- 📄 **Documentación**: Mejoras en documentación
- ⚡ **Performance**: Optimizaciones de rendimiento
- 🔧 **Refactoring**: Mejoras en la estructura del código

### Áreas Que Necesitan Contribución
- 🎵 **Sistema de Audio**: Música y efectos de sonido
- 🌍 **Localización**: Traducción a otros idiomas
- 🚀 **Optimización**: Mejoras de rendimiento
- 🎨 **Arte**: Sprites y texturas mejoradas
- 📁 **Documentación**: Guías y tutoriales
- 🧪 **Testing**: Más pruebas automatizadas

## 🔗 Enlaces Útiles

- **Repositorio**: [https://github.com/ParaDevOne/snake](https://github.com/ParaDevOne/snake)
- **Issues**: [Reportar bugs o sugerir features](https://github.com/ParaDevOne/snake/issues)
- **Releases**: [Descargar versiones compiladas](https://github.com/ParaDevOne/snake/releases)

## 🔎 FAQ (Preguntas Frecuentes)

### ¿El juego funciona sin conexión a internet?
Sí, es completamente offline. No requiere conexión a internet.

### ¿Puedo modificar los gráficos?
Sí, todos los colores y efectos están en `settings.py` y `visual_effects.py`.

### ¿Cómo activo/desactivo los efectos visuales?
Modifica las variables en `settings.py`, como `PARTICLES_ENABLED` o `SMOOTH_MOVEMENT`.

### ¿Dónde se guardan mis puntajes?
En el archivo `Data/profiles.json` que se crea automáticamente.

### ¿Puedo compilarlo para distribución?
Sí, usa el script `setup.py` con PyInstaller para crear ejecutables.

## 📞 Futuras Mejoras

### Version - Planificada
- 🎵 **Sistema de Audio Completo**
  - Música de fondo dinámica
  - Efectos de sonido para todas las acciones
  - Control de volumen por categorías

### Version - Planificada
- 🌍 **Localización**
  - Soporte para múltiples idiomas

### Version - Concepto
- 👥 **Modo Multijugador**
  - Pantalla dividida local

- 🎆 **Modos de Juego Adicionales**
  - Supervivencia con obstáculos dinámicos
  - Contrarreloj
  - Laberintos procedurales
  - Modo arcade con power-ups especiales

## 📋 Licencia

```
Simplified Open License (SOL) v3.0
Copyright (c) 2025 ParaDevOne

• Uso libre para cualquier propósito (personal, educativo, comercial)
• Modificación y distribución permitidas con atribución
• Uso comercial completamente permitido
• Protección de marcas registradas del autor
• Licencias de patentes otorgadas automáticamente
• Sin garantía, uso bajo tu propia responsabilidad
• Indemnización requerida por parte del usuario
```

Para más detalles, consulta el archivo [`LICENSE.txt`](LICENSE.txt) incluido en este repositorio.

---

**🐍 Hecho con ❤️ por [ParaDevOne](https://github.com/ParaDevOne)**

*Si te gusta este proyecto, ¡dale una ⭐ en GitHub!*
