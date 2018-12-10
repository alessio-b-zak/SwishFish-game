import pygame as pg
import math
from enum import Enum

size = width, height = 800, 800

class ImageInsEnum(Enum):
    LEFT = 0
    FORWARD = 1
    RIGHT = 2
    PAUSE = 4

control_mapping = {"0": ImageInsEnum.LEFT, "1": ImageInsEnum.FORWARD, "2": ImageInsEnum.RIGHT, "3": ImageInsEnum.PAUSE}

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
