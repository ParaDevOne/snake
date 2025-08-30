""""A module for the game logic and mechanics."""
# logic.py
import random
import time

import src.snake.modules.profiles as profiles
import src.snake.system.settings as settings
import src.snake.system.utils as utils
from src.snake.core.food import Food, PowerUp
from src.snake.core.snake import Snake
from src.snake.modules.obstacles import ObstacleManager


class GameLogic:
    """Game logic and mechanics."""
    def __init__(self, load_highscore=True, profile_name=None):
        # profile_name: si None -> settings.DEFAULT_PROFILE
        self.profile_name = profile_name or settings.DEFAULT_PROFILE
        self.load_highscore_flag = load_highscore

        # Inicializar todos los atributos de instancia
        self.snake = None
        self.obstacles = []
        self.obstacle_manager = None
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
        try:
            utils.log_game_event("Game restarting")
            mid = (settings.COLUMNS // 2, settings.ROWS // 2)
            init = [mid, (mid[0]-1, mid[1]), (mid[0]-2, mid[1])]
            utils.log_info(f'[DEBUG] Initial snake: {init}')
            self.snake = Snake(init)
            if not self.snake or not hasattr(self.snake, 'body'):
                raise RuntimeError("Failed to initialize snake")
        except Exception as e:
            utils.log_error(f"Error in reset(): {str(e)}")
            self.game_over = True
            raise
        if settings.USE_OBSTACLES:
            self.obstacle_manager = ObstacleManager(
                grid_size=settings.GRID_SIZE,
                grid_width=settings.COLUMNS,
                grid_height=settings.ROWS,
                count=getattr(settings, 'OBSTACLE_COUNT', 8)
            )
            # Generar obstáculos aleatorios evitando la serpiente y la comida inicial
            self.obstacle_manager.generate_obstacles(self.snake.body, None)
            self.obstacles = self.obstacle_manager.get_obstacles()
            utils.log_info(f'[DEBUG] Obstacles generated: {self.obstacles}')
        else:
            self.obstacles = []
            self.obstacle_manager = None
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
        if not settings.POWERUP_ENABLED or self.snake is None:
            return
        if self.powerup is not None:
            return
        if random.random() < getattr(settings, "POWERUP_CHANCE", 0.12):
            snake_body = getattr(self.snake, 'body', [])
            food_pos = [self.food.pos] if self.food and hasattr(self.food, 'pos') and self.food.pos else []
            self.powerup = PowerUp(snake_body + food_pos + self.obstacles, self.obstacles)

    def apply_powerup(self, ptype):
        """Aplicar un power-up al jugador."""
        if self.snake is None:
            utils.log_warning("Cannot apply powerup: snake is None")
            return

        self.active_power = ptype
        self.power_end_time_ms = self.now_ms() + getattr(settings,
                                                        "POWERUP_DURATION_MS",
                                                        7000)
        if ptype == "slow":
            self.score += 1  # Slow Powerup: +1
            self.move_delay = min(999, self.move_delay + 80)
        elif ptype == "speed":
            self.score += 1   # Speed Powerup: +1
            self.move_delay = max(settings.MIN_MOVE_DELAY, self.move_delay - 60)
        elif ptype == "grow":
            self.score += 5   # Grow Powerup: +5
            self.snake.grow(3)
        elif ptype == "score":
            self.score += 20  # Score Powerup: +20

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
        if self.game_over or self.paused or not self.snake:
            return {"status": "idle"}

        try:
            # guardar snapshot previo para interpolación
            self.prev_snake = list(self.snake.body)
            self.last_move_start_ms = self.now_ms()
        except AttributeError as e:
            utils.log_error(f"Snake not properly initialized: {str(e)}")
            self.game_over = True
            return {"status": "error", "message": "Snake not properly initialized"}

        status = self.snake.step(settings.WRAP_AROUND)
        events = {"status": status}

        if status in ("wall", "self"):
            utils.log_info(f'[DEBUG] GameOver by status={status}, head={self.snake.head()}, snake={self.snake.body}')
            self.game_over = True
            self._on_game_over()
            return events

        if settings.USE_OBSTACLES and self.snake.head() in self.obstacles:
            utils.log_info(f'[DEBUG] GameOver by obstacle: head={self.snake.head()}, obstacles={self.obstacles}')
            self.game_over = True
            self._on_game_over()
            events["status"] = "obstacle"
            return events

        if self.food is not None and self.food.pos and self.snake.head() == self.food.pos:
            self.score += 1  # Food: +1
            self.snake.grow(1)
            if self.move_delay > settings.MIN_MOVE_DELAY:
                self.move_delay = max(settings.MIN_MOVE_DELAY,
                                    self.move_delay - settings.SPEED_STEP)
            utils.log_game_event("Comida consumida",
                                f"Puntos: {self.score}, Nueva velocidad: {self.move_delay}ms")
            self.food.respawn(self.snake.body + self.obstacles)
            events["ate_food"] = "true"
            self.spawn_power_if_needed()

        if self.powerup is not None and self.powerup.pos and self.snake.head() == self.powerup.pos:
            utils.log_game_event("Powerup recogido", f"Tipo: {self.powerup.type}")
            self.apply_powerup(self.powerup.type)
            events["picked_powerup"] = self.powerup.type
            self.powerup = None

        return events

    def _on_game_over(self):
        # actualizar perfil: highscore, last_score, play_count y salvar
        if not hasattr(self, "profile"):
            self.profile = profiles.load_profile(self.profile_name) if profiles.profile_exists(self.profile_name) else {"name": self.profile_name}
        prev_high = int(self.profile.get("highscore", 0))

        is_new_record = self.score > prev_high
        if is_new_record:
            self.profile["highscore"] = self.score
            self.highscore = self.score
            utils.log_game_event("NEW HIGHSCORE!",
                                f"Final score: {self.score} (previous: {prev_high})")
        else:
            utils.log_game_event("Game over", f"Score: {self.score}, Record: {prev_high}")

        self.profile["last_score"] = self.score
        self.profile["play_count"] = int(self.profile.get("play_count", 0)) + 1
        utils.log_info(f"Games played: {self.profile['play_count']}")
        profiles.save_profile(self.profile_name, self.profile)

    def update(self):
        """Actualizar el estado del juego."""
        if self.active_power and self.now_ms() > self.power_end_time_ms:
            self.clear_power_effects()

    def set_direction(self, d):
        """Establecer la dirección del jugador."""
        if self.snake is None:
            utils.log_warning("Attempted to set direction before snake was initialized")
            return
        self.snake.set_direction(d)

    def toggle_pause(self):
        """Alternar pausa."""
        self.paused = not self.paused

    def get_state(self):
        """Obtener el estado actual del juego."""
        return {
            "snake": list(self.snake.body) if self.snake else [],
            "prev_snake": list(self.prev_snake),
            "food": self.food.pos if hasattr(self, 'food') and self.food else None,
            "powerup": (self.powerup.type,
                        self.powerup.pos) if hasattr(self, 'powerup') and self.powerup and self.powerup.pos else None,
            "obstacles": list(self.obstacles) if hasattr(self, 'obstacles') else [],
            "score": self.score,
            "highscore": self.highscore,
            "move_delay": self.move_delay,
            "game_over": self.game_over,
            "paused": self.paused,
            "active_power": self.active_power,
            "last_move_start_ms": self.last_move_start_ms,
        }
