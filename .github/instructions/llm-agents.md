# Instrucciones para Agentes LLM – Proyecto Snake Game (Python)

## 1. Estructura y Arquitectura

- El proyecto es una versión avanzada y modular del clásico Snake, usando Python 3.13.5+.
- Los módulos principales son:
  - `main.py`: punto de entrada, loop principal, orquestación.
  - `game.py`: controlador y gestión del estado del juego.
  - `snake.py`: lógica y movimiento de la serpiente.
  - `food.py`: lógica de comida y powerups.
  - `menu.py`: menús (si existen).
  - `logic.py`: funciones auxiliares.
  - `settings.py`: configuración centralizada.
  - `profiles.py`: gestión de perfiles y puntajes.
  - `utils.py`: utilidades, logging, helpers JSON.
  - `visual_effects.py`: efectos visuales y partículas.
  - Carpeta `Data/`: datos persistentes (perfiles, logs, assets).

## 2. Principios de Desarrollo

- Toda la configuración debe gestionarse desde `settings.py`.
- El acceso a archivos y logging debe hacerse usando los helpers de `utils.py`.
- Los efectos visuales deben ser modulares y estar en `visual_effects.py`.
- El estado del juego se gestiona en `game.py` y se comunica por objetos y funciones.
- Para nuevas features, crea un módulo y enlázalo desde `main.py` y/o `game.py`.
- Si agregas dependencias, actualiza `requirements.txt` y `pyproject.toml`.

## 3. Workflows

- Ejecutar: `python -m main`
- Instalar dependencias: `pip install -r requirements.txt` o `poetry install`
- Compilar ejecutable: `pyinstaller setup.py` o `poetry run build`
- Logs: en `Data/logs.txt` y consola
- Perfiles: en `Data/profiles.json`

## 4. Convenciones para Agentes LLM

- Usa helpers de `utils.py` para acceso a datos y logging.
- Toda configuración nueva debe ir en `settings.py`.
- Los efectos visuales nuevos deben ser modulares y ubicarse en `visual_effects.py`.
- Mantén el código limpio, modular y documentado.
- Sigue los patrones y convenciones de los módulos principales.
- Consulta el archivo `LICENSE.txt` para temas de licencia (SOL).

---

Estas instrucciones aseguran que cualquier agente LLM pueda contribuir de forma consistente y alineada con la arquitectura y estándares del proyecto.
