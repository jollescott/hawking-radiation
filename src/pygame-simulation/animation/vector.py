import random
import math


def new_vector(length, rotation):
    x = math.cos(rotation) * length
    y = math.sin(rotation) * length
    return (x, y)


def rand_vector_rot(length):
    rotation = random.uniform(0, 2 * math.pi)
    return new_vector(length, rotation)


def rand_vector_pos(x_min, x_max, y_min, y_max):
    x = random.uniform(x_min, x_max)
    y = random.uniform(y_min, y_max)
    return (x, y)


def invert(vector):
    return (-vector[0], -vector[1])


def get_length(vector):
    return math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))


def get_rotation(vector):
    length = get_length(vector)
    rotation = math.acos(vector[0] / length)
    return rotation if vector[1] >= 0 else -rotation


def change_length(vector, new_length):
    rotation = get_rotation(vector)
    return new_vector(new_length, rotation)


def change_rotation(vector, new_rotation):
    length = get_length(vector)
    return new_vector(length, new_rotation)


def add(vector1, vector2):
    return (vector1[0] + vector2[0], vector1[1] + vector2[1])


def subtract(vector1, vector2):
    return (vector1[0] - vector2[0], vector1[1] - vector2[1])


def get_distance(vector1, vector2):
    dx = abs(vector1[0] - vector2[0])
    dy = abs(vector1[1] - vector2[1])
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))


def point_from_to(vector1, vector2):
    x = vector2[0] - vector1[0]
    y = vector2[1] - vector1[1]
    return (x, y)
