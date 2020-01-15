import random
import vector
import math
from particle import particle


class particle_controller:
    particle_evaporation_time = 3
    spawn_on_horizon_chance = 0.15

    def __init__(self):
        self._particles = []

    def update(self, elapsed_time):
        for p in self._particles:
            self._update_particle(elapsed_time, p)

        # TODO: spawn particles

    def _update_particle(self, elapsed_time, particle):
        particle.update(elapsed_time)

        if particle.life_time >= self.particle_evaporation_time:
            # TODO: remove particle
            pass

    def _spawn_particle_pair(self):
        """
        Spawns a pair of particles with opposite charge.
        """

        on_horizon = random.uniform(0, 1) < self.spawn_on_horizon_chance

        particles = (
            self._spawn_on_event_horizon() if on_horizon
            else self._spawn_outside_event_horizon()
        )
        self._particles.extend(particles)

    def _create_on_event_horizon(self, black_hole):
        """
        Returns a pair of particles with opposite charge positioned on the
        event horizon.
        """

        velocity = 20

        # Spawn position relative to the center of the black hole
        spawn_offset = vector.rand_vector_rot(black_hole.get_radius())

        spawn_position = vector.add(black_hole.position, spawn_offset)

        rand_rot = math.uniform(-math.pi / 2, math.pi / 2)

        reg_par = particle(
            # Charge
            True,
            # Position
            vector.add(
                spawn_position,
                vector.change_length(spawn_offset, particle.radius / 2)
            ),
            # Velocity
            vector.new_vector(
                velocity,
                vector.get_rotation(spawn_offset) + rand_rot
            )
        )
        neg_par = particle(
            # Charge
            False,
            # Position
            vector.subtract(
                spawn_offset,
                vector.change_length(spawn_offset, particle.radius / 2)
            ),
            # Velocity
            vector.new_vector(
                velocity,
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
        # TODO: this
        pass

    def draw_particles(self, surface):
        for p in self._particles:
            p.draw(surface)
