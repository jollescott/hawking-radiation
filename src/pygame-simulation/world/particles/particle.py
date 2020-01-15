import numpy as np
import vector
from pygame import draw
from trail import trail


class particle:
    radius = 5
    spawn_velocity = 100
    force_constant = 7000
    mass = 3 * 10**-13

    def __init__(self, is_positive, position, velocity):
        self.is_positive = is_positive
        self.position = position
        self.velocity = velocity

        self.force = (0, 0)
        self.life_time = 0
        self.trail = trail()

        # particle that this particle will react with
        self.connected_particle

    def update(self, elapsed_time, force):
        self.life_time += elapsed_time

        # force needs to be reset every update
        self.force = force

        if self.connected_particle:
            # add force from the connected particle
            self.force = vector.add(
                self.force,
                self.__calculate_force(self.connected_particle)
            )

        self.velocity = np.add(
            self.velocity,
            np.array(self.force) * elapsed_time
        )
        self.position = np.add(
            self.position,
            self.velocity * elapsed_time
        )

        self.trail.add_point(self.position)

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
        # draw trail
        self.trail.draw(surface)

        position = np.array(self.position, dtype=int)
        # draw particle
        color = (150, 150, 255) if self.is_positive else (255, 150, 150)
        draw.circle(
            surface,
            color,
            position,
            self.radius
        )
        # # draw velocity vector
        # draw.line(
        #     surface,
        #     (255, 255, 255),
        #     position,
        #     np.array(
        #         vector.add(self.position, np.array(self.velocity) * 0.3),
        #         dtype=int
        #     ),
        #     2
        # )
        # # draw force vector
        # draw.line(
        #     surface,
        #     (100, 255, 100),
        #     position,
        #     np.array(
        #         vector.add(self.position, np.array(self.force) * 0.1),
        #         dtype=int
        #     ),
        #     2
        # )

    @staticmethod
    def collide(particle1, particle2):
        # only particles with different charge can colide
        if particle1.is_positive == particle2.is_positive:
            return False

        distance = vector.get_distance(particle1.position, particle2.position)
        return distance < particle.radius * 2
