import pygame
import os

pygame.init()
# Create transparent surfaces
player_surface = pygame.Surface((40, 80), pygame.SRCALPHA)
enemy_surface = pygame.Surface((40, 80), pygame.SRCALPHA)

# Helper function to draw a car
def draw_car(surface, color):
    # body
    pygame.draw.rect(surface, color, (5, 10, 30, 60), border_radius=8)
    # windshield
    pygame.draw.rect(surface, (50, 200, 255), (10, 25, 20, 15), border_radius=3)
    # rear window
    pygame.draw.rect(surface, (50, 200, 255), (10, 50, 20, 10), border_radius=2)
    # wheels
    pygame.draw.rect(surface, (30, 30, 30), (0, 15, 6, 15), border_radius=2) # top-left
    pygame.draw.rect(surface, (30, 30, 30), (34, 15, 6, 15), border_radius=2) # top-right
    pygame.draw.rect(surface, (30, 30, 30), (0, 50, 6, 15), border_radius=2) # bottom-left
    pygame.draw.rect(surface, (30, 30, 30), (34, 50, 6, 15), border_radius=2) # bottom-right
    # headlights
    pygame.draw.rect(surface, (255, 255, 100), (8, 10, 6, 4))
    pygame.draw.rect(surface, (255, 255, 100), (26, 10, 6, 4))

draw_car(player_surface, (0, 100, 255))
draw_car(enemy_surface, (255, 50, 50))

# save images
pygame.image.save(player_surface, "player.png")
pygame.image.save(enemy_surface, "enemy.png")
print("Saved player.png and enemy.png")
