# enemy entity

import pygame
import random
from config import *

class Enemy:
    def __init__(self):
        # spawn above screen in random lane
        self.x = random.choice(LANES)
        self.y = -60
        self.speed = 5

    def update(self):
        # move down
        self.y += self.speed

    def rect(self):
        # collision rectangle
        return pygame.Rect(self.x - 20, self.y, 40, 70)

    def offscreen(self):
        # check if below screen
        return self.y > SCREEN_HEIGHT

    def draw(self, screen):
        # draw enemy
        pygame.draw.rect(screen, Colors.RED.value, self.rect())