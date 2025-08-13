# Snake Game

Este proyecto es una implementación del clásico juego de la serpiente en Python.

## Estructura del proyecto

- `main.py`: Archivo principal para ejecutar el juego.
- `snake.py`: Lógica de la serpiente.
- `food.py`: Lógica de la comida.
- `game.py`: Controlador principal del juego.
- `logic.py`: Funciones auxiliares de lógica.
- `settings.py`: Configuración del juego.
- `profiles.py`: Gestión de perfiles de usuario.
- `utils.py`: Utilidades generales.
- `Data/score/highscore.json`: Almacena el puntaje más alto.

## Requisitos

- Python 3.8 o superior

## Instalación

1. Clona el repositorio:
   ```pwsh
   git clone https://github.com/ParaDevOne/snake.git
   ```
2. Instala las dependencias si las hay (puedes agregar instrucciones aquí si usas algún paquete externo).

## Ejecución

Ejecuta el juego con:

```pwsh
python -m main
```

## Personalización

Puedes modificar `settings.py` para cambiar la configuración del juego.

## Créditos

Desarrollado por ParaDevOne.

## Versiones

- **v1.0.0: Versión inicial del juego clásico Snake.**
- **v1.1.0: Mejoras en la gestión de perfiles y almacenamiento de puntajes.**
- **v1.2.0: Corrección de bugs y optimización de rendimiento.**
- **v1.3.0: MEJORAS GRÁFICAS AVANZADAS** ✨
  - Sistema completo de efectos visuales con partículas
  - Animaciones suaves e interpolación de movimientos
  - Efectos de screen shake y flash para mayor impacto
  - Serpiente con gradientes, sombras y ojos animados
  - Comida y powerups con efectos de brillo y animaciones
  - Fondo mejorado con gradientes y grid sutil
  - Interfaz de usuario moderna con sombras y efectos
- **v1.3.1: CORRECCIÓN DE BUGS** 🐛
  - Arreglado: Rectángulos negros en segmentos de la serpiente
  - Arreglado: Problemas de interpolación con wrap-around
  - Arreglado: Problemas menores con colores alpha en efectos
- **v1.3.2: SISTEMA DE LOGGING COMPLETO** 📝
  - Sistema completo de logging en consola y archivo (`Data/logs.txt`)
  - Logs automáticos de eventos del juego con timestamps
  - Diferentes niveles de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Logs con colores en consola para mejor legibilidad
  - Registro de estadísticas de juego y acciones del usuario

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

### Demo de Efectos:
Ejecuta `python demo_visual_effects.py` para una demostración interactiva de todos los efectos.

## Futuras mejoras

- Añadir niveles de dificultad.
- Implementar modo multijugador local.
- Agregar efectos de sonido y música.
- ~~Crear una interfaz gráfica mejorada.~~ ✅ **COMPLETADO en v1.3.0**
- Guardar y cargar partidas.
- Temas visuales adicionales y personalización avanzada.
- Poner más logs en consola y en la carpeta Data en un logs.txt
- Bugs
