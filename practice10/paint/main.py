import pygame
import sys
from config import *
from tools import PaintTool

pygame.init()

display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint")

# the surface we draw on (persists shapes)
canvas_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas_surf.fill(WHITE)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 14)

paint_tool = PaintTool()

# ui elements
color_rects = []
for i, color in enumerate(COLORS):
    rect = pygame.Rect(10 + i * 40, 10, 30, 30)
    color_rects.append((rect, color))

tool_rects = []
tools = ['pen', 'rect', 'circle', 'eraser']
for i, t in enumerate(tools):
    rect = pygame.Rect(10 + i * 60, 50, 50, 30)
    tool_rects.append((rect, t))

def draw_ui():
    # draw colors
    for rect, color in color_rects:
        pygame.draw.rect(display_surf, color, rect)
        if paint_tool.color == color and paint_tool.tool_type != 'eraser':
            pygame.draw.rect(display_surf, BLACK, rect, 2)
    
    # draw tool buttons
    for rect, t in tool_rects:
        pygame.draw.rect(display_surf, (200, 200, 200), rect)
        if paint_tool.tool_type == t:
            pygame.draw.rect(display_surf, BLACK, rect, 2)
        text = font.render(t, True, BLACK)
        display_surf.blit(text, (rect.x + 5, rect.y + 5))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # check ui clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_ui = False
            for rect, color in color_rects:
                if rect.collidepoint(event.pos):
                    paint_tool.color = color
                    if paint_tool.tool_type == 'eraser':
                        paint_tool.tool_type = 'pen' # switch to pen if color selected
                    clicked_ui = True
            
            for rect, t in tool_rects:
                if rect.collidepoint(event.pos):
                    paint_tool.tool_type = t
                    clicked_ui = True

            if clicked_ui:
                # ignore drawing action if clicked ui
                continue

        # handle drawing on canvas
        paint_tool.handle_event(event, canvas_surf)

    # draw canvas to display
    display_surf.blit(canvas_surf, (0, 0))
    
    # draw preview shapes on top of canvas (not persisted yet)
    paint_tool.draw_preview(display_surf)
    
    # draw ui on top
    draw_ui()

    pygame.display.update()
    clock.tick(FPS)
