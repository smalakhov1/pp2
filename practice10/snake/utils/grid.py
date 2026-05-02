import random
import pygame

from config import cell_size, grid_cols, grid_rows


def cell_to_rect(cell):
    # convert a grid cell to a pygame rect
    x, y = cell
    return pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)


def cell_to_center(cell):
    # get the pixel center of a grid cell
    x, y = cell
    return (
        x * cell_size + cell_size // 2,
        y * cell_size + cell_size // 2,
    )


def get_playable_cells():
    # return all cells inside the wall border
    cells = []
    for y in range(1, grid_rows - 1):
        for x in range(1, grid_cols - 1):
            cells.append((x, y))
    return cells


def random_free_cell(occupied_cells):
    # pick a random cell that is not occupied by the snake or wall
    occupied = set(occupied_cells)
    free_cells = [cell for cell in get_playable_cells() if cell not in occupied]
    if not free_cells:
        return None
    return random.choice(free_cells)