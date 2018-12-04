import pygame as pg
import math
from enum import Enum

size = width, height = 1500, 1500

class ImageInsEnum(Enum):
    RIGHT = 0
    LEFT = 1
    PAUSE = 2
    FORWARD = 4

control_mapping = {0: ImageInsEnum.RIGHT, 1: ImageInsEnum.LEFT, 2: ImageInsEnum.PAUSE, 3: ImageInsEnum.FORWARD}

data_dir = "./assets"

def move_to_point(origin, destination, fps):
    dx, dy = (destination[0] - origin[0], destination[1] - origin[1])
    stepx, stepy = (dx/fps , dy/fps )
    return stepx, stepy


def calc_angle(vec1, vec2):
    x1, y1, = vec1
    x2, y2, = vec2
    dot = x1*x2 + y1*y2      # dot product between [x1, y1] and [x2, y2]
    det = x1*y2 - y1*x2      # determinant
    return  math.atan2(det, dot)


def distance(source, target):
    dist = math.sqrt((target[1]-source[1])**2 + (target[0]-source[0])**2)
    return dist
