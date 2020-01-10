import time
import vector
from particle import particle


class universe:
    spawn_time = 3

    def __init__(self, size):
        self._size = size
        self.particles = []
        self.__particle_spawn_timer = time.perf_counter()

    def update(self, elapsed_time):
        # update all particles
        for p in self.particles:
            p.update(elapsed_time)

        self.__particle_spawn_timer -= elapsed_time
        # check it it is time to spawn a particle pair
        if self.__particle_spawn_timer <= 0:
            self.spawn_particle_pair()
            self.__particle_spawn_timer = self.spawn_time

    def spawn_particle_pair(self):
        # start directions
        way = vector.rand_vector_rot(1)
        inv_way = vector.invert(way)

        # center start postition
        center = vector.rand_vector_pos(0, self._size[0], 0, self._size[1])
        # start positions (the particles can't overlap when spawned)
        pos = vector.add(center, vector.change_length(way, particle.radius))
        inv_pos = vector.add(center, vector.change_length(inv_way,
                                                          particle.radius))

        # create particles
        par = particle(True, pos, way)
        inv_par = particle(False, inv_pos, inv_way)

        par.connected_particles.append(inv_par)
        inv_par.connected_particles.append(par)

        self.particles.extend([par, inv_par])

    def draw(self, surface):
        # draw all particles
        for p in self.particles:
            p.draw(surface)
