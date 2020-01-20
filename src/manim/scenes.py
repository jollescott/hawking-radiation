from manimlib.imports import *


class VirtualParticles(Scene):
    def get_sine_wave(self, dx=0):
        return FunctionGraph(
            lambda x: np.sin((x+dx)-(PI/2)),
            x_min=-4, x_max=4, color=RED
        )

    def get_cosine_wave(self, dx=0):
        return FunctionGraph(
            lambda x: np.cos(x+dx),
            x_min=-4, x_max=4, color=BLUE
        )

    def construct(self):
        # Waves
        sine_function = self.get_sine_wave()
        cosine_function = self.get_cosine_wave()

        d_theta = ValueTracker(0)

        def update_sine_wave(func):
            func.become(
                self.get_sine_wave(dx=d_theta.get_value())
            )
            return func

        def update_cosine_wave(func):
            func.become(
                self.get_cosine_wave(dx=d_theta.get_value())
            )
            return func

        sine_function.add_updater(update_sine_wave)
        cosine_function.add_updater(update_cosine_wave)

        # Particles
        anti_particle = Circle(color=RED, fill_color=RED, fill_opacity=1)
        anti_particle.scale(0.2)
        anti_particle.move_to(DOWN)

        particle = Circle(color=BLUE, fill_color=BLUE, fill_opacity=1)
        particle.scale(0.2)
        particle.move_to(UP)

        self.add(sine_function)
        self.add(anti_particle)
        self.add(cosine_function)
        self.add(particle)

        self.play(d_theta.increment_value, PI, ApplyMethod(anti_particle.shift, [0, 2, 0]), ApplyMethod(
            particle.shift, [0, -2, 0]), rate_func=linear)

        self.play(d_theta.increment_value, PI, ApplyMethod(anti_particle.shift, [0, -2, 0]), ApplyMethod(
            particle.shift, [0, 2, 0]), rate_func=linear)
