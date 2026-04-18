# main.py

import pygame
import sys
from clock import draw_clock, load_images

# initialize pygame
pygame.init()

# window size
WIDTH = 800
HEIGHT = 800

# create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mickey clock")

# load images
load_images()

# fps controller
clock = pygame.time.Clock()

while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw clock
    draw_clock(screen)

    # update display
    pygame.display.flip()

    # limit fps
    clock.tick(60)