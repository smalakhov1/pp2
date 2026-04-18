import pygame

RADIUS = 25
SPEED = 5


def draw_ball(screen, x, y):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), RADIUS)


def move_ball(x, y, dx, dy, width, height):
    new_x = x + dx
    new_y = y + dy

    if new_x - RADIUS >= 0 and new_x + RADIUS <= width:
        x = new_x

    if new_y - RADIUS >= 0 and new_y + RADIUS <= height:
        y = new_y

    return x, y