import arcade
import random

SPEED = 200
THICKNESS = 20

GAP = 180
HALF_GAP = GAP / 2


class Pipe:
    pos: list

    def __init__(self, x: float, y: float):
        self.pos = [x, y]

    def randomize(self, max_height: float, x: float = 800):
        max_height -= GAP
        self.pos = [
            x,
            (random.random() * max_height) + HALF_GAP
        ]

    def on_update(self, dt) -> bool:
        """Returns True if needs reassignment, otherwise false."""
        self.pos[0] -= SPEED * dt

        if self.pos[0] + THICKNESS <= 0:
            return True

        return False

    def on_draw(self):
        # Top Half
        arcade.draw_line(
            self.pos[0], 600,
            self.pos[0], self.pos[1] + HALF_GAP,
            arcade.color.WHITE,
            THICKNESS)

        # Bottom Half
        arcade.draw_line(
            self.pos[0], 0,
            self.pos[0], self.pos[1] - HALF_GAP,
            arcade.color.WHITE,
            THICKNESS)
