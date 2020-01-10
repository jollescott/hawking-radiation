import numpy as np
import pygame
import vector


class particle:
    radius = 10
    spawn_velocity = 100
    force_constant = 10000

    def __init__(self, isPositive, position=(0, 0), direction=(0, 0)):
        self.isPositive = isPositive

        self.position = position
        self.velocity = vector.change_length(direction, self.spawn_velocity)
        self.force = (0, 0)

        # array of particles that this particle will react with
        self.connected_particles = []

    def update(self, elapsedTime):
        # force needs to be reset every update
        self.force = (0, 0)

        # add force from all concted particles
        for p in self.connected_particles:
            self.force = vector.add(self.force, self.__calculate_force(p))

        self.velocity = np.add(self.velocity,
                               np.array(self.force) * elapsedTime)
        self.position = np.add(self.position, self.velocity * elapsedTime)

    def __calculate_force(self, other_particle):
        distance = vector.get_distance(self.position, other_particle.position)

        if distance < self.radius * 2:
            distance = self.radius * 2

        force_strength = self.force_constant / distance

        # invert force if the other particle has the same charge
        if self.isPositive == other_particle.isPositive:
            force_strength *= -1

        # vector pointing from this particle to the other particle
        force_vector = vector.point_from_to(
            self.position,
            other_particle.position
        )

        return vector.change_length(force_vector, force_strength)

    def draw(self, surface):
        # draw particle
        color = (0, 255, 0) if self.isPositive else (255, 0, 0)
        pygame.draw.circle(
            surface,
            color,
            np.array(self.position, dtype=int),
            self.radius
        )
        # draw velocity vector
        pygame.draw.line(
            surface,
            (255, 255, 255),
            self.position,
            vector.add(self.position, np.array(self.velocity) * 0.3),
            4
        )
        # draw force vector
        pygame.draw.line(
            surface,
            (100, 100, 255),
            self.position,
            vector.add(self.position, np.array(self.force) * 0.1),
            3
        )
