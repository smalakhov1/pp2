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
        tools = ["pen","rect","circle","eraser", "square", "r_tri", "e_tri", "rhombus", "line", "fill", "text"]
        for i,t in enumerate(tools):
            rect = pygame.Rect(10+i*65,50,60,30)
            self.tool_rects.append((rect,t))
            
        self.slider_rect = pygame.Rect(10, 90, 200, 20)
        self.dragging_slider = False
        self.min_brush = 1
        self.max_brush = 50
        
    def _update_slider(self, pos, app):
        pct = (pos[0] - self.slider_rect.x) / self.slider_rect.width
        pct = max(0.0, min(1.0, pct)) # clamp to [0, 1]
        app.brush_size = int(self.min_brush + pct * (self.max_brush - self.min_brush))

    def handle_event(self,event,app):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging_slider = True
                self._update_slider(event.pos, app)
                return True
                
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
                    elif t == "square":
                        app.current_tool = app.square_tool
                    elif t == "r_tri":
                        app.current_tool = app.right_triangle_tool
                    elif t == "e_tri":
                        app.current_tool = app.equilateral_triangle_tool
                    elif t == "rhombus":
                        app.current_tool = app.rhombus_tool
                    elif t == "line":
                        app.current_tool = app.line_tool
                    elif t == "fill":
                        app.current_tool = app.flood_fill_tool
                    elif t == "text":
                        app.current_tool = app.text_tool
                    return True
                        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_slider:
                self._update_slider(event.pos, app)
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging_slider:
                self.dragging_slider = False
                return True
                
        return False

    def draw(self,surface, app):
        #draw colors
        for rect, color in self.color_rects:
            pygame.draw.rect(surface, color.value, rect)
            if app.current_color == color:
                pygame.draw.rect(surface, Colors.black.value,rect,2)
        #draw tools
        for rect,t in self.tool_rects:
            pygame.draw.rect(surface,(200,200,200), rect)

            text = self.font.render(t, True, Colors.black.value)
            surface.blit(text,(rect.x+5,rect.y+5))
            
        #draw slider
        pygame.draw.rect(surface, (200, 200, 200), self.slider_rect, border_radius=10)
        
        # draw filled part of slider
        pct = (app.brush_size - self.min_brush) / (self.max_brush - self.min_brush)
        filled_width = int(pct * self.slider_rect.width)
        filled_rect = pygame.Rect(self.slider_rect.x, self.slider_rect.y, filled_width, self.slider_rect.height)
        if filled_width > 0:
            pygame.draw.rect(surface, (100, 100, 100), filled_rect, border_radius=10)
            
        # draw handle
        handle_x = self.slider_rect.x + filled_width
        pygame.draw.circle(surface, Colors.black.value, (handle_x, self.slider_rect.centery), 10)
        
        # draw text
        text = self.font.render(f"Size: {app.brush_size}", True, Colors.black.value)
        surface.blit(text, (self.slider_rect.right + 15, self.slider_rect.y))