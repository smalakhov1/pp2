import pygame
import math
from .base_tool import BaseTool

#same as rect_tool, but .draw.circle and radius

class CircleTool(BaseTool):

    def __init__(self):
        self.start_pos = None

    def handle_event(self, event, app, canvas):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            self.start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if app.drawing and self.start_pos is not None:

                dx = event.pos[0] - self.start_pos[0]
                dy = event.pos[1] - self.start_pos[1]
                radius = int(math.hypot(dx, dy))

                pygame.draw.circle(
                    canvas,
                    app.current_color,
                    self.start_pos,
                    radius,
                    app.brush_size
                )

            app.drawing = False
            self.start_pos = None

    def draw_preview(self, surface, app):
        if app.drawing and self.start_pos is not None:
            mouse_pos = pygame.mouse.get_pos()

            dx = mouse_pos[0] - self.start_pos[0]
            dy = mouse_pos[1] - self.start_pos[1]
            radius = int(math.hypot(dx, dy))

            pygame.draw.circle(
                surface,
                app.current_color,
                self.start_pos,
                radius,
                app.brush_size
            )