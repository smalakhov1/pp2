# spawn logic

import pygame
from config import *
from entities.enemy import Enemy
from entities.coin import Coin
from entities.powerup import PowerUp
from entities.hazard import Hazard

class Spawner:
    def __init__(self, difficulty="Normal"):
        # last spawn times
        self.last_enemy = pygame.time.get_ticks()
        self.last_coin = pygame.time.get_ticks()
        self.last_powerup = pygame.time.get_ticks()
        self.last_hazard = pygame.time.get_ticks()
        self.difficulty = difficulty

    def _is_safe(self, rect, game):
        for e in game.enemies + game.coins + game.powerups + game.hazards:
            if rect.colliderect(e.rect()):
                return False
        return True

    def update(self, game):
        now = pygame.time.get_ticks()

        # difficulty scaling
        mult = 1.0
        if self.difficulty == "Easy": mult = 1.5
        elif self.difficulty == "Hard": mult = 0.7
        
        # density scaling by distance
        distance_mult = max(0.5, 1.0 - (game.distance / FINISH_LINE_DISTANCE))
        
        real_spawn_interval = SPAWN_INTERVAL * mult * distance_mult
        real_hazard_interval = HAZARD_SPAWN_INTERVAL * mult * distance_mult

        # spawn enemy
        if now - self.last_enemy > real_spawn_interval:
            e = Enemy()
            if self._is_safe(e.rect(), game):
                game.enemies.append(e)
            self.last_enemy = now

        # spawn coin
        if now - self.last_coin > COIN_SPAWN_INTERVAL:
            c = Coin()
            if self._is_safe(c.rect(), game):
                game.coins.append(c)
            self.last_coin = now
            
        # spawn powerup
        if now - self.last_powerup > POWERUP_SPAWN_INTERVAL:
            p = PowerUp()
            if self._is_safe(p.rect(), game):
                game.powerups.append(p)
            self.last_powerup = now
            
        # spawn hazard
        if now - self.last_hazard > real_hazard_interval:
            h = Hazard()
            if self._is_safe(h.rect(), game):
                game.hazards.append(h)
            self.last_hazard = now