import numpy as np
import pygame


class particle:
    radius = 10

    def __init__(self, isPositive, position=(0, 0), velocity=(0, 0)):
        self.isPositive = isPositive

        self.position = position
        self.velocity = velocity
        self.force = np.array((0, 0))

    def update(self, elapsedTime):
        self.velocity = np.add(self.velocity, self.force * elapsedTime)
        self.position = np.add(self.position, self.velocity * elapsedTime)

    def draw(self, surface):
        color = (0, 255, 0) if self.isPositive else (255, 0, 0)
        pygame.draw.circle(
            surface,
            color,
            np.array(self.position, dtype=int),
            self.radius
        )
