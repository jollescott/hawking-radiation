from animation.world.universe import universe


class animation:
    def __init__(self, screen_size):
        self.universe = universe(screen_size)

    def update(self, elapsed_time):
        self.universe.update(elapsed_time)

    def draw(self, surface):
        self.universe.draw(surface)
