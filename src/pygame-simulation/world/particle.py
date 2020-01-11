import numpy as np
import vector
from pygame import draw


class particle:
    radius = 10
    spawn_velocity = 100
    force_constant = 10000

    def __init__(self, is_positive, position=(0, 0), direction=(0, 0),
                 side_velocity=(0, 0)):
        self.is_positive = is_positive

        self.position = position
        self.velocity = vector.add(
            vector.change_length(direction, self.spawn_velocity),
            side_velocity
        )
        self.force = (0, 0)

        # array of particles that this particle will react with
        self.connected_particles = []

    def update(self, elapsed_time):
        # force needs to be reset every update
        self.force = (0, 0)

        # add force from all concted particles
        for p in self.connected_particles:
            self.force = vector.add(self.force, self.__calculate_force(p))

        self.velocity = np.add(self.velocity,
                               np.array(self.force) * elapsed_time)
        self.position = np.add(self.position, self.velocity * elapsed_time)

    def __calculate_force(self, other_particle):
        distance = vector.get_distance(self.position, other_particle.position)

        if distance < self.radius * 2:
            distance = self.radius * 2

        force_strength = self.force_constant / distance

        # invert force if the other particle has the same charge
        if self.is_positive == other_particle.is_positive:
            force_strength *= -1

        # vector pointing from this particle to the other particle
        force_vector = vector.point_from_to(
            self.position,
            other_particle.position
        )

        return vector.change_length(force_vector, force_strength)

    def draw(self, surface):
        # draw particle
        color = (150, 255, 150) if self.is_positive else (255, 150, 150)
        draw.circle(
            surface,
            color,
            np.array(self.position, dtype=int),
            self.radius
        )
        # draw velocity vector
        draw.line(
            surface,
            (255, 255, 255),
            self.position,
            vector.add(self.position, np.array(self.velocity) * 0.3),
            2
        )
        # draw force vector
        draw.line(
            surface,
            (100, 100, 255),
            self.position,
            vector.add(self.position, np.array(self.force) * 0.1),
            2
        )

    @staticmethod
    def collide(particle1, particle2):
        # only particles with different charge can colide
        if particle1.is_positive == particle2.is_positive:
            return False

        distance = vector.get_distance(particle1.position, particle2.position)
        return distance < particle.radius * 2
