from manimlib.imports import *
from random import Random
import math


class HawkingRadiation(Scene):
    def construct(self):
        steps = [self.blackhole_presentation, self.vparticle_presentation]

        for step in steps:
            step()

    def blackhole_presentation(self):
        circle = Circle()
        circle.set_style(
            stroke_color=ORANGE, sheen_factor=2, sheen_direction=RIGHT + DOWN
        )
        circle.scale(2)

        self.play(ShowCreation(circle))

    def vparticle_presentation(self):
        for i in range(5):
            r = Random()

            ran_x = 0
            ran_y = 0

            while True:
                ran_x = r.randint(-6, 6)
                ran_y = r.randint(-3, 3)

                if math.sqrt(math.pow(ran_y, 2) + math.pow(ran_y, 2)) > 2:
                    break
                else:
                    print("Inside circle {}, {}".format(ran_x, ran_y))

            l_arrow = Arrow([ran_x, ran_y, 0], [ran_x - 1, ran_y, 0])
            r_arrow = Arrow([ran_x, ran_y, 0], [ran_x + 1, ran_y, 0])

            p_particle = Point([ran_x, ran_y, 0])
            p_particle.set_color(BLUE)

            a_particle = Point([ran_x, ran_y, 0])
            a_particle.set_color(RED)

            self.play(
                GrowArrow(l_arrow),
                GrowArrow(r_arrow),
                ApplyMethod(p_particle.shift, [-1, 0, 0]),
                ApplyMethod(a_particle.shift, [1, 0, 0]),
            )
            self.play(FadeOut(l_arrow), FadeOut(r_arrow))

            l_arrow = Arrow([ran_x - 1, ran_y, 0], [ran_x, ran_y, 0])
            r_arrow = Arrow([ran_x + 1, ran_y, 0], [ran_x, ran_y, 0])

            self.play(
                GrowArrow(l_arrow),
                GrowArrow(r_arrow),
                ApplyMethod(p_particle.shift, [1, 0, 0]),
                ApplyMethod(a_particle.shift, [-1, 0, 0]),
            )
            self.play(
                FadeOut(l_arrow),
                FadeOut(r_arrow),
                FadeOut(p_particle),
                FadeOut(a_particle),
            )

