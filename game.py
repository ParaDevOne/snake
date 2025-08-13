# game.py (renderer para pygame, usa logic.GameLogic)
import pygame
import settings
from logic import GameLogic

MOVE_EVENT = pygame.USEREVENT + 1

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(settings.FONT_NAME, 20)
        self.bigfont = pygame.font.Font(settings.FONT_NAME, 48)
        self.logic = GameLogic(load_highscore=True)
        # start timer with current delay
        pygame.time.set_timer(MOVE_EVENT, self.logic.move_delay)

    def reset_all(self):
        self.logic.reset()
        pygame.time.set_timer(MOVE_EVENT, self.logic.move_delay)

    def handle_move(self):
        events = self.logic.handle_move()
        # if move_delay changed, update timer
        pygame.time.set_timer(MOVE_EVENT, self.logic.move_delay)
        return events

    def update(self):
        self.logic.update()

    def draw_cell(self, cell, color):
        x, y = cell
        rect = pygame.Rect(x*settings.GRID_SIZE, y*settings.GRID_SIZE, settings.GRID_SIZE, settings.GRID_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def render(self):
        state = self.logic.get_state()
        # background
        self.screen.fill(settings.BG_COLOR)

        # obstacles
        if settings.USE_OBSTACLES:
            for ox, oy in state["obstacles"]:
                self.draw_cell((ox, oy), (120,120,120))

        # food
        if state["food"]:
            self.draw_cell(state["food"], settings.FOOD_COLOR)

        # powerup
        if state["powerup"]:
            ptype, ppos = state["powerup"]
            color = settings.POWERUP_COLORS.get(ptype, (200,200,200))
            self.draw_cell(ppos, color)

        # snake
        for i, seg in enumerate(state["snake"]):
            color = settings.SNAKE_HEAD if i == 0 else settings.SNAKE_BODY
            self.draw_cell(seg, color)

        hud = f"Puntos: {state['score']}  Mejor: {state['highscore']}  Vel(ms): {state['move_delay']}"
        if state['paused']:
            hud += "  [PAUSADO]"
        if state['active_power']:
            hud += f"  Power: {state['active_power'].upper()}"

        text = self.font.render(hud, True, (230,230,230))
        self.screen.blit(text, (8,8))

        if state['game_over']:
            go = self.bigfont.render("GAME OVER", True, (240,240,240))
            sub = self.font.render(f"Puntos: {state['score']} — R para reiniciar", True, (240,240,240))
            self.screen.blit(go, ((settings.WIDTH - go.get_width())//2, settings.HEIGHT//2 - 40))
            self.screen.blit(sub, ((settings.WIDTH - sub.get_width())//2, settings.HEIGHT//2 + 10))
