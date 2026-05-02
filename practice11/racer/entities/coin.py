# coin entity

import pygame
import random
from config import *

class Coin:
    def __init__(self):
        # spawn above screen
        self.x = random.choice(LANES)
        self.y = -20
        
        # randomly assign weight to the coin (1, 2, or 3)
        self.weight = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        
        # assign properties based on weight
        if self.weight == 1:
            self.radius = 10
            self.color = Colors.YELLOW.value
        elif self.weight == 2:
            self.radius = 12
            self.color = Colors.WHITE.value
        else:
            self.radius = 15
            self.color = Colors.BLUE.value

    def update(self, speed):
        # move down
        self.y += speed

    def rect(self):
        # collision rectangle based on dynamic radius
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def offscreen(self):
        # check if below screen
        return self.y > SCREEN_HEIGHT

    def draw(self, screen):
        # draw coin with dynamic color
        pygame.draw.circle(screen, self.color, (self.x, int(self.y)), self.radius)