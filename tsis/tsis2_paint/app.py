import pygame
import sys
from config import *

from ui.ui_manager import UIManager
from tools.pen_tool import PenTool
from tools.eraser_tool import EraserTool
from tools.rect_tool import RectTool
from tools.circle_tool import CircleTool
from tools.square_tool import SquareTool
from tools.right_triangle_tool import RightTriangleTool
from tools.equilateral_triangle_tool import EquilateralTriangleTool
from tools.rhombus_tool import RhombusTool
from tools.line_tool import LineTool
from tools.flood_fill_tool import FloodFillTool
from tools.text_tool import TextTool
import datetime


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
        self.square_tool = SquareTool()
        self.right_triangle_tool = RightTriangleTool()
        self.equilateral_triangle_tool = EquilateralTriangleTool()
        self.rhombus_tool = RhombusTool()
        self.line_tool = LineTool()
        self.flood_fill_tool = FloodFillTool()
        self.text_tool = TextTool()

        self.current_tool = self.pen_tool

        #uI

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

            if event.type == pygame.KEYDOWN:
                # brush size shortcuts
                if event.key == pygame.K_1:
                    self.brush_size = 2
                elif event.key == pygame.K_2:
                    self.brush_size = 5
                elif event.key == pygame.K_3:
                    self.brush_size = 10
                
                # save on Ctrl+S or Cmd+S
                if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    pygame.image.save(self.canvas_surface, f"paint_save_{timestamp}.png")
                    print(f"Saved canvas to paint_save_{timestamp}.png")

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