import time
import vector
import random
import math
from particle import particle


class universe:
    min_spawn_time = 0.1
    max_spawn_time = 0.5

    def __init__(self, size):
        self._size = size
        self.particles = []
        self.__particle_spawn_timer = time.perf_counter()

    def update(self, elapsed_time):
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
            p.update(elapsed_time)
            index += 1

        self.__particle_spawn_timer -= elapsed_time
        # check if it is time to spawn a particle pair
        if self.__particle_spawn_timer <= 0:
            self.spawn_particle_pair()
            self.__particle_spawn_timer = random.uniform(self.min_spawn_time,
                                                         self.max_spawn_time)

    def spawn_particle_pair(self):
        # start directions
        way = vector.rand_vector_rot(1)
        inv_way = vector.invert(way)

        # center start postition
        center = vector.rand_vector_pos(0, self._size[0], 0, self._size[1])
        # start positions (the particles can't overlap when spawned)
        pos = vector.add(center, vector.change_length(way, particle.radius))
        inv_pos = vector.add(center, vector.change_length(inv_way,
                                                          particle.radius + 1))

        # side velocity
        max_vel = 100
        side_vel = vector.new_vector(random.uniform(-max_vel, max_vel),
                                     vector.get_rotation(way) + math.pi / 2)

        # create particles
        par = particle(True, pos, way, side_vel)
        inv_par = particle(False, inv_pos, inv_way, side_vel)

        # connect particle pair
        par.connected_particles.append(inv_par)
        inv_par.connected_particles.append(par)

        # connect with all universe particles
        # par.connected_particles.extend(self.particles)
        # inv_par.connected_particles.extend(self.particles)
        # for p in self.particles:
        #     p.connected_particles.extend([par, inv_par])

        # add to universe
        self.particles.extend([par, inv_par])

        print("particle pair spawned at " + str(center))

    def draw(self, surface):
        # draw all particles
        for p in self.particles:
            p.draw(surface)
