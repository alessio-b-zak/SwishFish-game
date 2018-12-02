import pygame as pg
import math

size = width, height = 1500, 1500

data_dir = "./assets"

def move_to_point(origin, destination, fps):
    dx, dy = (destination[0] - origin[0], destination[1] - origin[1])
    stepx, stepy = (dx/fps , dy/fps )
    return stepx, stepy

def distance(source, target):
    dist = math.sqrt((target[1]-source[1])**2 + (target[0]-source[0])**2)
    return dist
