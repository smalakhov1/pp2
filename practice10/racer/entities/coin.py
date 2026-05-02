# coin entity

import pygame
import random
from config import *

class Coin:
    def __init__(self):
        # spawn above screen
        self.x = random.choice(LANES)
        self.y = -20
        self.speed = 5
        self.radius = 10

    def update(self):
        # move down
        self.y += self.speed

    def rect(self):
        # collision rectangle
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20)

    def offscreen(self):
        # check if below screen
        return self.y > SCREEN_HEIGHT

    def draw(self, screen):
        # draw coin
        pygame.draw.circle(screen, Colors.YELLOW.value, (self.x, int(self.y)), self.radius)