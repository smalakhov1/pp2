import pygame
from .base_tool import BaseTool

class SquareTool(BaseTool):
    def __init__(self):
        # store starting position of square
        self.start_pos = None

    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            self.start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if app.drawing and self.start_pos is not None:
                end_pos = event.pos
                rect = self._get_square_rect(self.start_pos, end_pos)
                # draw final square on canvas
                pygame.draw.rect(canvas, app.current_color, rect, app.brush_size)
            app.drawing = False
            self.start_pos = None

    def draw_preview(self, surface, app):
        # draw temporary square while dragging
        if app.drawing and self.start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()
            rect = self._get_square_rect(self.start_pos, mouse_pos)
            pygame.draw.rect(surface, app.current_color, rect, app.brush_size)

    def _get_square_rect(self, start, end):
        # force width and height to be equal (max of differences)
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        side = max(abs(dx), abs(dy))
        
        # preserve direction
        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1
        
        rect = pygame.Rect(start[0], start[1], side * sign_x, side * sign_y)
        rect.normalize()
        return rect
