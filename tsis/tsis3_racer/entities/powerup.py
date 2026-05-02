import pygame
import random
from config import *

class PowerUp:
    def __init__(self, x=None, y=-20, p_type=None):
        if x is None:
            self.x = random.choice(LANES)
        else:
            self.x = x
        self.y = y
        self.radius = 12
        
        types = ["NITRO", "SHIELD", "REPAIR"]
        self.type = p_type if p_type else random.choice(types)
        
        if self.type == "NITRO":
            self.color = Colors.GREEN.value
        elif self.type == "SHIELD":
            self.color = Colors.CYAN.value
        else: # rEPAIR
            self.color = Colors.MAGENTA.value
            
        self.font = pygame.font.SysFont("Verdana", 10, bold=True)
            
    def update(self, speed):
        self.y += speed

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def offscreen(self):
        return self.y > SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # draw a small letter indicator
        letter = self.type[0]
        text = self.font.render(letter, True, Colors.BLACK.value)
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)
