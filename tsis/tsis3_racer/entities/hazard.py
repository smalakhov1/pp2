import pygame
import random
from config import *

class Hazard:
    def __init__(self, x=None, y=-40):
        if x is None:
            self.x = random.choice(LANES)
        else:
            self.x = x
        self.y = y
        
        # 0 = Pothole, 1 = Oil Spill
        self.type = random.choice(["POTHOLE", "OIL"])
        
        if self.type == "POTHOLE":
            self.width, self.height = 30, 20
            self.color = Colors.BLACK.value
        else: # oIL
            self.width, self.height = 40, 30
            self.color = Colors.BROWN.value
            
    def update(self, speed):
        self.y += speed

    def rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    def offscreen(self):
        return self.y > SCREEN_HEIGHT

    def draw(self, screen):
        if self.type == "POTHOLE":
            pygame.draw.ellipse(screen, self.color, self.rect())
        else:
            # draw irregular oil spill shape (just an ellipse for simplicity)
            pygame.draw.ellipse(screen, self.color, self.rect())
