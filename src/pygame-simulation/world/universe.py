import time
import vector
import random
import math
from world.particle import particle
from world.black_hole import black_hole
import formulas
import numpy as np


class universe:
    min_spawn_time = 0.1
    max_spawn_time = 0.5

    def __init__(self, size):
        self._size = size
        self.black_hole = black_hole(np.array(size) * 0.5, formulas.Ms * 0.05)
        print(self.black_hole.get_radius())
        self.particles = []
        self.__particle_spawn_timer = time.perf_counter()

    def update(self, elapsed_time):
        self.black_hole.update(elapsed_time)

        # loop thorugh all particles
        index = 0
        while index < len(self.particles):
            p = self.particles[index]
            # loop thorugh all particles connected to this particle
            cp_index = 0
            while cp_index < len(p.connected_particles):
                cp = p.connected_particles[cp_index]
                # remove particles if collided
                if particle.collide(p, cp):
                    self.particles.pop(index)
                    self.particles.remove(cp)
                    print("particle pair removed")
                    break
                cp_index += 1

            # update particle
            p.update(
                elapsed_time,
                (0, 0)  # self.black_hole.calculate_particle_force(p)
            )
            index += 1

        self.__particle_spawn_timer -= elapsed_time
        # check if it is time to spawn a particle pair
        if self.__particle_spawn_timer <= 0 and self.black_hole.mass > 0:
            self.spawn_particle_pair()
            self.__particle_spawn_timer = random.uniform(self.min_spawn_time,
                                                         self.max_spawn_time)

    def spawn_particle_pair(self):
        spawn_on_horizon_chance = 0.15
        on_horizon = random.uniform(0, 1) < spawn_on_horizon_chance

        #
        # p_??? data for positive particle
        # n_??? data for negative particle
        #

        # spawn on event horizon
        if (on_horizon):
            # center start position
            center = vector.add(
                self.black_hole.position,
                vector.rand_vector_rot(self.black_hole.get_radius())
            )

            b_rot = vector.get_rotation(
                vector.point_from_to(center, self.black_hole.position)
            )
            side_rot = random.uniform(-math.pi / 2, math.pi / 2)
            # start directions
            p_dir = vector.new_vector(
                1,
                b_rot + math.pi + side_rot
            )
            n_dir = vector.new_vector(
                1,
                b_rot - side_rot
            )

            # side velocity
            side_vel = (0, 0)

        # spawn outside event horizon
        else:
            b_radius = self.black_hole.get_radius()
            min_horizon_dist = 50
            max_horizon_dist = max(self._size) / 2 - b_radius

            # center start postition
            center = vector.add(
                self.black_hole.position,
                vector.rand_vector_rot(
                    random.uniform(
                        b_radius + min_horizon_dist,
                        b_radius + max_horizon_dist
                    )
                )
            )

            # start directions
            p_dir = vector.rand_vector_rot(1)
            n_dir = vector.invert(p_dir)

            # side velocity
            max_vel = 100
            side_vel = vector.new_vector(
                random.uniform(-max_vel, max_vel),
                vector.get_rotation(p_dir) + math.pi/2
            )

        # start positions (the particles can't overlap when spawned)
        p_pos = vector.add(
            center,
            vector.change_length(p_dir, particle.radius)
        )
        n_pos = vector.add(
            center,
            vector.change_length(n_dir, particle.radius + 1)
        )

        # create particles
        p_par = particle(True, p_pos, p_dir, side_vel)
        n_par = particle(False, n_pos, n_dir, side_vel)

        # spawn on event horizon
        if (on_horizon):
            # add to universe/black_hole
            self.particles.append(p_par)
            self.black_hole.eat_particle(n_par)

        # spawn outside event horizon
        else:
            # connect particle pair
            p_par.connected_particles.append(n_par)
            n_par.connected_particles.append(p_par)

            # add to universe
            self.particles.extend([p_par, n_par])

        # connect with all universe particles
        # par.connected_particles.extend(self.particles)
        # inv_par.connected_particles.extend(self.particles)
        # for p in self.particles:
        #     p.connected_particles.extend([p_par, n_par])

        print("particle pair spawned at " + str(center))

    def draw(self, surface):
        self.black_hole.draw(surface)
        # draw all particles
        for p in self.particles:
            p.draw(surface)
