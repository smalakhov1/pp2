import pygame
import sys
import time
from config import *
from sprites import Player, Enemy, Coin

# initialize pygame
pygame.init()

# setup fonts and display
font = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 40)

display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

# create sprites
player = Player()
enemy = Enemy()
coin = Coin()

# group sprites
enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

# increase enemy speed event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

score = 0
enemy_speed = 10

def show_game_over():
    # print game over message and exit
    display_surf.fill(RED)
    game_over_text = game_over_font.render("game over", True, BLACK)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    display_surf.blit(game_over_text, text_rect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED:
            enemy_speed += 0.5

    # update and move
    player.update()
    
    # move enemy with current speed
    enemy.rect.move_ip(0, int(enemy_speed))
    if enemy.rect.bottom > SCREEN_HEIGHT:
        enemy.rect.top = 0
        import random
        enemy.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    coin.move()

    # handle collision with enemies
    if pygame.sprite.spritecollideany(player, enemies):
        show_game_over()

    # handle collision with coins
    collected_coins = pygame.sprite.spritecollide(player, coins, False)
    for c in collected_coins:
        score += 1
        c.reset()

    # draw animated background road
    display_surf.fill((60, 60, 60)) # dark grey road
    
    # move road lines
    if not hasattr(player, 'bg_y'): player.bg_y = 0
    player.bg_y = (player.bg_y + enemy_speed) % 60
    
    # draw middle lane dashes
    for y in range(-60, SCREEN_HEIGHT, 60):
        pygame.draw.rect(display_surf, WHITE, (SCREEN_WIDTH // 2 - 5, y + player.bg_y, 10, 30))
    
    # draw side borders
    pygame.draw.rect(display_surf, (200, 200, 0), (10, 0, 10, SCREEN_HEIGHT))
    pygame.draw.rect(display_surf, (200, 200, 0), (SCREEN_WIDTH - 20, 0, 10, SCREEN_HEIGHT))
    # draw score in top right
    score_text = font.render(f"coins: {score}", True, BLACK)
    display_surf.blit(score_text, (SCREEN_WIDTH - 100, 10))

    # draw all sprites
    for entity in all_sprites:
        entity.draw(display_surf)

    pygame.display.update()
    clock.tick(FPS)
