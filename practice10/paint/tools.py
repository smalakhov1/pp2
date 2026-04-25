import pygame

class PaintTool:
    def __init__(self):
        self.drawing = False
        self.last_pos = None
        self.color = (0, 0, 0)
        self.radius = 5
        self.tool_type = 'pen' # 'pen', 'rect', 'circle', 'eraser'
        self.start_pos = None

    def handle_event(self, event, surface):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                self.drawing = True
                self.last_pos = event.pos
                self.start_pos = event.pos
                
                # draw single point immediately for pen or eraser
                if self.tool_type in ['pen', 'eraser']:
                    color = (255, 255, 255) if self.tool_type == 'eraser' else self.color
                    radius = self.radius * 2 if self.tool_type == 'eraser' else self.radius
                    pygame.draw.circle(surface, color, event.pos, radius)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False
                # finalize shape for rect and circle
                if self.tool_type == 'rect' and self.start_pos:
                    rect = pygame.Rect(self.start_pos[0], self.start_pos[1], 
                                       event.pos[0] - self.start_pos[0], 
                                       event.pos[1] - self.start_pos[1])
                    rect.normalize()
                    pygame.draw.rect(surface, self.color, rect, 2)
                elif self.tool_type == 'circle' and self.start_pos:
                    # calculate radius
                    dx = event.pos[0] - self.start_pos[0]
                    dy = event.pos[1] - self.start_pos[1]
                    radius = int((dx**2 + dy**2)**0.5)
                    pygame.draw.circle(surface, self.color, self.start_pos, radius, 2)
                    
                self.last_pos = None
                self.start_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if self.drawing:
                if self.tool_type == 'pen':
                    pygame.draw.line(surface, self.color, self.last_pos, event.pos, self.radius * 2)
                    # draw circles at points for smooth lines
                    pygame.draw.circle(surface, self.color, event.pos, self.radius)
                    self.last_pos = event.pos
                elif self.tool_type == 'eraser':
                    color = (255, 255, 255)
                    pygame.draw.line(surface, color, self.last_pos, event.pos, self.radius * 4)
                    pygame.draw.circle(surface, color, event.pos, self.radius * 2)
                    self.last_pos = event.pos

    def draw_preview(self, surface):
        # draw preview for shapes while mouse is held
        if self.drawing and self.start_pos:
            mouse_pos = pygame.mouse.get_pos()
            if self.tool_type == 'rect':
                rect = pygame.Rect(self.start_pos[0], self.start_pos[1], 
                                   mouse_pos[0] - self.start_pos[0], 
                                   mouse_pos[1] - self.start_pos[1])
                rect.normalize()
                pygame.draw.rect(surface, self.color, rect, 2)
            elif self.tool_type == 'circle':
                dx = mouse_pos[0] - self.start_pos[0]
                dy = mouse_pos[1] - self.start_pos[1]
                radius = int((dx**2 + dy**2)**0.5)
                pygame.draw.circle(surface, self.color, self.start_pos, radius, 2)
