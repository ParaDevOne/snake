
# 🐍 Snake Game Version 1.7.0

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-green)
![License](https://img.shields.io/badge/license-SOL%203.0-orange)
![Status](https://img.shields.io/badge/status-stable-success)
![Version](https://img.shields.io/badge/version-1.7.0-brightgreen)

> **Snake, modular y multiplataforma con efectos visuales avanzados, perfiles persistentes y workflows.**

## 🎯 Características Destacadas

- 🎨 Efectos visuales avanzados: partículas, gradientes, animaciones suaves
- 🐍 Serpiente mejorada: gradientes, sombras, ojos animados
- 🍎 Comida y powerups dinámicos: formas, animaciones, efectos
- 🌅 Fondos: gradientes, grid, obstáculos volumétricos
- 📝 Logging: consola y archivo, niveles, colores [Para más información](./docs/SISTEMA_LOGGING.md)
- 👤 Perfiles persistentes: multiusuario, datos en `Data/profiles/`
- ⚙️ Configuración centralizada: todo en `settings.py`
- 🖥️ Soporte multiplataforma: Windows, Linux, macOS
- 🔧 Workflows: ejecución, instalación, build y logs documentados
- 📄 Documentación técnica: comentarios en el código, guías y ejemplos
- 📦 Distribución: empaquetado y distribución del juego
- 🔍 Análisis de rendimiento: herramientas y métricas
- 🛠️ Mantenimiento: scripts y herramientas de soporte

---

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

## [1.7.0] - 2025-08-21
- Obstáculos y nuevos componentes de UI.
	- Añadido sistema de obstáculos: colisiones, generación y gestión desde `obstacles.py`.
	- Nuevo archivo `ui_components.py`: componentes reutilizables para menús y HUD.
	- Mejoras visuales en la interfaz y menús usando los nuevos componentes UI.
	- Corrección de bugs menores y mejoras de estabilidad.

> [!NOTE]
> **Las versiones anteriores a la ultima se pueden encontrar en el archivo [`CHANGELOG.md`](./docs/CHANGELOG.md).**

## 👾 Cómo Jugar

- **Mover:** ↑ ↓ ← → o WASD
- **Pausar:** ESC o ESPACIO
- **Reiniciar:** R
- **Menús:** ENTER para seleccionar, TAB para cambiar perfil
- **Pantalla completa:** F11

### Objetivo
Come la mayor cantidad de comida posible sin chocar contigo mismo ni con obstáculos (o con las paredes si tienes el modo wrap-around desactivado).

### Puntuación
- 🍎 Comida: +10
- ⚡ Speed Powerup: +1 y velocidad
- 🔷 Grow Powerup: +5 y crecimiento
- ⭐ Score Powerup: +50
- 🔵 Slow Powerup: +10 y ralentización

---

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.10 o superior
- **Sistema Operativo**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM**: 512 MB disponible
- **Espacio en Disco**: 64 MB

> [!NOTE]
> Estos requisitos son para la version ya publicada.

> [!NOTE]
> Aqui pone **Python 3.10** pero en el archivo [pyproject.toml](./pyproject.toml) **pone 3.13.5**,
> eso es porque `Pyinstaller` necesita la version **3.13.5** para funcionar.

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
# Windows Powershell
python -m venv .venv
.venv\Scripts\activate.ps1

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
poetry run start
```

# Compilación a Ejecutable (Opcional)

Para crear un ejecutable independiente:

## Ejecutar script de compilación
```
#### Con bash
python setup.py
```
```

#### Con Poetry en bash:
```bash

# Ejecutar script de compilación
poetry run build
```

```bash
# El ejecutable estará en dist/Snake Game.exe (Windows) o dist/Snake Game (Linux/macOS)
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
5. **Abrir una Pull Request**

### Guías de Contribución

#### Tipos de Contribución
- 🐛 **Bug Fixes**: Corrección de errores
- ✨ **Features**: Nuevas características
- 🎨 **Graphics**: Mejoras visuales
- 📄 **Documentación**: Mejoras en documentación
- ⚡ **Performance**: Optimizaciones de rendimiento
- 🔧 **Refactoring**: Mejoras en la estructura del código

### Áreas Que Necesitan Contribución
- 🌍 **Localización**: Traducción a otros idiomas
- 🚀 **Optimización**: Mejoras de rendimiento
- 🎨 **Arte**: Sprites y texturas mejoradas
- 📁 **Documentación**: Guías y tutoriales
- 🧪 **Testing**: Más pruebas automatizadas

## 📞 Futuras Mejoras

### Version - 1.8
- 🎵 **Sistema de Audio Completo**
  - Música de fondo dinámica
  - Efectos de sonido para la mayoría de acciones

### Version - Planificada
- 🌍 **Localización**
  - Soporte para múltiples idiomas
  - En `./Data/lang` se pondrán JSON con las traducciones
  - Arreglo de pantalla completa y menús

### Version - Concepto
- 👥 **Modo Multijugador**
  - Pantalla dividida local

- 🎆 **Modos de Juego Adicionales**
  - Contrarreloj
  - Modo arcade

## 🛠️ Desarrollo

---

### ❓ FAQ Rápido

- ¿Funciona offline? **Sí**
- ¿Dónde están mis puntajes? `Data/profiles/`
- ¿Puedo modificar gráficos? Sí, en `settings.py` y `visual_effects.py`
- ¿Compilar para distribución? Sí, con `setup.py` o `Poetry run build`
- ¿Logs? En `Data/logs.txt`

---

### 📄 Licencia

**Simplified Open License (SOL) v3.0**

Uso libre para cualquier propósito (personal, educativo, comercial). Modificación y distribución permitidas con atribución. Uso comercial permitido. Protección de marcas y patentes. Sin garantía, uso bajo tu responsabilidad. Indemnización requerida por parte del usuario.

Consulta el archivo [`LICENSE.txt`](LICENSE.txt) para detalles completos.

---

**🐍 Hecho con ❤️ por [ParaDevOne](https://github.com/ParaDevOne)**

*Si te gusta este proyecto, ¡dale una ⭐ en GitHub!*
