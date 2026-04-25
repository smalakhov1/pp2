import pygame
import random
from config import *

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (BLOCK_SIZE, 0) # moving right

    def move(self, grow=False):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop() # remove tail

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)
            if i == 0:
                pygame.draw.rect(surface, (0, 200, 0), rect, border_radius=5) # darker head
            else:
                pygame.draw.rect(surface, GREEN, rect, border_radius=3) # rounded body

    def check_collision(self):
        head = self.body[0]
        # wall collision
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        # self collision
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            if (x, y) not in snake_body:
                self.position = (x, y)
                break

    def draw(self, surface):
        center = (self.position[0] + BLOCK_SIZE // 2, self.position[1] + BLOCK_SIZE // 2)
        pygame.draw.circle(surface, RED, center, BLOCK_SIZE // 2 - 2)
