from utils.grid import random_free_cell


class Food:
    def __init__(self):
        self.position = None

    def spawn(self, occupied_cells):
        # place food on a free cell only
        self.position = random_free_cell(occupied_cells)
        return self.position