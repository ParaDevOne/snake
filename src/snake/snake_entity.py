"""A module for managing the snake in the game."""
# snake_entity.py

from snake import settings


class Snake:

    """Snake class representing the player snake in the game."""

    def __init__(self, initial=None):
        if initial is None:
            mid = (settings.COLUMNS // 2, settings.ROWS // 2)
            initial = [mid, (mid[0]-1, mid[1]), (mid[0]-2, mid[1])]
        self.body = list(initial)
        self.direction = (1, 0)
        self.grow_pending = 0

    def set_direction(self, d):
        """Establece la dirección de la serpiente."""
        # evita invertir 180 grados
        if (d[0], d[1]) == (-self.direction[0], -self.direction[1]):
            return
        self.direction = (d[0], d[1])

    def head(self):
        """Devuelve la posición de la cabeza de la serpiente."""
        return self.body[0]

    def step(self, wrap=False):
        """Avanza la serpiente en la dirección actual."""
        hx, hy = self.head()
        dx, dy = self.direction
        nx, ny = hx + dx, hy + dy

        if wrap:
            nx %= settings.COLUMNS
            ny %= settings.ROWS
        else:
            if not (0 <= nx < settings.COLUMNS and 0 <= ny < settings.ROWS):
                return 'wall'

        new_head = (nx, ny)
        if new_head in self.body:
            return 'self'

        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return 'ok'

    def grow(self, n=1):
        """Hace crecer la serpiente."""
        self.grow_pending += n


