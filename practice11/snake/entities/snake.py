class Snake:
    def __init__(self, start_cell):
        self.start_cell = start_cell
        self.reset()

    def reset(self):
        # initialize the snake in the center with a short body
        x, y = self.start_cell
        self.segments = [
            (x, y),
            (x - 1, y),
            (x - 2, y),
        ]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow_pending = 0

    @property
    def head(self):
        return self.segments[0]

    def set_direction(self, new_direction):
        # prevent instant reverse movement
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction == opposite:
            return
        self.next_direction = new_direction

    def step(self):
        # move the snake one cell forward
        self.direction = self.next_direction
        hx, hy = self.head
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)

        self.segments.insert(0, new_head)

        if self.grow_pending > 0: 
            self.grow_pending -= 1 # each step -> head mowes forward, tail is deleted. 
        else:
            self.segments.pop()

        return new_head

    def grow(self, amount=1):
        # delay tail removal for future steps
        self.grow_pending += amount

    def occupies(self, cell):
        return cell in self.segments

    def hits_self(self):
        # head collision with any body segment
        return self.head in self.segments[1:]