import pygame
import time
from universe import universe

(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))

universe = universe()

startTime = time.perf_counter()

running = True
while running:

    elapsedTime = time.perf_counter() - startTime
    startTime = time.perf_counter()

    print(elapsedTime)

    # update -----------------------------------
    for event in pygame.event.get():
        # exit if close button is pressed
        if event.type == pygame.QUIT:
            running = False
    
    universe.update(elapsedTime)

    # draw --------------------------------------
    screen.fill((0, 0, 0))
    universe.draw(screen)

    pygame.display.update()
