"""Snake module - Handles snake movement and collision logic."""


class Snake:
    """Represents the snake in the game."""

    def __init__(self, start_pos=(0, 0), start_direction=(1, 0), initial_size=3):
        """Initialize the snake.

        Args:
            start_pos (tuple): Starting position (x, y)
            start_direction (tuple): Initial direction (dx, dy)
            initial_size (int): Initial length of the snake
        """
        self.direction = start_direction
        self.body = []
        # Create initial body
        for i in range(initial_size):
            x = start_pos[0] - (self.direction[0] * i)
            y = start_pos[1] - (self.direction[1] * i)
            self.body.append((x, y))

    def head(self):
        """Get the position of the snake's head."""
        return self.body[0] if self.body else None

    def step(self, wrap_around=False):
        """Move the snake one step in the current direction.

        Args:
            wrap_around (bool): If True, snake wraps around screen edges

        Returns:
            str: Movement result ('ok', 'wall', or 'self')
        """
        if not self.body:
            return "error"

        # Calculate new head position
        new_x = self.body[0][0] + self.direction[0]
        new_y = self.body[0][1] + self.direction[1]
        new_head = (new_x, new_y)

        # Check for collisions with self
        if new_head in self.body[:-1]:
            return "self"

        # Add new head
        self.body.insert(0, new_head)
        self.body.pop()  # Remove tail

        return "ok"

    def grow(self, amount=1):
        """Increase the snake's length.

        Args:
            amount (int): Number of segments to add
        """
        for _ in range(amount):
            # Add new segment at current tail position
            self.body.append(self.body[-1])

    def set_direction(self, new_direction):
        """Set a new direction for the snake.

        Args:
            new_direction (tuple): New direction as (dx, dy)
        """
        # Prevent 180-degree turns
        if (self.direction[0] * -1, self.direction[1] * -1) != new_direction:
            self.direction = new_direction
