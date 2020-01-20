from animation.world.universe import universe
import formulas


class animation:
    def __init__(self, screen_size, start_mass):
        black_hole_radius = min(screen_size) / 2 * 0.5

        self.scale = (black_hole_radius
                      / formulas.schwarzschild_radius(start_mass))

        self.universe = universe(screen_size, self.scale)

    def update(self, elapsed_time, black_hole_mass):
        self.universe.black_hole.mass = black_hole_mass
        self.universe.update(elapsed_time)

    def draw(self, surface):
        self.universe.draw(surface)
