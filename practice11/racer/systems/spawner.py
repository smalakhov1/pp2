# spawn logic

import pygame
from config import *
from entities import Enemy, Coin

class Spawner:
    def __init__(self):
        # last spawn times
        self.last_enemy = pygame.time.get_ticks()
        self.last_coin = pygame.time.get_ticks()

    def update(self, game):
        now = pygame.time.get_ticks()

        # spawn enemy
        if now - self.last_enemy > SPAWN_INTERVAL:
            game.enemies.append(Enemy())
            self.last_enemy = now

        # spawn coin
        if now - self.last_coin > COIN_SPAWN_INTERVAL:
            game.coins.append(Coin())
            self.last_coin = now