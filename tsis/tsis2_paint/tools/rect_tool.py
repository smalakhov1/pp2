import pygame
from .base_tool import BaseTool

class RectTool(BaseTool):

    def __init__(self):
        # store starting position of rectangle
        self.start_pos = None

    def handle_event(self, event, app, canvas):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            app.drawing = True
            self.start_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if app.drawing and self.start_pos is not None:
                end_pos = event.pos

                rect = pygame.Rect(self.start_pos[0], #left
                                   self.start_pos[1], #top
                                   end_pos[0] - self.start_pos[0], #width
                                   end_pos[1] - self.start_pos[1]) #height
                rect.normalize()
                #draw final rectangle on canvas
                pygame.draw.rect(canvas, app.current_color, rect, app.brush_size)
            app.drawing = False
            self.start_pos = None

    def draw_preview(self, surface, app):
        #draw temporary rect while dragging
        if app.drawing and self.start_pos is not None:
            mouse_pos = pygame.mouse.get_pos() #event.pos cannot be reached since it occurs only in event loop and we are now handling the preview that happening directly in render(), so we are using get_pos() to get the position

            rect = pygame.Rect(self.start_pos[0], #left
                                   self.start_pos[1], #top
                                   mouse_pos[0] - self.start_pos[0], #width
                                   mouse_pos[1] - self.start_pos[1]) #height
            rect.normalize()

            pygame.draw.rect(
                surface,
                app.current_color,
                rect,
                app.brush_size
            )
            

    