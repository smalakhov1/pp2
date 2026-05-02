import pygame
import sys
from config import *

from ui.ui_manager import UIManager
from tools.pen_tool import PenTool
from tools.eraser_tool import EraserTool
from tools.rect_tool import RectTool
from tools.circle_tool import CircleTool


class PaintApp:

    #setup
    def __init__(self):
        pygame.init()
        #window
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Paint")
        #canvas
        self.canvas_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.canvas_surface.fill(Colors.white.value)
        #clock
        self.clock = pygame.time.Clock()
        #application lifecycle control
        self.running = True
        #application state
        self.current_color = Colors.black.value
        self.brush_size = 5

        self.drawing = False #is the mouse button pressed
        self.start_pos = None #where is the start
        self.last_pos = None #last position

        self.pen_tool = PenTool()
        self.eraser_tool = EraserTool()
        self.rect_tool = RectTool()
        self.circle_tool = CircleTool()

        self.current_tool = self.pen_tool

        #UI

        self.ui = UIManager()


    #runing loop
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.update_display()
        #exit if self.funning == false
        pygame.quit()
        sys.exit()

    #handling events
    def handle_events(self):
        #handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False #-> quiting the game cycle

            if self.ui.handle_event(event,self):
                continue

            self.current_tool.handle_event(event,self,self.canvas_surface)

    
    def render(self):
        self.display_surface.blit(self.canvas_surface, (0,0))
        self.current_tool.draw_preview(self.display_surface,self)
        self.ui.draw(self.display_surface,self)
    
    def update_display(self):
        pygame.display.update()
        self.clock.tick(FPS)