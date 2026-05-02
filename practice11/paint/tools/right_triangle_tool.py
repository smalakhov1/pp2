import pygame
from .base_tool import BaseTool

class RightTriangleTool(BaseTool):
    def __init__(self):
        # store starting position of right triangle
        self.start_pos = None

    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            self.start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if app.drawing and self.start_pos is not None:
                end_pos = event.pos
                points = self._get_triangle_points(self.start_pos, end_pos)
                # draw final right triangle on canvas
                pygame.draw.polygon(canvas, app.current_color, points, app.brush_size)
            app.drawing = False
            self.start_pos = None

    def draw_preview(self, surface, app):
        # draw temporary right triangle while dragging
        if app.drawing and self.start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()
            points = self._get_triangle_points(self.start_pos, mouse_pos)
            if len(points) == 3:
                pygame.draw.polygon(surface, app.current_color, points, app.brush_size)

    def _get_triangle_points(self, start, end):
        # points for a right triangle starting from top-left to bottom-right
        return [
            (start[0], start[1]), # top left
            (start[0], end[1]),   # bottom left
            (end[0], end[1])      # bottom right
        ]
