import time
import vector
from particle import particle


class universe:
    spawnTime = 3
    particleStartVel = 5

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
        self.particles.append(particle(True, pos, vel))
        self.particles.append(particle(False, inv_pos, inv_vel))

    def draw(self, surface):
        # draw all particles
        for p in self.particles:
            p.draw(surface)
