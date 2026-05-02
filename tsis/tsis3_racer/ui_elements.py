import pygame
from config import Colors

class Button:
    def __init__(self, x, y, width, height, text, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("Verdana", font_size)
        self.is_hovered = False

    def draw(self, surface):
        color = Colors.GRAY.value if self.is_hovered else Colors.ROAD.value
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, Colors.WHITE.value, self.rect, 2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, Colors.WHITE.value)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

class TextInput:
    def __init__(self, x, y, width, height, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.SysFont("Verdana", font_size)
        self.active = False

    def draw(self, surface):
        color = Colors.WHITE.value if self.active else Colors.GRAY.value
        pygame.draw.rect(surface, Colors.BLACK.value, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, Colors.WHITE.value)
        surface.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE:
                if len(self.text) < 15: # max length
                    self.text += event.unicode
