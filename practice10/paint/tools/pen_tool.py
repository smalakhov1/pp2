import pygame
from .base_tool import BaseTool

class PenTool(BaseTool):

    def handle_event(self, event, app, canvas):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            app.last_pos = event.pos

        #draw while moving
        if event.type == pygame.MOUSEMOTION:
            if app.drawing and app.last_pos is not None:
                pygame.draw.line(
                    canvas,
                    app.current_color,
                    app.last_pos,
                    event.pos,
                    app.brush_size)
                app.last_pos = event.pos
            #stop moving
        if event.type ==  pygame.MOUSEBUTTONUP and event.button == 1:
                app.drawing = False
                app.last_pose = None

                