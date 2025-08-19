""""A module for the game logic and mechanics."""
# logic.py
import time
import random
import settings
import utils
from snake import Snake
from food import Food, PowerUp
import profiles

class GameLogic:
    """Game logic and mechanics."""
    def __init__(self, load_highscore=True, profile_name=None):
        # profile_name: si None -> settings.DEFAULT_PROFILE
        self.profile_name = profile_name or settings.DEFAULT_PROFILE
        self.load_highscore_flag = load_highscore

        # Inicializar todos los atributos de instancia
        self.snake = None
        self.obstacles = []
        self.food = None
        self.powerup = None
        self.score = 0
        self.move_delay = settings.INIT_MOVE_DELAY
        self.game_over = False
        self.paused = False
        self.active_power = None
        self.power_end_time_ms = 0
        self.prev_snake = []
        self.last_move_start_ms = 0
        self.profile = {}
        self.highscore = 0

        self.reset()

    def reset(self):
        """Reiniciar el juego a su estado inicial."""
        utils.log_game_event("Reiniciando juego")
        mid = (settings.COLUMNS // 2, settings.ROWS // 2)
        init = [mid, (mid[0]-1, mid[1]), (mid[0]-2, mid[1])]
        self.snake = Snake(init)
        self.obstacles = list(settings.OBSTACLES) if settings.USE_OBSTACLES else []
        self.food = Food(self.snake.body + self.obstacles, self.obstacles)
        self.powerup = None
        self.score = 0
        self.move_delay = settings.INIT_MOVE_DELAY  # ms
        self.game_over = False
        self.paused = False

        self.active_power = None
        self.power_end_time_ms = 0

        # interpolation helpers
        self.prev_snake = list(self.snake.body)
        self.last_move_start_ms = self.now_ms()

        # load profile / highscore
        if self.load_highscore_flag:
            # if profile doesn't exist, create it
            if not profiles.profile_exists(self.profile_name):
                profiles.create_profile(self.profile_name)
            self.profile = profiles.load_profile(self.profile_name)
            self.highscore = self.profile.get("highscore", 0)
        else:
            self.profile = {"name": self.profile_name}
            self.highscore = 0

    def set_profile(self, profile_name):
        """Cambiar el perfil activo en caliente. \
        Cargará/creará el perfil y actualizará highscore."""
        self.profile_name = profile_name or settings.DEFAULT_PROFILE
        if not profiles.profile_exists(self.profile_name):
            profiles.create_profile(self.profile_name)
        self.profile = profiles.load_profile(self.profile_name)
        self.highscore = self.profile.get("highscore", 0)

    def now_ms(self):
        """Obtener la marca de tiempo actual en milisegundos."""
        return int(time.time() * 1000)

    def spawn_power_if_needed(self):
        """Generar un power-up si es necesario."""
        if not settings.POWERUP_ENABLED:
            return
        if self.powerup is not None:
            return
        if random.random() < getattr(settings, "POWERUP_CHANCE", 0.12):
            self.powerup = PowerUp(self.snake.body + ([self.food.pos]
                                                    if self.food.pos else []) + self.obstacles,
                                                    self.obstacles)

    def apply_powerup(self, ptype):
        """Aplicar un power-up al jugador."""
        self.active_power = ptype
        self.power_end_time_ms = self.now_ms() + getattr(settings, "POWERUP_DURATION_MS", 7000)
        if ptype == "slow":
            self.move_delay = min(999, self.move_delay + 80)
        elif ptype == "speed":
            self.move_delay = max(settings.MIN_MOVE_DELAY, self.move_delay - 60)
        elif ptype == "grow":
            self.snake.grow(3)
        elif ptype == "score":
            self.score += 3

    def clear_power_effects(self):
        """Limpiar los efectos del power-up activo."""
        if not self.active_power:
            return
        if self.active_power == "slow":
            self.move_delay = max(settings.MIN_MOVE_DELAY, self.move_delay - 80)
        elif self.active_power == "speed":
            self.move_delay = min(settings.INIT_MOVE_DELAY, self.move_delay + 60)
        self.active_power = None
        self.power_end_time_ms = 0

    def handle_move(self):
        """Manejar el movimiento del jugador y eventos relacionados."""
        if self.game_over or self.paused:
            return {"status": "idle"}

        # guardar snapshot previo para interpolación
        self.prev_snake = list(self.snake.body)
        self.last_move_start_ms = self.now_ms()

        status = self.snake.step(settings.WRAP_AROUND)
        events = {"status": status}

        if status in ("wall", "self"):
            self.game_over = True
            self._on_game_over()
            return events

        if settings.USE_OBSTACLES and self.snake.head() in self.obstacles:
            self.game_over = True
            self._on_game_over()
            events["status"] = "obstacle"
            return events

        if self.food.pos and self.snake.head() == self.food.pos:
            self.score += 1
            self.snake.grow(1)
            if self.move_delay > settings.MIN_MOVE_DELAY:
                self.move_delay = max(settings.MIN_MOVE_DELAY,
                                    self.move_delay - settings.SPEED_STEP)
            utils.log_game_event("Comida consumida",
                                f"Puntos: {self.score}, Nueva velocidad: {self.move_delay}ms")
            self.food.respawn(self.snake.body + self.obstacles)
            events["ate_food"] = True
            self.spawn_power_if_needed()

        if self.powerup and self.powerup.pos and self.snake.head() == self.powerup.pos:
            utils.log_game_event("Powerup recogido", f"Tipo: {self.powerup.type}")
            self.apply_powerup(self.powerup.type)
            events["picked_powerup"] = self.powerup.type
            self.powerup = None

        return events

    def _on_game_over(self):
        # actualizar perfil: highscore, last_score, play_count y salvar
        if not hasattr(self, "profile"):
            self.profile = profiles.load_profile(self.profile_name) if profiles.profile_exists(self.profile_name) else {"name": self.profile_name}
        prev_high = self.profile.get("highscore", 0)

        is_new_record = self.score > prev_high
        if is_new_record:
            self.profile["highscore"] = self.score
            self.highscore = self.score
            utils.log_game_event("¡NUEVO RECORD!",
                                f"Puntuación final: {self.score} (anterior: {prev_high})")
        else:
            utils.log_game_event("Fin del juego", f"Puntuación: {self.score}, Record: {prev_high}")

        self.profile["last_score"] = self.score
        self.profile["play_count"] = self.profile.get("play_count", 0) + 1
        utils.log_info(f"Partidas jugadas: {self.profile['play_count']}")
        profiles.save_profile(self.profile_name, self.profile)

    def update(self):
        """Actualizar el estado del juego."""
        if self.active_power and self.now_ms() > self.power_end_time_ms:
            self.clear_power_effects()

    def set_direction(self, d):
        """Establecer la dirección del jugador."""
        self.snake.set_direction(d)

    def toggle_pause(self):
        """Alternar pausa."""
        self.paused = not self.paused

    def get_state(self):
        """Obtener el estado actual del juego."""
        return {
            "snake": list(self.snake.body),
            "prev_snake": list(self.prev_snake),
            "food": self.food.pos,
            "powerup": (self.powerup.type,
                        self.powerup.pos) if self.powerup and self.powerup.pos else None,
            "obstacles": list(self.obstacles),
            "score": self.score,
            "highscore": self.highscore,
            "move_delay": self.move_delay,
            "game_over": self.game_over,
            "paused": self.paused,
            "active_power": self.active_power,
            "last_move_start_ms": self.last_move_start_ms,
        }
