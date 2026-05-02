import pygame
from .base_tool import BaseTool
from config import Colors

class EraserTool (BaseTool):
    #start erasing
    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            app.last_pos = event.pos
        # erase while moving (similar as pentool but with background color)
        if event.type == pygame.MOUSEMOTION:
            if app.drawing and app.last_pos is not None:
                pygame.draw.line(canvas, Colors.white.value, app.last_pos, event.pos, app.brush_size * 2)
                app.last_pos = event.pos
        #Stop erasing
        if event.type == pygame.MOUSEBUTTONUP and event.button ==1:
            app.drawing = False
            app.last_pos = None