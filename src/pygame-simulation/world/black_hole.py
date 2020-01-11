import numpy as np
import math
from pygame import draw


class black_hole:
    event_horizon_force = 100

    def __init__(self, position, mass):
        self.position = position
        self.mass = mass

    def get_radius(self):
        return math.sqrt(self.mass / self.event_horizon_force)

    def update(self, elapsed_time):
        pass

    def draw(self, surface):
        draw.circle(
            surface,
            (255, 255, 0),
            np.array(self.position, dtype=int),
            int(self.get_radius()),
            1
        )
