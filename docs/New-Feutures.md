# New Features — Snake

---

## Resumen

Este documento recoge el plan, criterios de aceptación, notas técnicas y checklist para implementar las features marcadas. Está pensado para integrarlo directamente en el repo y usado como hoja de ruta para desarrollo, pruebas y QA.

---

## 1) Modo por niveles

**Descripción:** Campaña por niveles donde cada nivel tiene un layout y objetivos distintos.

**Impacto:** Alta rejugabilidad, separación clara entre objetivos y partidas rápidas.

**Complejidad estimada:** Media.

**Criterios de aceptación:**

* Existe una selección en el menú para elegir "Campaña (niveles)" o "Infinito".
* Campaña: al menos 6 niveles diseñados (pueden ser simples) con cambio de layout entre niveles.
* Infinito: dificultad aumenta cada X puntos/segundos.
* Transición de nivel estable y sin glitches (guardar estado, reset de power-ups, posicionamiento correcto de la serpiente/food).

**Notas de implementación:**

* Definir `Level` como clase con propiedades: `layout`, `initial_snake_pos`, `initial_speed`, `objectives`, `powerup_frequency`.
* Niveles guardados en `Data/levels/level_01.json`... con el mismo schema del editor (sección abajo).
* Motor de progresión para modo infinito: `difficulty = base + floor(score / X) * delta`.
* Guardar checkpoint opcional entre niveles.

**Criterios técnicos:**

* No se debe reiniciar todo el proceso si subes de nivel (reset controlado de objetos temporales).
* HUD muestra nivel actual y objetivo si aplica.

---

## 2) Power-up: GHOST (atravesar cola/paredes)

**Descripción:** Power-up temporal que permite a la serpiente atravesar su propia cola y/o paredes durante 5000 milisegundos.

**Impacto:** Cambia dinámicas de riesgo y planificación.

**Complejidad estimada:** Baja.

**Criterios de aceptación:**

* El power-up aparece en mapa y puede recogerse.
* Al activarse, se establece `snake.ghost_mode = True` y expirará a los 5000 milisegundos.
* Mientras `ghost_mode` True, la colisión con la propia cola y/o paredes se ignora según flags configurables (por ejemplo, `ghost_ignores_walls`, `ghost_ignores_self`).
* Indicador visual en HUD (icono + contador regresivo).

**Notas de implementación:**

* No eliminar la detección de colisiones: envolverla en checks (`if not snake.ghost_mode and collide_with_self(): game_over()`).
* Para evitar exploits, al terminar el efecto comprobar que la serpiente no esté incrustada en pared/cola — en caso de superposición, desplazar la cabeza a la primera celda válida o matar al jugador según diseño.
* Duración configurable por power-up (por defecto 5s).

**Variables sugeridas:** `PowerUp(kind='ghost', duration=5, ignore_walls=True, ignore_self=True)`.

---

## 3) Local multiplayer (split-screen / hotseat)

**Descripción:** Dos modos multiplayer locales:

* **Split-screen:** Dos jugadores simultáneos en la misma pantalla (cada uno en su viewport) — ideal con gamepads/teclados separados.
* **Hotseat:** Turnos alternos en la misma sesión (útil en modos por niveles o desafíos).

**Impacto:** Alta diversión social en la misma máquina.

**Complejidad estimada:** Media.

**Criterios de aceptación:**

* Menú con opción "Multiplayer" -> elegir `Split-screen` o `Hotseat`.
* Split-screen: pantalla dividida vertical/horizontal según resolución; cada jugador tiene su HUD (score/vidas/powerups).
* Hotseat: transición de turno clara; estado de la partida guardado entre turnos.
* Entrada configurable: cada jugador puede mapear sus controles (teclado 1/teclado 2/gamepad).

**Notas de implementación (split-screen):**

* Implementar renderizado con dos cámaras: calcular viewport rects y renderizar escena dos veces con su propia `camera_offset`.
* Cada jugador mantiene entidad `Snake` independiente y su propio `GameState` (o compartir el mismo `World` según diseño competitivo/cooperativo).
* Evitar colisiones entre jugadores en modo cooperativo (opcional): definir reglas claras (p.ej., colisión entre serpientes sí provoca muerte).

**Hotseat:**

* Guardar estado simple entre turnos: posición de la comida, obstácuclos, seed RNG para reproducibilidad.
* Mostrar resumen entre turnos (puntuación, efectos activos).

---

## 4) Editor de niveles (JSON)

**Descripción:** Editor mínimo (herramienta separada o modo dev) para crear/editar niveles y para hacerlos como JSON compatible con el motor.

**Impacto:** Facilita creación rápida de niveles y reproducibilidad.

**Complejidad estimada:** Media

**Schema JSON sugerido (ejemplo):**

```json
{
  "id": "level_01",
  "name": "Plaza inicial",
  "grid_size": [20, 15],
  "tiles": [
    [0,0,0,1,...],
    ...
  ],
  "initial_snake": { "pos": [5,7], "dir": "RIGHT" },
  "initial_speed": 5,
  "food_positions": [],
  "powerups": [ {"kind":"ghost","pos":[10,5], "spawn_mode":"static"} ],
  "objectives": {"type":"survive","value":60}
}
```

**Notas de implementación (editor):**

* Implementar editor como script Pygame independiente (`tools/level_editor.py`) con export JSON.
* Permitir pintar tiles, colocar spawn points, power-ups y probar nivel en modo preview.
* Incluir validación básica al exportar (snake inside bounds, no walls covering spawn, etc.).

---

## Checklist de implementación (por feature)

* [ ] Diseño: doc breve con comportamiento final
* [ ] Prototipo mínimo (engine + pruebas headless)
* [ ] Integración en game loop principal
* [ ] UI/HUD (contador powerups, nivel, turnos)
* [ ] Performance check (30 min sim)
* [ ] Documentación (README, schema JSON)

---

## Notas finales

* Evitar cambios grandes en el mismo commit: separar engine, UI/HUD y multiplayer en archivos distintos.
