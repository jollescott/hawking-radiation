import numpy as np
from particle import particle

class universe:
    def __init__(self):
        self.particles = [particle(False)]
        self.particles[0].force = np.array([10, 10])  # only for testing

    def update(self, elapsedTime):
        # update all particles
        for p in self.particles:
            p.update(elapsedTime)

    def spawn_particle_pair(self):
        pass

    def draw(self, surface):
        # draw all particles
        for p in self.particles:
            p.draw(surface)