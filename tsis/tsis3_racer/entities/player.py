# player entity

import pygame
from config import *

class Player:
    def __init__(self, color_name="BLUE"):
        # start in center lane
        self.lane = 1
        self.x = LANES[self.lane]
        self.y = PLAYER_Y

        # size
        self.w, self.h = 40, 70
        
        # properties
        try:
            self.color = Colors[color_name.upper()].value
        except:
            self.color = Colors.BLUE.value
            
        self.has_shield = False

    def handle_event(self, event):
        # handle keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # move left
                self.lane = max(0, self.lane - 1)
            elif event.key == pygame.K_RIGHT:
                # move right
                self.lane = min(len(LANES) - 1, self.lane + 1)

            # update position
            self.x = LANES[self.lane]

    def rect(self):
        # collision rectangle
        return pygame.Rect(self.x - 20, self.y, self.w, self.h)

    def draw(self, screen):
        # draw player
        pygame.draw.rect(screen, self.color, self.rect())
        
        # draw shield
        if self.has_shield:
            pygame.draw.circle(screen, Colors.CYAN.value, (self.x, self.y + self.h//2), 45, 3)