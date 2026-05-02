import pygame
import math
from .base_tool import BaseTool

class EquilateralTriangleTool(BaseTool):
    def __init__(self):
        # store starting position of equilateral triangle
        self.start_pos = None

    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            self.start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if app.drawing and self.start_pos is not None:
                end_pos = event.pos
                points = self._get_triangle_points(self.start_pos, end_pos)
                # draw final equilateral triangle on canvas
                pygame.draw.polygon(canvas, app.current_color, points, app.brush_size)
            app.drawing = False
            self.start_pos = None

    def draw_preview(self, surface, app):
        # draw temporary equilateral triangle while dragging
        if app.drawing and self.start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()
            points = self._get_triangle_points(self.start_pos, mouse_pos)
            if len(points) == 3:
                pygame.draw.polygon(surface, app.current_color, points, app.brush_size)

    def _get_triangle_points(self, start, end):
        # use width to determine height of equilateral triangle (h = w * sqrt(3) / 2)
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        width = abs(dx)
        
        # calculate proper height
        height = width * (math.sqrt(3) / 2)
        sign_y = 1 if dy >= 0 else -1
        
        # top vertex
        top_x = start[0] + dx / 2
        top_y = start[1]
        
        # bottom vertices
        bottom_y = start[1] + height * sign_y
        left_x = start[0]
        right_x = start[0] + dx
        
        return [
            (top_x, top_y),
            (left_x, bottom_y),
            (right_x, bottom_y)
        ]
