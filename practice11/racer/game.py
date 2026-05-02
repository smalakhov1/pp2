# main game logic

import pygame
import sys
from config import *

from entities import Player, Enemy, Coin, Road
from systems import Spawner
from ui import HUD


class Game:
    def __init__(self):
        # init pygame
        pygame.init()

        # create window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racer")

        # clock and state
        self.clock = pygame.time.Clock()
        self.running = True

        # game objects
        self.player = Player()
        self.road = Road()

        self.enemies = []
        self.coins = []

        self.spawner = Spawner()
        self.hud = HUD()

        self.coins_collected = 0
        self.game_over = False

    def run(self):
        # main loop
        while self.running:
            self.events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def events(self):
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if not self.game_over:
                self.player.handle_event(event)

    def update(self):
        # stop updates if game over
        if self.game_over:
            return

        # calc current global speed
        current_speed = 5 + (self.coins_collected // 5)

        self.road.update(current_speed)
        self.spawner.update(self)

        for e in self.enemies:
            e.update(current_speed)

        for c in self.coins:
            c.update(current_speed)

        # coin collision
        for c in self.coins[:]:
            if self.player.rect().colliderect(c.rect()):
                self.coins.remove(c)
                # add coin's weight to the collected count
                self.coins_collected += c.weight

        # enemy collision
        for e in self.enemies:
            if self.player.rect().colliderect(e.rect()):
                self.game_over = True

        # cleanup
        self.enemies = [e for e in self.enemies if not e.offscreen()]
        self.coins = [c for c in self.coins if not c.offscreen()]

    def draw(self):
        # draw scene
        self.road.draw(self.screen)

        for c in self.coins:
            c.draw(self.screen)

        for e in self.enemies:
            e.draw(self.screen)

        self.player.draw(self.screen)
        self.hud.draw(self.screen, self.coins_collected)

        # draw game over text
        if self.game_over:
            font = pygame.font.SysFont("Arial", 48)
            text = font.render("GAME OVER", True, Colors.RED.value)
            self.screen.blit(text, (60, 250))