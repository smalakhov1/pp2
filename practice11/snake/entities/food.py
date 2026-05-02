import random
from utils.grid import random_free_cell


class Food:
    def __init__(self):
        self.position = None
        self.weight = 1
        self.timer = 0.0
        self.max_time = 0.0

    def spawn(self, occupied_cells):
        # randomly assign weight to food (1, 2, or 3)
        self.weight = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        
        # more valuable food disappears faster
        if self.weight == 1:
            self.max_time = 15.0 # regular food lasts 15 seconds
        elif self.weight == 2:
            self.max_time = 10.0 # medium food lasts 10 seconds
        else:
            self.max_time = 5.0  # rare food lasts 5 seconds
            
        self.timer = self.max_time

        # place food on a free cell only
        self.position = random_free_cell(occupied_cells)
        return self.position

    def update(self, dt):
        # decrease timer if food exists
        if self.position is not None:
            self.timer -= dt
            # if timer runs out, food disappears
            if self.timer <= 0:
                self.position = None