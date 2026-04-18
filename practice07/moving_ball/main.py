import pygame
import sys
from ball import draw_ball, move_ball, SPEED

# initialize pygame
pygame.init()

# window size
WIDTH = 800
HEIGHT = 600

# create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("moving ball")

# ball start position
x = WIDTH // 2
y = HEIGHT // 2

# fps controller
clock = pygame.time.Clock()

# main loop
while True:
    for event in pygame.event.get():

        # close window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # get pressed keys
    keys = pygame.key.get_pressed()

    # move up
    if keys[pygame.K_UP]:
        x, y = move_ball(x, y, 0, -SPEED, WIDTH, HEIGHT)

    # move down
    if keys[pygame.K_DOWN]:
        x, y = move_ball(x, y, 0, SPEED, WIDTH, HEIGHT)

    # move left
    if keys[pygame.K_LEFT]:
        x, y = move_ball(x, y, -SPEED, 0, WIDTH, HEIGHT)

    # move right
    if keys[pygame.K_RIGHT]:
        x, y = move_ball(x, y, SPEED, 0, WIDTH, HEIGHT)

    # fill background
    screen.fill((255, 255, 255))

    # draw ball
    draw_ball(screen, x, y)

    # update screen
    pygame.display.flip()

    # 60 fps
    clock.tick(60)