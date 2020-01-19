import pygame
import time
from simulation.simulation import simulation
from animation.animation import animation
import formulas


pygame.init()

(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))

simulation = simulation()
animation = animation((width, height), simulation.start_mass)

start_time = time.perf_counter()
time_multiplier = 5 * 10**72

font = pygame.font.SysFont('consolas', 15)


def draw_data(data):
    max_text_width = 0
    # get max text width
    for d in data:
        for string in d:
            text_width = font.size(string)[0]
            if text_width > max_text_width:
                max_text_width = text_width

    text_height = font.get_height()
    name_color = (180, 180, 180)
    val_color = (255, 180, 180)
    offset = (8, 8)
    spacing = 10

    # draw background
    surf = pygame.Surface((
        max_text_width + 2 * offset[0],
        offset[1] * 2 + (text_height * 2 + spacing) * len(data) - spacing
    ))
    surf.set_alpha(128)
    surf.fill((50, 50, 50))
    screen.blit(surf, (0, 0))

    # draw data
    for index, (name, value) in enumerate(data):
        name_surf, value_surf = (
            font.render(name, True, name_color),
            font.render(value, True, val_color)
        )
        screen.blit(name_surf, (
            offset[0],
            offset[1] + index * (text_height * 2 + spacing)
        ))
        screen.blit(value_surf, (
            offset[0],
            offset[1] + index * (text_height * 2 + spacing) + text_height
        ))


running = True
while running:

    elapsed_time = time.perf_counter() - start_time
    start_time = time.perf_counter()

    # update -----------------------------------
    for event in pygame.event.get():
        # exit if close button is pressed
        if event.type == pygame.QUIT:
            running = False

    simulation.update(elapsed_time * time_multiplier)
    animation.update(
        elapsed_time * time_multiplier,
        simulation.get_current_mass()
    )

    # draw --------------------------------------
    screen.fill((0, 0, 0))
    animation.draw(screen)

    current_mass = simulation.get_current_mass()
    draw_data([
        (
            'Seconds per second',
            "{:.2e}".format(time_multiplier)
        ),
        (
            'Total elapsed time [s]',
            "{:.2e}".format(simulation.total_elapsed_time)
        ),
        (
            '',
            ''
        ),
        (
            'Mass [kg]',
            "{:.2e}".format(current_mass)
        ),
        (
            'Schwarzschild radius [m]',
            "{:.2e}".format(formulas.schwarzschild_radius(current_mass))
        ),
        (
            'Temperature [K]',
            "{:.2e}".format(formulas.black_hole_temperature(current_mass))
        ),
        (
            'Remaining lifetime [s]',
            "{:.2e}".format(formulas.black_hole_lifetime(current_mass))
        ),
    ])

    pygame.display.update()
