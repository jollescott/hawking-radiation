from math import pi

# light speed
c = 2.99792458 * 10**8

# gravitational constant
G = 6.67384 * 10**-11

# planck constant
h = 6.62607015 * 10**-34

# reduced planck constant
h_bar = h / (2 * pi)

# boltzmann constant
Kb = 1.38064852 * 10**-23

# mas of the sun
Ms = 2 * 10**30


def gravitational_force(M1, M2, r):
    """
    Returns the force [N] between two objects with mass M1, M2 [kg] and a
    distance of r [m].
    """
    return G * M1 * M2 / r**2


def schwarzschild_radius(M):
    """
    Returns the Schwarzschild radius [m] of a black hole with mass M [kg].
    """
    return 2 * G * M / c**2


def black_hole_temperature(M):
    """
    Returns the temperature [K] of a black hole with mass M [kg].
    """
    return h_bar * c**3 / (8 * pi * G * M * Kb)


def black_hole_lifetime(M):
    """
    Retruns the lifetime [s] of a black hole with mass M [kg].
    """
    return M**3 * 5120 * pi * G**2 / (h_bar * c**4)


def black_hole_mass(t):
    """
    Returns the mass [kg] of a black hole with the remaning lifetime t [s].
    """
    return (t * h_bar * c**4 / (5120 * pi * G**2))**(1/3)
