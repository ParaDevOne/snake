
# 🐍 Snake Game Version 1.6.0

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green)
![License](https://img.shields.io/badge/license-SOL%203.0-orange)
![Status](https://img.shields.io/badge/status-stable-success)
![Version](https://img.shields.io/badge/version-1.6.0-brightgreen)

> **Snake, modular y multiplataforma con efectos visuales avanzados, perfiles persistentes y workflows.**

## 🎯 Características Destacadas

- 🎨 Efectos visuales avanzados: partículas, gradientes, animaciones suaves
- 🐍 Serpiente mejorada: gradientes, sombras, ojos animados
- 🍎 Comida y powerups dinámicos: formas, animaciones, efectos
- 🌅 Fondos: gradientes, grid, obstáculos volumétricos
- 📝 Logging: consola y archivo, niveles, colores
- 👤 Perfiles persistentes: multiusuario, datos en `Data/profiles/`
- ⚙️ Configuración centralizada: todo en `settings.py`
- 🖥️ Soporte multiplataforma: Windows, Linux, macOS
- 🔧 Workflows: ejecución, instalación, build y logs documentados
- 📄 Documentación técnica: comentarios en el código, guías y ejemplos
- 📦 Distribución: empaquetado y distribución del juego

---

## 📦 Instalación y Workflows

### Instalación Rápida

```bash
git clone https://github.com/ParaDevOne/snake.git
cd snake
pip install -r requirements.txt
python -m main
```

### Instalación con Poetry

```bash
poetry install
poetry run start
```

### Build de ejecutable

```bash
# PyInstaller
python setup.py
# O con Poetry
poetry run build
```

### Logs y datos
- Logs: `Data/logs.txt`
- Perfiles: `Data/profiles/`

---

## 🗂️ Estructura del Proyecto

```
snake/
├── main.py           # Loop principal y orquestación
├── game.py           # Controlador y estado del juego
├── snake.py          # Lógica de la serpiente
├── food.py           # Comida y powerups
├── menu.py           # Menús y navegación
├── logic.py          # Funciones auxiliares
├── settings.py       # Configuración centralizada
├── profiles.py       # Gestión de perfiles y puntajes
├── utils.py          # Utilidades y logging
├── visual_effects.py # Efectos visuales y partículas
├── video_config.py   # Configuración SDL automática
├── requirements.txt  # Dependencias
├── pyproject.toml    # Configuración Poetry/Build
├── setup.py          # Build PyInstaller
├── Data/             # Perfiles, logs
└── docs/             # Documentación técnica
```

---

## ⚙️ Configuración y Personalización

- Todas las opciones en `settings.py` (controles, visual, gameplay)
- Drivers y optimización SDL en `video_config.py`
- Perfiles y puntajes: `Data/profiles/` (nombres de perfil por usuario)
- Logging configurable: niveles, archivo, consola

Ejemplo de configuración:

```python
OBSTACULES = True
WRAP_AROUND = True
POWERUPS_ENABLED = True
SMOOTH_MOVEMENT = True
LOG_LEVEL = "INFO"
LOG_TO_FILE = True
LOG_TO_CONSOLE = True
```

---

## 📝 Versiones y Cambios

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

**v1.6.0: Modularidad avanzada, workflows mejorados, licencia SOL 3.0 y documentación ampliada.** 🚀
  - Configuración centralizada y documentada en `settings.py`, helpers de acceso y logging en `utils.py`.
  - Logging avanzado: logs detallados de eventos, errores, perfiles y sistema en `Data/logs.txt`.
  - Compatibilidad total con Python 3.13.5+ y dependencias actualizadas en `requirements.txt` y `pyproject.toml`.
  - Workflows de desarrollo y build documentados: ejecución (`python -m main`), instalación (`pip install -r requirements.txt` o `poetry install`), (`pyinstaller setup.py` o `poetry run build`).
  - Licencia actualizada a SOL 3.0, mayor claridad y protección legal.
  - Documentación técnica y de pruebas ampliada en `docs/` y en el propio README.
  - Estructura de datos y persistencia mejorada: perfiles, logs y puntajes organizados en `Data/`.
  - Refactorización y optimización de código para mayor mantenibilidad y rendimiento.
  - Corrección de bugs menores y mejoras de estabilidad.

---

## 👾 Cómo Jugar

- **Mover:** ↑ ↓ ← → o WASD
- **Pausar:** ESC o ESPACIO
- **Reiniciar:** R
- **Menús:** ENTER para seleccionar, TAB para cambiar perfil
- **Pantalla completa:** F11
- **Captura:** F10

### Objetivo
Come la mayor cantidad de comida posible sin chocar contigo mismo ni con obstáculos.

### Puntuación
- 🍎 Comida: +10
- ⚡ Speed Powerup: +15 y velocidad
- 🔷 Grow Powerup: +20 y crecimiento
- ⭐ Score Powerup: +50
- 🔵 Slow Powerup: +15 y ralentización

---

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.10 o superior
- **Sistema Operativo**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM**: 512 MB disponible
- **Espacio en Disco**: 64 MB

> [!NOTE]
> Aqui pone **Python 3.10** pero en el archivo [pyproject.toml](pyproject.toml) **pone 3.13.5**,
> eso es porque `Pyinstaller` necesita la version **3.13.5** para funcionar.

---

---

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
> instalalo de forma global o en lib/upx.exe
> (Puede que en entornos Linux/MacOS no funcione bien esta herramienta, pero en Windows la recomiendo.)

## 🎮 Ejecución

### Modo Normal
```bash
python -m main
```

---

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
---

### 🔍 Troubleshooting

Si experimentas problemas:

1. **Revisar logs:** `Data/logs.txt` contiene información detallada
2. **Forzar driver:** `export SDL_VIDEODRIVER=<driver>`
3. **Verificar pygame:** Los logs muestran si pygame está disponible
4. **Probar fallbacks:** El sistema intenta múltiples drivers automáticamente

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

## 🛠️ Desarrollo

---

## ❓ FAQ Rápido

- ¿Funciona offline? **Sí**
- ¿Dónde están mis puntajes? `Data/profiles/`
- ¿Puedo modificar gráficos? Sí, en `settings.py` y `visual_effects.py`
- ¿Compilar para distribución? Sí, con `setup.py` o `Poetry run build`
- ¿Logs? En `Data/logs.txt`

---

## 📄 Licencia

**Simplified Open License (SOL) v3.0**

Uso libre para cualquier propósito (personal, educativo, comercial). Modificación y distribución permitidas con atribución. Uso comercial permitido. Protección de marcas y patentes. Sin garantía, uso bajo tu responsabilidad. Indemnización requerida por parte del usuario.

Consulta el archivo [`LICENSE.txt`](LICENSE.txt) para detalles completos.

---

**🐍 Hecho con ❤️ por [ParaDevOne](https://github.com/ParaDevOne)**

*Si te gusta este proyecto, ¡dale una ⭐ en GitHub!*
