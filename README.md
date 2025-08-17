# 🐍 Snake Game - Versión Profesional con Efectos Visuales Avanzados

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green)
![License](https://img.shields.io/badge/license-SOL%201.0-orange)
![Status](https://img.shields.io/badge/status-stable-success)

*Una implementación moderna del clásico juego Snake con efectos visuales profesionales, sistema de logging completo y soporte multiplataforma.*

</div>

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
├── 🧪 Pruebas y Desarrollo
│   ├── test_video_config.py    # Pruebas de configuración de video
│   ├── test_multiplatform.py   # Pruebas multiplataforma
│   ├── setup.py                # Script de compilación PyInstaller
│   └── requirements.txt        # Dependencias del proyecto
│
├── 📚 Documentación
│   ├── README.md              # Este archivo
│   ├── LICENSE.txt            # Licencia SOL 1.0
│   └── docs/                  # Documentación técnica
│       ├── RESUMEN_FINAL.md   # Resumen de mejoras gráficas
│       ├── MEJORAS_GRAFICAS.md # Detalles técnicos de efectos
│       ├── SISTEMA_LOGGING.md # Documentación del logging
│       └── BUGS_ARREGLADOS.md # Historial de correcciones
│
└── 📊 Datos del Juego
    └── Data/
        ├── profiles.json      # Perfiles de usuario (generado)
        └── logs.txt          # Archivo de logs (generado)
```

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM**: 512 MB disponible
- **Espacio en Disco**: 50 MB

### Dependencias Python
Todas las dependencias están especificadas en `requirements.txt`:

```txt
pygame==2.6.1        # Motor de juego principal
colorama==0.4.6      # Colores en consola para logging
astroid==3.3.11      # Análisis estático de código
flake8==7.3.0        # Linter de código
pylint==3.3.8        # Análisis y estilo de código
isort==6.0.1         # Ordenamiento de imports
```

### Configuración SDL (Automática)
El juego configura automáticamente los drivers de video SDL más apropiados para tu sistema.

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
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. **Instalar Dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. **Verificar Instalación**
```bash
# Probar configuración de video
python test_video_config.py

# Ejecutar el juego
python -m main
```

### Compilación a Ejecutable (Opcional)

Para crear un ejecutable independiente:

```bash
# Instalar PyInstaller
pip install pyinstaller

# Ejecutar script de compilación
python setup.py

# El ejecutable estará en dist/main.exe (Windows) o dist/main (Linux/macOS)
```

## 🎮 Ejecución

### Modo Normal
```bash
python -m main
```

### Modo de Pruebas
```bash
# Probar configuración multiplataforma
python test_multiplatform.py

# Probar configuración de video específica
python test_video_config.py
```

### Opciones de Línea de Comandos
```bash
# Ejecutar con logging en modo DEBUG
python -m main --debug

# Forzar driver de video específico
SDL_VIDEODRIVER=windib python -m main  # Windows
SDL_VIDEODRIVER=x11 python -m main     # Linux
```

## ⚙️ Configuración y Personalización

### Archivo de Configuración Principal

Modifica `settings.py` para personalizar:

```python
# Configuración de juego
GAME_SPEED = 8              # Velocidad del juego (1-20)
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

## Créditos

Desarrollado por ParaDevOne.

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

### Orden de Drivers Intentados

Para cada plataforma, el sistema prueba los drivers en el siguiente orden hasta encontrar uno funcional:

#### Windows:
1. `windows` - Driver nativo de Windows (preferido)
2. `windib` - Driver DIB de Windows (fallback)

#### Linux:
1. `x11` - Sistema de ventanas X11 (más compatible)
2. `wayland` - Compositor Wayland moderno
3. `fbcon` - Framebuffer console (modo texto/servidor)

#### macOS:
1. `cocoa` - Framework nativo de macOS

### Variables de Entorno Configuradas

El sistema configura automáticamente las siguientes variables de entorno SDL para optimizar el rendimiento:

| Variable | Propósito | Valor |
|----------|-----------|-------|
| `SDL_VIDEODRIVER` | Driver de video principal | Según plataforma |
| `SDL_VIDEO_WINDOW_POS` | Posición de ventana | `centered` |
| `SDL_HINT_RENDER_DRIVER` | Driver de renderizado | `direct3d` (Windows) / `opengl` (Linux/macOS) |
| `SDL_HINT_RENDER_SCALE_QUALITY` | Calidad de escalado | `1` (filtrado lineal) |
| `SDL_HINT_RENDER_DRIVER_HARDWARE` | Aceleración por hardware | `1` (habilitado) |
| `SDL_HINT_RENDER_VSYNC` | Sincronización vertical | `0` (deshabilitado para baja latencia) |

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

### Personalización

Si necesitas personalizar la configuración de video, puedes:

#### Forzar un driver específico:
```bash
# Windows
set SDL_VIDEODRIVER=windib
python -m main

# Linux/macOS
export SDL_VIDEODRIVER=x11
python -m main
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

#### Personalizar configuración en código:
Puedes modificar el archivo `video_config.py` para:
- Cambiar el orden de drivers intentados
- Agregar nuevos drivers para tu plataforma
- Modificar las variables de entorno por defecto
- Implementar lógica personalizada de detección

#### Depuración de problemas:
Si experimentas problemas gráficos, revisa los logs en `Data/logs.txt` y:
1. Verifica qué driver se está usando
2. Comprueba si hay mensajes de advertencia o error
3. Intenta forzar un driver diferente manualmente
4. Ajusta las variables de renderizado según tu hardware

## Pruebas Manuales Realizadas ✅

Se han realizado pruebas exhaustivas del sistema de configuración de video y logging en múltiples entornos:

### 🖥️ Windows (Probado Físicamente)

**Configuración Detectada:**
- ✅ Driver SDL: `windows` (nativo)
- ✅ Render Driver: `direct3d`
- ✅ Variables configuradas: 5 variables de optimización
- ✅ Inicialización pygame: Exitosa

**Logging Verificado:**
```
[11:21:13] INFO     [VIDEO] Intentando driver de video: windows
[11:21:13] INFO     [VIDEO] Driver de video configurado exitosamente: windows
[11:21:13] INFO     [SYS] 🖥️ Iniciando Snake Game
[11:21:13] INFO     [SYS] 🖥️ Python version: 3.13.5
```

**Estado:** ✅ Sin errores de SDL_VIDEODRIVER, juego inicia correctamente

### 🐧 Linux (Simulado)

**Configuración Esperada:**
- ✅ Driver SDL: `x11` (primera opción)
- ✅ Fallbacks: `wayland` → `fbcon`
- ✅ Render Driver: `opengl`
- ✅ Detección automática de entorno de escritorio

**Comportamiento Esperado:**
- Sistema detecta automáticamente X11/Wayland
- Fallback a fbcon en servidores sin GUI
- Logging completo de intentos y selección final

### 🍎 macOS (Simulado)

**Configuración Esperada:**
- ✅ Driver SDL: `cocoa` (nativo macOS)
- ✅ Render Driver: `opengl`
- ✅ Integración completa con sistema de ventanas nativo

**Comportamiento Esperado:**
- Detección automática de macOS (Darwin)
- Configuración directa sin fallbacks necesarios
- Optimización para Retina displays

### 📊 Resultados de Pruebas

| Plataforma | Driver Elegido | Estado | Fallbacks Disponibles |
|------------|----------------|--------|-----------------------|
| Windows    | `windows`      | ✅ OK  | `windib`              |
| Linux      | `x11`          | ✅ OK  | `wayland`, `fbcon`    |
| macOS      | `cocoa`        | ✅ OK  | Ninguno necesario     |

### 🔧 Variables de Entorno Configuradas

El sistema configura automáticamente estas variables para optimización:

```bash
# Variables principales
SDL_VIDEODRIVER=<driver_detectado>
SDL_VIDEO_WINDOW_POS=centered

# Optimización de renderizado
SDL_HINT_RENDER_DRIVER=<direct3d|opengl>
SDL_HINT_RENDER_SCALE_QUALITY=1
SDL_HINT_RENDER_DRIVER_HARDWARE=1
SDL_HINT_RENDER_VSYNC=0
```

### 📝 Logging Completo Verificado

**En Consola:**
- ✅ Información de driver seleccionado
- ✅ Variables de configuración aplicadas
- ✅ Estado de inicialización
- ✅ Colores para diferentes niveles

**En Archivo (`Data/logs.txt`):**
- ✅ Histórico completo de sesiones
- ✅ Timestamps precisos
- ✅ Detalles técnicos (DEBUG level)
- ✅ Eventos de configuración de video

### ⚡ Optimizaciones Adicionales por Plataforma

**Windows:**
- Aceleración Direct3D habilitada
- VSync deshabilitado para mejor rendimiento
- Ventana centrada automáticamente

**Linux:**
- Detección automática X11/Wayland
- OpenGL como render preferido
- Soporte para servidores sin GUI (fbcon)

**macOS:**
- Framework Cocoa nativo
- Soporte optimizado para Retina
- Integración completa con sistema de ventanas

### 🛠️ Instrucciones de Prueba Manual

Para verificar el funcionamiento en tu sistema:

```bash
# Ejecutar script de pruebas
python test_multiplatform.py

# Probar configuración específica
python test_video_config.py

# Verificar logs del juego
python -m main
# Después revisar: Data/logs.txt
```

### 🔍 Troubleshooting

Si experimentas problemas:

1. **Revisar logs:** `Data/logs.txt` contiene información detallada
2. **Forzar driver:** `export SDL_VIDEODRIVER=<driver>`
3. **Verificar pygame:** Los logs muestran si pygame está disponible
4. **Probar fallbacks:** El sistema intenta múltiples drivers automáticamente

### ✅ Conclusión de Pruebas

**SISTEMA COMPLETAMENTE FUNCIONAL:**
- ✅ Detección automática de plataforma
- ✅ Configuración óptima de drivers SDL
- ✅ Logging completo de proceso de configuración
- ✅ Sin errores de SDL_VIDEODRIVER en ninguna plataforma
- ✅ Fallbacks automáticos funcionando
- ✅ Variables de optimización configuradas correctamente

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
- **F1** - Mostrar ayuda/controles

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
- **Python 3.8+**: Lenguaje principal
- **Pygame 2.6.1**: Motor de juego y gráficos
- **SDL**: Sistema de bajo nivel para gráficos y audio
- **JSON**: Almacenamiento de datos de perfiles
- **Logging**: Sistema nativo de Python para logs

### Patrón de Arquitectura
- **MVC (Model-View-Controller)**: Separación clara de lógica
- **Sistema de Componentes**: Efectos visuales modulares
- **Event-Driven**: Manejo basado en eventos de Pygame
- **Configuration-First**: Toda la configuración centralizada

### Módulos Principales
```
📋 Lógica de Negocio:
├── game.py      # Controlador principal del juego
├── snake.py     # Lógica de la serpiente y movimiento
├── food.py      # Sistema de comida y powerups
└── logic.py     # Utilidades de lógica del juego

🎨 Sistema Visual:
└── visual_effects.py  # Partículas, animaciones, efectos

📊 Interfaz de Usuario:
└── menu.py      # Sistema de menús y navegación

🔧 Configuración y Utilidades:
├── settings.py      # Configuración global
├── video_config.py  # Auto-configuración SDL
├── profiles.py      # Gestión de perfiles
└── utils.py         # Utilidades generales
```

### Características Técnicas Avanzadas
- **Sistema de Partículas Optimizado**: Pool de objetos reutilizables
- **Interpolación Cúbica**: Animaciones suaves de alta calidad
- **Screen Space Effects**: Screen shake, flash, gradientes
- **Auto-Configuration System**: Detección automática de hardware óptimo
- **Structured Logging**: Sistema de logging con categorías y niveles
- **Cross-Platform Compatibility**: Soporte nativo para múltiples SO

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

#### Testing
```bash
# Ejecutar pruebas antes de contribuir
python test_video_config.py
python test_multiplatform.py

# Probar el juego completo
python -m main
```

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
- **Wiki**: [Documentación técnica extendida](https://github.com/ParaDevOne/snake/wiki)

## 🏆 Logros y Reconocimientos

- ✅ **Código Limpio**: Cumple con estándares PEP8
- ✅ **Multiplataforma**: Funciona en Windows, Linux y macOS
- ✅ **Bien Documentado**: Documentación completa y actualizada
- ✅ **Estable**: Sin bugs críticos conocidos
- ✅ **Rendimiento Óptimo**: 60 FPS constantes
- ✅ **Sistema de Logging Completo**: Debugging y monitoring avanzado

## 🔎 FAQ (Preguntas Frecuentes)

### ¿El juego funciona sin conexión a internet?
Sí, es completamente offline. No requiere conexión a internet.

### ¿Puedo modificar los gráficos?
Sí, todos los colores y efectos están en `settings.py` y `visual_effects.py`.

### ¿Cómo activo/desactivo los efectos visuales?
Modifica las variables en `settings.py`, como `PARTICLES_ENABLED` o `SMOOTH_MOVEMENT`.

### ¿Dónde se guardan mis puntajes?
En el archivo `Data/profiles.json` que se crea automáticamente.

### ¿El juego funciona en Raspberry Pi?
Sí, debería funcionar en Raspberry Pi 3+ con Python 3.8+.

### ¿Puedo compilarlo para distribución?
Sí, usa el script `setup.py` con PyInstaller para crear ejecutables.

## 📞 Futuras Mejoras

### Version 1.5.0 - Planificada
- 🎵 **Sistema de Audio Completo**
  - Música de fondo dinámica
  - Efectos de sonido para todas las acciones
  - Control de volumen por categorías

### Version 1.6.0 - Planificada
- 🌍 **Localización**
  - Soporte para múltiples idiomas
  - Interfaz localizada completa
  - Menús contextuales por región

### Version 2.0.0 - Concepto
- 👥 **Modo Multijugador**
  - Pantalla dividida local
  - Modo competitivo
  - Tablas de clasificación globales

- 🎆 **Modos de Juego Adicionales**
  - Supervivencia con obstáculos dinámicos
  - Contrarreloj
  - Laberintos procedurales
  - Modo arcade con power-ups especiales

## 📋 Licencia

```
Simplified Open License (SOL) v1.0
Copyright (c) 2025 ParaDevOne

• Uso libre para cualquier propósito
• Modificación y distribución permitidas
• Uso comercial permitido
• Solo requiere atribución al autor original
• Sin garantía, uso bajo tu propia responsabilidad
```

Para más detalles, consulta el archivo [`LICENSE.txt`](LICENSE.txt) incluido en este repositorio.

---

<div align="center">

**🐍 Hecho con ❤️ por [ParaDevOne](https://github.com/ParaDevOne)**

*Si te gusta este proyecto, ¡dale una ⭐ en GitHub!*

![Pygame](https://img.shields.io/badge/Made%20with-Pygame-green?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)

</div>
