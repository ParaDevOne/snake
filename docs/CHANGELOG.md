# CHANGELOG

Todas las modificaciones, mejoras y correcciones del proyecto Snake Game se documentan aquí siguiendo el formato semántico.

---

## [1.7.0] - 20-08-2025
- Obstáculos y nuevos componentes de UI.
	- Añadido sistema de obstáculos: colisiones, generación y gestión desde `obstacles.py`.
	- Nuevo archivo `ui_components.py`: componentes reutilizables para menús y HUD.
	- Mejoras visuales en la interfaz y menús usando los nuevos componentes UI.
	- Corrección de bugs menores y mejoras de estabilidad.

## [1.6.0] - 19-08-2025
- Modularidad avanzada, workflows mejorados, licencia SOL 3.0 y documentación ampliada.
	- Configuración centralizada y documentada en `settings.py`, helpers de acceso y logging en `utils.py`.
	- Logging avanzado: logs detallados de eventos, errores, perfiles y sistema en `Data/logs.txt`.
	- Compatibilidad total con Python 3.13.5+ y dependencias actualizadas en `requirements.txt` y `pyproject.toml`.
	- Workflows de desarrollo y build documentados: ejecución (`python -m main`), instalación (`pip install -r requirements.txt` o `poetry install`), (`pyinstaller setup.py` o `poetry run build`).
	- Licencia actualizada a SOL 3.0, mayor claridad y protección legal.
	- Documentación técnica y de pruebas ampliada en `docs/` y en el propio README.
	- Estructura de datos y persistencia mejorada: perfiles, logs y puntajes organizados en `Data/`.
	- Refactorización y optimización de código para mayor mantenibilidad y rendimiento.
	- Corrección de bugs menores y mejoras de estabilidad.

## [1.5.0] - 17-08-2025
- Modernización del sistema de construcción y gestión de dependencias.
	- Licencia actualizada de SOL 1.0 a SOL 2.0 (más detallada y completa).
	- Nuevo archivo `pyproject.toml` con soporte completo para Poetry.
	- Mejoras en la gestión de dependencias del proyecto.
	- Scripts de construcción optimizados y modernizados.
	- Documentación de pruebas multiplataforma completadas y verificadas.
	- Sistema de builds y distribución mejorado.
	- Gestión diferenciada de dependencias de desarrollo y producción.
	- Configuración de herramientas de desarrollo integrada (linting, formatting).
	- Soporte para gestores de paquetes modernos (Poetry + pip).

## [1.4.0] - 17-08-2025
- Release de estabilidad y optimización.
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

## [1.3.3] - 21-08-2025
- Corrección de bugs detectados por pylint.
	- Eliminación de variables no utilizadas.
	- Corrección de errores de estilo y convenciones de nombres.
	- Mejora en la legibilidad del código.
	- Ajustes en la lógica para evitar posibles errores en tiempo de ejecución.

## [1.3.2] - 13-08-2025
- Sistema de logging completo.
	- Sistema completo de logging en consola y archivo (`Data/logs.txt`).
	- Logs automáticos de eventos del juego con timestamps.
	- Diferentes niveles de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
	- Logs con colores en consola para mejor legibilidad.
	- Registro de estadísticas de juego y acciones del usuario.

## [1.3.1] - 13-08-2025
- Corrección de bugs.
	- [x]: Rectángulos negros en segmentos de la serpiente.
	- [x]: Problemas de interpolación con wrap-around.
	- [x]: Problemas menores con colores alpha en efectos.

## [1.3.0] - 13-08-2025
- Mejoras gráficas avanzadas.
	- Sistema completo de efectos visuales con partículas.
	- Animaciones suaves e interpolación de movimientos.
	- Efectos de screen shake y flash para mayor impacto.
	- Serpiente con gradientes, sombras y ojos animados.
	- Comida y powerups con efectos de brillo y animaciones.
	- Fondo mejorado con gradientes y grid sutil.
	- Interfaz de usuario moderna con sombras y efectos.

## [1.2.0] - 13-08-2025
- Corrección de bugs y optimización de rendimiento.
	- Optimización del motor de colisiones.
	- Reducción del uso de memoria.
	- Corrección de errores en la lógica de crecimiento de la serpiente.

## [1.1.0] - 13-08-2025
- Mejoras en la gestión de perfiles y almacenamiento de puntajes.
	- Sistema de perfiles de usuario.
	- Almacenamiento persistente del puntaje más alto.
	- Correcciones menores de bugs.

## [1.0.0] - 12-08-2025
- Versión inicial del juego clásico Snake.
	- Implementación básica del juego.
	- Movimiento de la serpiente y detección de colisiones.
	- Generación de comida y aumento de tamaño de la serpiente.

---

Estas notas de la versión documentan los cambios, mejoras y correcciones realizadas en el proyecto Snake Game. Cada versión sigue un esquema semántico para facilitar la comprensión de las modificaciones y su impacto en el proyecto. Se recomienda revisar las notas antes de actualizar o contribuir al código para asegurar la compatibilidad y seguir las mejores prácticas establecidas.

---
