# food.py
import random
import utils

class Food:
    def __init__(self, occupied, obstacles=None):
        self.obstacles = obstacles or []
        self.pos = None
        self.respawn(occupied)

    def respawn(self, occupied):
        pos = utils.random_free_cell(occupied, extra_forbidden=self.obstacles)
        self.pos = pos
        return pos

class PowerUp:
    TYPES = ("slow", "speed", "grow", "score")  # slow = reduce speed (slower), speed = faster, grow = +growth, score = bonus
    def __init__(self, occupied, obstacles=None):
        self.obstacles = obstacles or []
        self.type = random.choice(self.TYPES)
        self.pos = utils.random_free_cell(occupied, extra_forbidden=self.obstacles)
