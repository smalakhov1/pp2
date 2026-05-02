import pygame
from config import Colors

class UIManager:
    def __init__(self):
        self.font = pygame.font.SysFont("Verdana", 14)

        #color buttons
        self.color_rects = []
        for i,color in enumerate(Colors):
            rect = pygame.Rect(10+i*40,10,30,30) #-> 10+i*40 = left pos of rectangle
            self.color_rects.append((rect,color))

        self.tool_rects = []
        tools = ["pen","rect","circle","eraser"]
        for i,t in enumerate(tools):
            rect = pygame.Rect(10+i*80,50,70,30)
            self.tool_rects.append((rect,t))
        
    def handle_event(self,event,app):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                #color selection

                for rect, color in self.color_rects:
                    if rect.collidepoint(event.pos):
                        app.current_color = color.value
                        return True
                
                #tool selection

                for rect,t in self.tool_rects:
                    if rect.collidepoint(event.pos):
                        if t == "pen":
                            app.current_tool = app.pen_tool
                        elif t == "rect":
                            app.current_tool = app.rect_tool
                        elif t == "circle":
                            app.current_tool = app.circle_tool
                        elif t == "eraser":
                            app.current_tool = app.eraser_tool
                        return True
            return False
    def draw(self,surface, app):
        #draw colors
        for rect, color in self.color_rects:
            pygame.draw.rect(surface, color.value, rect)
            if app.current_color == color:
                pygame.draw.rect(surface, Colors.black.value,rect,2)
        #cdraw tools
        for rect,t in self.tool_rects:
            pygame.draw.rect(surface,(200,200,200), rect)

            text = self.font.render(t, True, Colors.black.value)
            surface.blit(text,(rect.x+5,rect.y+5))