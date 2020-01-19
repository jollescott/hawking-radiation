import formulas


class simulation:
    def __init__(self, start_mass=formulas.Ms):
        self.start_mass = start_mass
        self._total_lifetime = formulas.black_hole_lifetime(start_mass)
        self.total_elapsed_time = 0

    def update(self, elapsed_time):
        self.total_elapsed_time += elapsed_time

    def get_current_mass(self):
        return formulas.black_hole_mass(self._total_lifetime
                                        - self.total_elapsed_time)
