import numpy as np
import math
import vector
from pygame import draw


class black_hole:
    event_horizon_force = 100

    def __init__(self, position, mass):
        self.position = position
        self.mass = mass
        self.eaten_particles = []

    def get_radius(self):
        return math.sqrt(self.mass / self.event_horizon_force)

    def eat_particle(self, particle):
        # disconnect with all connected particles
        for p in particle.connected_particles:
            p.connected_particles.remove(particle)
        particle.connected_particles = []

        # set particle velcity towards black hole center
        particle.velocity = vector.change_length(
            vector.point_from_to(
                particle.position,
                self.position
            ),
            vector.get_length(particle.velocity)
        )

        self.eaten_particles.append(particle)

    def update(self, elapsed_time):
        # Updates all particles and removes them if they have reached
        # the center of the black hole.
        index = 0
        while index < len(self.eaten_particles):
            p = self.eaten_particles[index]
            if self.__should_be_removed(p):
                self.eaten_particles.pop(index)
            else:
                index += 1

            p.update(elapsed_time)

    def __should_be_removed(self, particle):
        min_dist = 5
        return vector.get_distance(
            self.position,
            particle.position
        ) < min_dist

    def draw(self, surface):
        draw.circle(
            surface,
            (255, 255, 0),
            np.array(self.position, dtype=int),
            int(self.get_radius()),
            1
        )
        # draw all eaten particles
        for p in self.eaten_particles:
            p.draw(surface)

    def is_position_on_horizon(self, position):
        margin = 100
        radius = self.get_radius()
        distance = vector.get_distance(self.position, position)
        return True
        return radius - margin < distance < radius + margin
