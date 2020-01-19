import time
from animation import vector
import random
import math
from animation.world.particle import particle
from animation.world.black_hole import black_hole
import numpy as np


class universe:
    min_spawn_time = 0.10
    max_spawn_time = 0.5
    spawn_on_horizon_chance = 0.15
    particle_spawn_velocity = 100

    def __init__(self, size, scale):
        self._size = size
        self.black_hole = black_hole(np.array(size) * 0.5, 0, scale)
        print(self.black_hole.get_radius())
        self._particles = []
        self.__particle_spawn_timer = time.perf_counter()

    def update(self, elapsed_time):
        # loop thorugh all particles
        index = 0
        while index < len(self._particles):
            p = self._particles[index]
            cp = p.connected_particle
            # remove if collided
            if cp and particle.collide(p, cp):
                self._particles.pop(index)
                self._particles.remove(cp)
            # update particle
            p.update(
                elapsed_time,
                (0, 0)  # self.black_hole.calculate_particle_force(p)
            )
            index += 1

        self.__particle_spawn_timer -= elapsed_time
        # check if it is time to spawn a particle pair
        if self.__particle_spawn_timer <= 0 and self.black_hole.mass > 0:
            self._spawn_particle_pair()
            self.__particle_spawn_timer = random.uniform(self.min_spawn_time,
                                                         self.max_spawn_time)

        if self.black_hole.mass > 0:
            self.black_hole.update(elapsed_time, self._particles)

    def _spawn_particle_pair(self):
        """
        Spawns a pair of particles with opposite charge.
        """
        on_horizon = random.uniform(0, 1) < self.spawn_on_horizon_chance

        particles = (
            self._create_on_event_horizon() if on_horizon
            else self._create_outside_event_horizon()
        )
        self._particles.extend(particles)

    def _create_on_event_horizon(self):
        """
        Returns a pair of particles with opposite charge positioned on the
        event horizon.
        """
        # spawn center relative to the center of the black hole
        spawn_offset = vector.rand_vector_rot(self.black_hole.get_radius())

        spawn_center = vector.add(self.black_hole.position, spawn_offset)

        rand_rot = random.choice((-1, 1)) * random.uniform(math.pi / 4,
                                                           math.pi / 2)

        reg_par = particle(
            # charge
            True,
            # position
            vector.add(
                spawn_center,
                vector.change_length(spawn_offset, particle.radius)
            ),
            # velocity
            vector.new_vector(
                self.particle_spawn_velocity,
                vector.get_rotation(spawn_offset) + rand_rot
            )
        )
        neg_par = particle(
            # charge
            False,
            # position
            vector.subtract(
                spawn_center,
                vector.change_length(spawn_offset, particle.radius)
            ),
            # velocity
            vector.new_vector(
                self.particle_spawn_velocity,
                vector.get_rotation(spawn_offset) + math.pi - rand_rot
            )
        )

        reg_par.connected_particle = neg_par
        neg_par.connected_particle = reg_par

        return (reg_par, neg_par)

    def _create_outside_event_horizon(self):
        """
        Returns a pair of particles with opposite charge positioned outside the
        event horizon.
        """
        min_horizon_dist = 40
        spawn_center = vector.add(
            self.black_hole.position,
            vector.rand_vector_rot(
                random.uniform(
                    self.black_hole.get_radius() + min_horizon_dist,
                    max(self._size) / 2
                )
            )
        )

        direction_rot = random.uniform(0, 2 * math.pi)

        max_side_velocity = self.particle_spawn_velocity / 2
        side_velocity = vector.new_vector(
            random.uniform(-max_side_velocity, max_side_velocity),
            direction_rot + math.pi / 2
        )

        reg_par = particle(
            # charge
            True,
            # position
            vector.add(
                spawn_center,
                vector.new_vector(particle.radius + 1, direction_rot)
            ),
            # velocity
            vector.add(
                vector.new_vector(self.particle_spawn_velocity, direction_rot),
                side_velocity
            )
        )
        neg_par = particle(
            # charge
            False,
            # position
            vector.add(
                spawn_center,
                vector.new_vector(particle.radius, direction_rot + math.pi)
            ),
            # velocity
            vector.add(
                vector.new_vector(
                    self.particle_spawn_velocity,
                    direction_rot + math.pi
                ),
                side_velocity
            )
        )

        reg_par.connected_particle = neg_par
        neg_par.connected_particle = reg_par

        return (reg_par, neg_par)

    def draw(self, surface):
        self.black_hole.draw(surface)
        # draw all particles
        for p in self._particles:
            p.draw(surface)
