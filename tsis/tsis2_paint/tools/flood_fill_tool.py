import pygame
from .base_tool import BaseTool

class FloodFillTool(BaseTool):
    def __init__(self):
        pass

    def handle_event(self, event, app, canvas):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = event.pos
            
            target_color = canvas.get_at(start_pos)
            fill_color = pygame.Color(app.current_color)
            
            # if the color is already the fill color, do nothing
            if target_color == fill_color:
                return

            # perform BFS for flood fill using get_at and set_at
            width, height = canvas.get_size()
            queue = [start_pos]
            
            # keep track of visited pixels to avoid infinite loops and redundant checks
            # we can just check the color on the canvas, but python sets are faster
            visited = set()
            visited.add(start_pos)

            while queue:
                x, y = queue.pop(0)
                
                # set color
                canvas.set_at((x, y), fill_color)

                # check neighbors (up, down, left, right)
                for nx, ny in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
                    if 0 <= nx < width and 0 <= ny < height:
                        if (nx, ny) not in visited:
                            if canvas.get_at((nx, ny)) == target_color:
                                queue.append((nx, ny))
                                visited.add((nx, ny))

    def draw_preview(self, surface, app):
        # flood fill does not need a dragging preview
        pass
