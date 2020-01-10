import numpy as np
import pygame


class particle:
    def __init__(self, isPositive):
        self.isPositive = isPositive

        self.radius = 10

        self.position = np.array([30, 30])
        self.velocity = np.array([0, 0])
        self.force = np.array([0, 0])

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
