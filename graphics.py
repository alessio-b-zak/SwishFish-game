import pygame as pg
import os
import math
from settings import size, width, height

#position = x,y
def rotate(direction, angle):
    x = direction[0]
    y = direction[1]
    new_x = (x * math.cos(angle) - (y*math.sin(angle)))
    new_y = (x * math.sin(angle) + (y*math.cos(angle)))
    return new_x, new_y

def clip(val, minval, maxval):
        return min(max(val, minval), maxval)

def load_image(data_dir, name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
        image = pg.transform.scale2x(image)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def clip_object(world_object_rect):
    world_object_rect.left  = clip(world_object_rect.left, 0, width)
    world_object_rect.right = clip(world_object_rect.right, 0, width)
    world_object_rect.top  = clip(world_object_rect.top, 0, height)
    world_object_rect.bottom  = clip(world_object_rect.bottom, 0, height)
    return world_object_rect

def is_off_screen(world_object_rect):
    return (world_object_rect.left < (-110) or
            world_object_rect.right >  (110+width) or
            world_object_rect.top < (-110) or
            world_object_rect.bottom  > (height+110))
