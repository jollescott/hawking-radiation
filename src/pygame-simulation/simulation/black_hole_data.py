import formulas


class black_hole_data:
    def __init__(self, mass):
        self._mass = mass

    def get_mass(self):
        return self._mass

    def get_radius(self):
        return formulas.schwarzschild_radius(self._mass)

    def get_lifetime(self):
        return formulas.black_hole_lifetime(self._mass)

    def get_temperature(self):
        raise NotImplementedError

    def get_radiation_rate(self):
        raise NotImplementedError
