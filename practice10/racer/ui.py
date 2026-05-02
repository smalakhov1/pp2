# hud display

import pygame
from config import Colors

class HUD:
    def __init__(self):
        # font setup
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen, coins):
        # render coin counter
        text = self.font.render(f"Coins: {coins}", True, Colors.WHITE.value)
        screen.blit(text, (10, 10))