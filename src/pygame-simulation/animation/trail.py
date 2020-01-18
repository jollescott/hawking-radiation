from pygame import draw
from animation import vector
import numpy as np


class trail:
    color = (255, 255, 255)
    fade_color = (0, 0, 0)
    thickness = 1
    max_length = 40
    min_point_dist = 1

    def __init__(self):
        self.points = []
        self.__current_length = 0

    def __insert_point(self, point, add_length):
        self.points.insert(0, point)
        self.__current_length += add_length

    def add_point(self, point):
        # add point
        if (len(self.points) == 0):
            self.__insert_point(point, 0)
        else:
            add_dist = vector.get_distance(point, self.points[0])
            if add_dist >= self.min_point_dist:
                self.__insert_point(point, add_dist)

        # remove points if trail is too long
        while self.__current_length > self.max_length and len(self.points) > 1:
            self.__current_length -= vector.get_distance(
                self.points[-1],
                self.points[-2]
            )
            self.points.pop(-1)

    def get_length(self):
        return self.__current_length

    def draw(self, surface):
        n = len(self.points)
        for i in range(n - 1):
            point = self.points[i]
            next_point = self.points[i + 1]

            p = i / n

            draw.line(
                surface,
                (
                    (1 - p) * self.color[0] + p * self.fade_color[0],
                    (1 - p) * self.color[1] + p * self.fade_color[1],
                    (1 - p) * self.color[2] + p * self.fade_color[2],
                ),
                np.array(point, dtype=int),
                next_point,
                self.thickness
            )
