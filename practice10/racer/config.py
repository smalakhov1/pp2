from enum import Enum

#screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

#road settings
ROAD_LEFT = 80
ROAD_WIDTH = 240
LANE_COUNT = 3

#player pos
PLAYER_Y = SCREEN_HEIGHT - 120

#spawn timing (mls)
SPAWN_INTERVAL = 1200
COIN_SPAWN_INTERVAL = 900

#color defin enum
class Colors(Enum):
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GRAY = (50,50,50)
    ROAD = (60,60,60)
    GRASS = (30,120,40)
    RED = (220,40,40)
    BLUE = (40,100,220)
    YELLOW = (250,210,60)

def get_lanes():
    lane_width = ROAD_WIDTH/LANE_COUNT
    return [int(ROAD_LEFT+lane_width*(i+0.5)) for i in range(LANE_COUNT)]
LANES = get_lanes()
