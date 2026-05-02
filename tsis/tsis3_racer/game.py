import pygame
from config import *
from entities.player import Player
from entities.road import Road
from systems.spawner import Spawner

class RaceSession:
    def __init__(self, settings):
        self.settings = settings
        self.player = Player(color_name=settings.get("car_color", "BLUE"))
        self.road = Road()
        
        self.enemies = []
        self.coins = []
        self.powerups = []
        self.hazards = []
        
        self.spawner = Spawner(difficulty=settings.get("difficulty", "Normal"))
        
        self.coins_collected = 0
        self.distance = 0
        self.score = 0
        self.game_over = False
        
        # powerup states
        self.active_powerup = None
        self.powerup_timer = 0
        
        self.font = pygame.font.SysFont("Verdana", 20, bold=True)

    def handle_event(self, event):
        if not self.game_over:
            self.player.handle_event(event)

    def update(self):
        if self.game_over:
            return

        # calc global speed
        base_speed = 5
        if self.settings["difficulty"] == "Hard": base_speed = 7
        elif self.settings["difficulty"] == "Easy": base_speed = 4
            
        current_speed = base_speed + (self.coins_collected // 5)
        
        # powerup logic
        now = pygame.time.get_ticks()
        if self.active_powerup == "NITRO":
            current_speed += 5
            if now > self.powerup_timer:
                self.active_powerup = None
        elif self.active_powerup == "SHIELD":
            self.player.has_shield = True
            # shield lasts until hit
        else:
            self.player.has_shield = False

        self.distance += current_speed * 0.1
        if self.distance >= FINISH_LINE_DISTANCE:
            self.game_over = True
            
        self.score = (self.coins_collected * 10) + int(self.distance // 10)

        self.road.update(current_speed)
        self.spawner.update(self)

        for e in self.enemies: e.update(current_speed)
        for c in self.coins: c.update(current_speed)
        for p in self.powerups: p.update(current_speed)
        for h in self.hazards: h.update(current_speed)

        # collisions
        p_rect = self.player.rect()
        
        # coins
        for c in self.coins[:]:
            if p_rect.colliderect(c.rect()):
                self.coins.remove(c)
                self.coins_collected += c.weight
                
        # powerups
        for p in self.powerups[:]:
            if p_rect.colliderect(p.rect()):
                self.powerups.remove(p)
                if p.type == "NITRO":
                    self.active_powerup = "NITRO"
                    self.powerup_timer = now + 4000
                elif p.type == "SHIELD":
                    self.active_powerup = "SHIELD"
                    self.player.has_shield = True
                elif p.type == "REPAIR":
                    # clear all enemies and hazards on screen
                    self.enemies.clear()
                    self.hazards.clear()
                    
        # hazards
        for h in self.hazards[:]:
            if p_rect.colliderect(h.rect()):
                self.hazards.remove(h)
                if self.player.has_shield:
                    self.active_powerup = None
                    self.player.has_shield = False
                else:
                    self.score = max(0, self.score - 50)
                    self.distance = max(0, self.distance - 100) # penalty

        # enemies
        for e in self.enemies:
            if p_rect.colliderect(e.rect()):
                if self.player.has_shield:
                    self.enemies.remove(e)
                    self.active_powerup = None
                    self.player.has_shield = False
                else:
                    self.game_over = True

        # cleanup
        self.enemies = [e for e in self.enemies if not e.offscreen()]
        self.coins = [c for c in self.coins if not c.offscreen()]
        self.powerups = [p for p in self.powerups if not p.offscreen()]
        self.hazards = [h for h in self.hazards if not h.offscreen()]

    def draw(self, screen):
        self.road.draw(screen)
        
        for c in self.coins: c.draw(screen)
        for p in self.powerups: p.draw(screen)
        for h in self.hazards: h.draw(screen)
        for e in self.enemies: e.draw(screen)
        
        self.player.draw(screen)
        
        # hUD
        score_text = self.font.render(f"Score: {self.score}", True, Colors.BLACK.value)
        dist_text = self.font.render(f"Dist: {int(self.distance)}/{FINISH_LINE_DISTANCE}", True, Colors.BLACK.value)
        
        screen.blit(score_text, (10, 10))
        screen.blit(dist_text, (10, 40))
        
        if self.active_powerup:
            if self.active_powerup == "NITRO":
                rem = max(0, (self.powerup_timer - pygame.time.get_ticks()) // 1000)
                pw_text = self.font.render(f"NITRO: {rem}s", True, Colors.GREEN.value)
            elif self.active_powerup == "SHIELD":
                pw_text = self.font.render(f"SHIELD ACTIVE", True, Colors.CYAN.value)
            
            screen.blit(pw_text, (10, 70))