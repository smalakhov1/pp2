import pygame
from .base_tool import BaseTool

class RhombusTool(BaseTool):
    def __init__(self):
        # store starting position of rhombus
        self.start_pos = None

    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            self.start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if app.drawing and self.start_pos is not None:
                end_pos = event.pos
                points = self._get_rhombus_points(self.start_pos, end_pos)
                # draw final rhombus on canvas
                pygame.draw.polygon(canvas, app.current_color, points, app.brush_size)
            app.drawing = False
            self.start_pos = None

    def draw_preview(self, surface, app):
        # draw temporary rhombus while dragging
        if app.drawing and self.start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()
            points = self._get_rhombus_points(self.start_pos, mouse_pos)
            if len(points) == 4:
                pygame.draw.polygon(surface, app.current_color, points, app.brush_size)

    def _get_rhombus_points(self, start, end):
        # calculate midpoints of the bounding box
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        
        return [
            (mid_x, start[1]), # top
            (end[0], mid_y),   # right
            (mid_x, end[1]),   # bottom
            (start[0], mid_y)  # left
        ]
