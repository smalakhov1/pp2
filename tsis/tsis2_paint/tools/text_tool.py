import pygame
from .base_tool import BaseTool

class TextTool(BaseTool):
    def __init__(self):
        self.start_pos = None
        self.text = ""
        self.font = pygame.font.SysFont("Verdana", 24)

    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # place cursor and reset text
            self.start_pos = event.pos
            self.text = ""

        if event.type == pygame.KEYDOWN and self.start_pos is not None:
            if event.key == pygame.K_RETURN:
                # commit text to canvas
                self._render_text(canvas, app.current_color)
                self.start_pos = None
                self.text = ""
            elif event.key == pygame.K_ESCAPE:
                # cancel
                self.start_pos = None
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                # remove last character
                self.text = self.text[:-1]
            else:
                # append typed character
                self.text += event.unicode

    def draw_preview(self, surface, app):
        if self.start_pos is not None:
            # render a preview of the text
            self._render_text(surface, app.current_color)
            
            # render a blinking cursor effect
            if pygame.time.get_ticks() % 1000 < 500:
                text_surface = self.font.render(self.text, True, app.current_color)
                cursor_x = self.start_pos[0] + text_surface.get_width()
                pygame.draw.line(surface, app.current_color, 
                                 (cursor_x, self.start_pos[1]), 
                                 (cursor_x, self.start_pos[1] + text_surface.get_height()), 2)

    def _render_text(self, surface, color):
        if self.text:
            text_surface = self.font.render(self.text, True, color)
            surface.blit(text_surface, self.start_pos)
