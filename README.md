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

## Futuras mejoras

- Añadir niveles de dificultad con configuraciones personalizables.
- Implementar modo multijugador local con pantalla dividida.
- Agregar efectos de sonido y música.
- Guardar y cargar partidas en diferentes ranuras.
- Más opciones en opciones.
- Mejorar el sistema de logging con métricas avanzadas.
- Soporte para más idiomas.

## Licencia

Este proyecto está licenciado bajo la **Simplified Open License (SOL)**, versión 1.0. Para más detalles, consulta el archivo `LICENSE.txt` incluido en este repositorio.
