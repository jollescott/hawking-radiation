# from simulation.data import black_hole_data
import formulas


class simulation:
    def __init__(self, start_mass=formulas.Ms):
        # self._data = black_hole_data()
        # self._data.mass = start_mass

        self._total_lifetime = formulas.black_hole_lifetime(start_mass)

        self._total_elapsed_time = 0

    def update(self, elapsed_time):
        self._total_elapsed_time += elapsed_time

    def get_current_mass(self):
        return formulas.black_hole_mass(self._total_lifetime
                                        - self._total_elapsed_time)
