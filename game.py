# game.py
import pygame
import settings
from snake import Snake
from food import Food, PowerUp
import utils

MOVE_EVENT = pygame.USEREVENT + 1

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(settings.FONT_NAME, 20)
        self.bigfont = pygame.font.Font(settings.FONT_NAME, 48)
        self.reset_all()

    def reset_all(self):
        mid = (settings.COLUMNS // 2, settings.ROWS // 2)
        init = [mid, (mid[0]-1, mid[1]), (mid[0]-2, mid[1])]
        self.snake = Snake(init)
        self.obstacles = settings.OBSTACLES if settings.USE_OBSTACLES else []
        self.food = Food(self.snake.body + self.obstacles, self.obstacles)
        self.powerup = None
        self.score = 0
        self.move_delay = settings.INIT_MOVE_DELAY
        self.game_over = False
        self.paused = False
        # powerup active state
        self.active_power = None
        self.power_end_time = 0

        # load highscore
        data = utils.load_json(settings.HIGH_SCORE_FILE, {"highscore": 0})
        self.highscore = data.get("highscore", 0)

        # start timer event
        pygame.time.set_timer(MOVE_EVENT, self.move_delay)

    def spawn_power_if_needed(self):
        import random
        if not settings.POWERUP_ENABLED:
            return
        if self.powerup is not None:
            return
        if random.random() < settings.POWERUP_CHANCE:
            self.powerup = PowerUp(self.snake.body + [self.food.pos] + self.obstacles, self.obstacles)

    def apply_powerup(self, ptype):
        now = pygame.time.get_ticks()
        self.active_power = ptype
        self.power_end_time = now + settings.POWERUP_DURATION_MS

        if ptype == "slow":
            # make snake slower (increase delay), cap
            self.move_delay = min(999, self.move_delay + 80)
        elif ptype == "speed":
            self.move_delay = max(settings.MIN_MOVE_DELAY, self.move_delay - 60)
        elif ptype == "grow":
            self.snake.grow(3)
        elif ptype == "score":
            self.score += 3

        # update timer with new delay
        pygame.time.set_timer(MOVE_EVENT, self.move_delay)

    def clear_power_effects(self):
        # called when duration ends; revert to baseline-ish behavior
        if self.active_power == "slow":
            # try to revert somewhat
            self.move_delay = max(settings.MIN_MOVE_DELAY, self.move_delay - 80)
        elif self.active_power == "speed":
            self.move_delay = min(settings.INIT_MOVE_DELAY, self.move_delay + 60)
        # grow and score are instant effects
        self.active_power = None
        pygame.time.set_timer(MOVE_EVENT, self.move_delay)

    def handle_move(self):
        if self.game_over or self.paused:
            return
        status = self.snake.step(settings.WRAP_AROUND)
        if status in ("wall", "self"):
            self.game_over = True
            if self.score > self.highscore:
                self.highscore = self.score
                utils.save_json(settings.HIGH_SCORE_FILE, {"highscore": self.highscore})
            return

        # collision with obstacles
        if settings.USE_OBSTACLES and self.snake.head() in self.obstacles:
            self.game_over = True
            if self.score > self.highscore:
                self.highscore = self.score
                utils.save_json(settings.HIGH_SCORE_FILE, {"highscore": self.highscore})
            return

        # eat food
        if self.food.pos and self.snake.head() == self.food.pos:
            self.score += 1
            self.snake.grow(1)
            # speed up
            if self.move_delay > settings.MIN_MOVE_DELAY:
                self.move_delay = max(settings.MIN_MOVE_DELAY, self.move_delay - settings.SPEED_STEP)
            # respawn food
            self.food.respawn(self.snake.body + self.obstacles)
            # maybe spawn powerup
            self.spawn_power_if_needed()
            pygame.time.set_timer(MOVE_EVENT, self.move_delay)

        # pick powerup
        if self.powerup and self.snake.head() == self.powerup.pos:
            self.apply_powerup(self.powerup.type)
            self.powerup = None

    def update(self):
        # handle powerup duration expiration
        if self.active_power:
            if pygame.time.get_ticks() > self.power_end_time:
                self.clear_power_effects()

    def draw_cell(self, cell, color):
        x, y = cell
        rect = pygame.Rect(x*settings.GRID_SIZE, y*settings.GRID_SIZE, settings.GRID_SIZE, settings.GRID_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def render(self):
        # background
        self.screen.fill(settings.BG_COLOR)

        # draw obstacles
        if settings.USE_OBSTACLES:
            for ox, oy in self.obstacles:
                self.draw_cell((ox, oy), (120,120,120))

        # draw food
        if self.food.pos:
            self.draw_cell(self.food.pos, settings.FOOD_COLOR)

        # draw powerup
        if self.powerup and self.powerup.pos:
            color = settings.POWERUP_COLORS.get(self.powerup.type, (200,200,200))
            self.draw_cell(self.powerup.pos, color)

        # draw snake
        for i, seg in enumerate(self.snake.body):
            color = settings.SNAKE_HEAD if i == 0 else settings.SNAKE_BODY
            self.draw_cell(seg, color)

        # HUD
        hud = f"Puntos: {self.score}  Mejor: {self.highscore}  Vel(ms): {self.move_delay}"
        if self.paused:
            hud += "  [PAUSADO]"
        if self.active_power:
            hud += f"  Power: {self.active_power.upper()}"

        text = self.font.render(hud, True, (230,230,230))
        self.screen.blit(text, (8,8))

        if self.game_over:
            go = self.bigfont.render("GAME OVER", True, (240,240,240))
            sub = self.font.render(f"Puntos: {self.score} — R para reiniciar", True, (240,240,240))
            self.screen.blit(go, ((settings.WIDTH - go.get_width())//2, settings.HEIGHT//2 - 40))
            self.screen.blit(sub, ((settings.WIDTH - sub.get_width())//2, settings.HEIGHT//2 + 10))

    # input handling (key presses) done externally in main loop or here as helper
