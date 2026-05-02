import pygame

from config import (
    window_width,
    window_height,
    cell_size,
    grid_cols,
    grid_rows,
    fps,
    foods_per_level,
    base_move_delay,
    move_delay_step,
    min_move_delay,
    bg_color,
    grid_color,
    wall_color,
    wall_border_color,
    snake_head_color,
    snake_body_color,
    snake_outline_color,
    food_color,
)
from entities.snake import Snake
from entities.food import Food
from ui.hud import draw_hud, draw_center_message
from utils.grid import cell_to_rect, cell_to_center


class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("snake")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 24)
        self.small_font = pygame.font.SysFont("consolas", 18)
        self.title_font = pygame.font.SysFont("consolas", 42, bold=True)
        self.body_font = pygame.font.SysFont("consolas", 24)

        self.running = True
        self.reset()

    def reset(self):
        # reset core game state
        start_cell = (grid_cols // 2, grid_rows // 2)
        self.snake = Snake(start_cell)
        self.food = Food()

        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.state = "playing"

        self.move_timer = 0.0
        self.move_delay = base_move_delay

        self.spawn_food()

    def spawn_food(self):
        # place food away from walls and snake segments
        position = self.food.spawn(self.snake.segments)
        if position is None:
            self.state = "win"

    def update_speed(self):
        # increase speed every new level
        delay = base_move_delay - (self.level - 1) * move_delay_step
        self.move_delay = max(min_move_delay, delay)

    def level_up_if_needed(self):
        # level up after a fixed number of foods
        new_level = self.foods_eaten // foods_per_level + 1
        if new_level != self.level:
            self.level = new_level
            self.update_speed()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()

                if self.state != "playing":
                    continue

                if event.key == pygame.K_UP:
                    self.snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction((1, 0))

    def is_wall_collision(self, cell):
        # border cells are walls, so the playable area starts at 1 and ends at size - 2
        x, y = cell
        return x <= 0 or x >= grid_cols - 1 or y <= 0 or y >= grid_rows - 1

    def step_game(self):
        new_head = self.snake.step()

        if self.is_wall_collision(new_head):
            self.state = "game_over"
            return

        if self.snake.hits_self():
            self.state = "game_over"
            return

        if self.food.position == new_head:
            self.score += 10
            self.foods_eaten += 1
            self.snake.grow(1)
            self.spawn_food()
            self.level_up_if_needed()

            if self.state == "win":
                return

    def update(self, dt):
        if self.state != "playing":
            return

        self.move_timer += dt
        while self.move_timer >= self.move_delay and self.state == "playing":
            self.move_timer -= self.move_delay
            self.step_game()

    def draw_grid(self):
        # draw a subtle grid background
        for x in range(0, window_width, cell_size):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, window_height))
        for y in range(0, window_height, cell_size):
            pygame.draw.line(self.screen, grid_color, (0, y), (window_width, y))

    def draw_walls(self):
        # draw a solid border around the play area
        for x in range(grid_cols):
            top_rect = cell_to_rect((x, 0))
            bottom_rect = cell_to_rect((x, grid_rows - 1))
            pygame.draw.rect(self.screen, wall_color, top_rect)
            pygame.draw.rect(self.screen, wall_color, bottom_rect)
            pygame.draw.rect(self.screen, wall_border_color, top_rect, 1)
            pygame.draw.rect(self.screen, wall_border_color, bottom_rect, 1)

        for y in range(1, grid_rows - 1):
            left_rect = cell_to_rect((0, y))
            right_rect = cell_to_rect((grid_cols - 1, y))
            pygame.draw.rect(self.screen, wall_color, left_rect)
            pygame.draw.rect(self.screen, wall_color, right_rect)
            pygame.draw.rect(self.screen, wall_border_color, left_rect, 1)
            pygame.draw.rect(self.screen, wall_border_color, right_rect, 1)

    def draw_food(self):
        if self.food.position is None:
            return

        center = cell_to_center(self.food.position)
        radius = cell_size // 2 - 4
        pygame.draw.circle(self.screen, food_color, center, radius)

    def draw_snake(self):
        for index, segment in enumerate(self.snake.segments):
            rect = cell_to_rect(segment).inflate(-4, -4)

            if index == 0:
                pygame.draw.rect(self.screen, snake_head_color, rect, border_radius=6)
                pygame.draw.rect(self.screen, snake_outline_color, rect, 2, border_radius=6)
            else:
                pygame.draw.rect(self.screen, snake_body_color, rect, border_radius=6)

    def draw(self):
        self.screen.fill(bg_color)
        self.draw_grid()
        self.draw_walls()
        self.draw_food()
        self.draw_snake()
        draw_hud(self.screen, self.font, self.small_font, self.score, self.level)

        if self.state == "game_over":
            draw_center_message(
                self.screen,
                self.title_font,
                self.body_font,
                "game over",
                "press r to restart",
            )
        elif self.state == "win":
            draw_center_message(
                self.screen,
                self.title_font,
                self.body_font,
                "you win",
                "press r to restart",
            )

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(fps) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()