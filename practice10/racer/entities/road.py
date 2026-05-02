# road rendering

import pygame
from config import *

class Road:
    def __init__(self):
        # line offset
        self.offset = 0

    def update(self):
        # animate lines
        self.offset += 5
        if self.offset > 40:
            self.offset = 0

    def draw(self, screen):
        # draw grass
        screen.fill(Colors.GRASS.value)

        # draw road
        pygame.draw.rect(screen, Colors.ROAD.value,
                         (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # draw dashed line
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(
                screen,
                Colors.WHITE.value,
                (SCREEN_WIDTH // 2 - 5, y + self.offset, 10, 20)
            )