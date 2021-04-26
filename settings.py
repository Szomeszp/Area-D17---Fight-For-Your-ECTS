import pygame as pg
from enum import Enum

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Area-D17---Fight-For-Your-ECTS"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE


class PlayerImg(Enum):
    LEFT = "player_left.png"
    RIGHT = "player_right.png"
    UP = "player_up.png"
    DOWN = "player_down.png"
    LEFT2 = "player_left2.png"
    RIGHT2 = "player_right2.png"
    UP2 = "player_up2.png"
    DOWN2 = "player_down2.png"
    STATIC_LEFT = "player_static_left.png"
    STATIC_RIGHT = "player_static_right.png"
    STATIC_UP = "player_static_up.png"
    STATIC_DOWN = "player_static_down.png"


PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

SECRET_ROOM_PNG = ""
