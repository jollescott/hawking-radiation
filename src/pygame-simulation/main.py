import pygame
import time
from animation.animation import animation

(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))

animation = animation((width, height))

start_time = time.perf_counter()
time_multiplier = 1

running = True
while running:

    elapsed_time = time.perf_counter() - start_time
    start_time = time.perf_counter()

    # update -----------------------------------
    for event in pygame.event.get():
        # exit if close button is pressed
        if event.type == pygame.QUIT:
            running = False

    animation.update(elapsed_time * time_multiplier)

    # draw --------------------------------------
    screen.fill((0, 0, 0))
    animation.draw(screen)

    pygame.display.update()
