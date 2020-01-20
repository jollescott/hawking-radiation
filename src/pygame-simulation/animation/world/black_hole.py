import numpy as np
from animation import vector
from pygame import draw
import formulas


class black_hole:
    gravity_constant = 0.000001
    event_horizon_force = 100
    mass_los_per_particle = 10000

    def __init__(self, position, mass, scale):
        self.position = position
        self.mass = mass
        self.scale = scale
        self.eaten_particles = []

    def get_radius(self):
        return formulas.schwarzschild_radius(self.mass) * self.scale

    def eat_particle(self, particle):
        # disconnect with connected particle
        if particle.connected_particle:
            particle.connected_particle.connected_particle = None
            particle.connected_particle = None

        # # set particle velcity towards black hole center
        # particle.velocity = vector.change_length(
        #     vector.point_from_to(
        #         particle.position,
        #         self.position
        #     ),
        #     vector.get_length(particle.velocity)
        # )

        self.eaten_particles.append(particle)

    def calculate_particle_force(self, particle):
        return (
            vector.change_length(
                vector.point_from_to(
                    particle.position,
                    self.position
                ),
                formulas.gravitational_force(
                    self.mass,
                    particle.mass,
                    vector.get_distance(
                        self.position,
                        particle.position
                    )
                ) * self.scale
            )
        )

    def update(self, elapsed_time, particles):
        # Eat particles
        index = 0
        while index < len(particles):
            p = particles[index]
            if not p.is_positive and vector.get_distance(
                    self.position, p.position) < self.get_radius():
                self.eat_particle(p)
                particles.pop(index)
            index += 1

        # Updates all particles and removes them if they have reached
        # the center of the black hole.
        index = 0
        while index < len(self.eaten_particles):
            p = self.eaten_particles[index]
            if self.__should_be_removed(p):
                self.eaten_particles.pop(index)
                self.mass -= self.mass_los_per_particle
            else:
                index += 1

            pf = self.calculate_particle_force(p)
            max_vel = vector.get_length(pf) / 2
            # limit particle velocity to pervent infinit orbit
            # around black hole
            if vector.get_length(p.velocity) > max_vel:
                p.velocity = vector.change_length(p.velocity, max_vel)
            p.update(
                elapsed_time,
                pf
            )

    def __should_be_removed(self, particle):
        min_dist = 10
        return vector.get_distance(
            self.position,
            particle.position
        ) < min_dist

    def draw(self, surface):
        radius = int(self.get_radius())
        if radius > 0:
            draw.circle(
                surface,
                (255, 255, 0),
                np.array(self.position, dtype=int),
                radius,
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
