import os
import pygame
import random
from config import *

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_IMG = os.path.join(CURRENT_DIR, "player.png")
ENEMY_IMG = os.path.join(CURRENT_DIR, "enemy.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # load player car texture
        self.image = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        # move according to key presses
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # load enemy car texture
        self.image = pygame.image.load(ENEMY_IMG).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        # reset position if it goes off screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # gold circle for coin
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    def move(self):
        self.rect.move_ip(0, 5)
        # reset if off screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.reset()
            
    def reset(self):
        # random position to spawn coin again
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
