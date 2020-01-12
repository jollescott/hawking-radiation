import math


# gravitational constant
G = 6.674 * 10**-11

# light speed
c = 2.99792458 * 10**8

# mas of the sun
Ms = 2 * 10**30


def gravitational_force(M1, M2, r):
    return G * M1 * M2 / math.pow(r, 2)


def schwarzschild_radius(M):
    return 2 * G * M / math.pow(c, 2)
