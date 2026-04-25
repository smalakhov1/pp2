import pygame
import sys
import time
from config import *
from game_objects import Snake, Food

pygame.init()

font = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 40)

display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

snake = Snake()
food = Food(snake.body)

score = 0
level = 1
base_fps = 10
foods_eaten_in_level = 0

def show_game_over():
    display_surf.fill(BLACK)
    game_over_text = game_over_font.render("game over", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    display_surf.blit(game_over_text, text_rect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, BLOCK_SIZE):
                snake.direction = (0, -BLOCK_SIZE)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -BLOCK_SIZE):
                snake.direction = (0, BLOCK_SIZE)
            elif event.key == pygame.K_LEFT and snake.direction != (BLOCK_SIZE, 0):
                snake.direction = (-BLOCK_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-BLOCK_SIZE, 0):
                snake.direction = (BLOCK_SIZE, 0)

    # peek next position
    head_x, head_y = snake.body[0]
    dir_x, dir_y = snake.direction
    next_pos = (head_x + dir_x, head_y + dir_y)

    # move and handle food collision
    if next_pos == food.position:
        snake.move(grow=True)
        food.spawn(snake.body)
        score += 1
        foods_eaten_in_level += 1
        # increase level every 3 foods
        if foods_eaten_in_level >= 3:
            level += 1
            foods_eaten_in_level = 0
            base_fps += 2
    else:
        snake.move(grow=False)

    # check collision with wall or self
    if snake.check_collision():
        show_game_over()

    # draw background
    display_surf.fill(BLACK)
    
    # draw grid
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(display_surf, (30, 30, 30), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(display_surf, (30, 30, 30), (0, y), (SCREEN_WIDTH, y))

    # draw snake and food
    snake.draw(display_surf)
    food.draw(display_surf)

    # draw score and level
    score_text = font.render(f"score: {score}  level: {level}", True, WHITE)
    display_surf.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(base_fps)
