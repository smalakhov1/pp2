import pygame
from .base_tool import BaseTool

class LineTool(BaseTool):
    def __init__(self):
        # store starting position of the line
        self.start_pos = None

    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            self.start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if app.drawing and self.start_pos is not None:
                end_pos = event.pos
                # draw final straight line on canvas
                pygame.draw.line(canvas, app.current_color, self.start_pos, end_pos, app.brush_size)
            app.drawing = False
            self.start_pos = None

    def draw_preview(self, surface, app):
        # draw temporary straight line while dragging
        if app.drawing and self.start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(surface, app.current_color, self.start_pos, mouse_pos, app.brush_size)
