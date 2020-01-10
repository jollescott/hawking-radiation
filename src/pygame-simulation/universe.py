import time
import vector
from particle import particle


class universe:
    spawnTime = 3
    particleStartVel = 100

    def __init__(self, size):
        self._size = size

        self.particles = []
        self._nextSpawn = time.perf_counter()

    def update(self, elapsedTime):
        # update all particles
        for p in self.particles:
            p.update(elapsedTime)

        # check it it is time to spawn a particle pair
        if time.perf_counter() >= self._nextSpawn:
            self.spawn_particle_pair()
            self._nextSpawn = time.perf_counter() + self.spawnTime

    def spawn_particle_pair(self):
        # start velocities
        vel = vector.rand_vector_rot(self.particleStartVel)
        inv_vel = vector.invert(vel)

        # center start postition
        center = vector.rand_vector_pos(0, self._size[0], 0, self._size[1])
        # start positions (the particles can't overlap when spawned)
        pos = vector.add(center, vector.change_length(vel, particle.radius))
        inv_pos = vector.add(center, vector.change_length(inv_vel,
                                                          particle.radius))

        # create particles
        par = particle(True, pos, vel)
        inv_par = particle(False, inv_pos, inv_vel)

        par.connected_particles.append(inv_par)
        inv_par.connected_particles.append(par)

        self.particles.extend([par, inv_par])

    def draw(self, surface):
        # draw all particles
        for p in self.particles:
            p.draw(surface)
