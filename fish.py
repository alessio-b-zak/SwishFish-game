import pygame as pg
from graphics import *
from assets import *
from settings import *
from animation import *
from enum import Enum

class FishForwardState(Enum):
    FORWARD_IDLE = 0
    FORWARD_FORWARD = 1

class FishSideState(Enum):
    MOVING_LEFT = 0
    MOVING_RIGHT = 2
    SIDE_IDLE = 4

class FishSprite(pg.sprite.Sprite):
    def __init__(self, initial_position, controls):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer
        asset = data_dir + "/" + "slug_walk_right_small.png"
        self.anim = SpriteStripAnim(asset, (0,0,73,73), 4, -1, True, 12)
        self.image = pg.transform.scale2x(self.anim.next())
        self.rect = self.image.get_rect()
        self.rect.center = initial_position

        self.forward_state = FishForwardState.FORWARD_IDLE
        self.side_state = FishSideState.SIDE_IDLE

        self.original_direction = (1,0)
        self.direction = (1,0)
        self.move_rate = 5
        self.rotation_degree = 0.05

        self.left_key = controls[0]
        self.right_key = controls[1]
        self.forward_key = controls[2]

    def change_direction(self):
        if self.side_state == FishSideState.MOVING_LEFT:
            new_direction = rotate(self.direction, -1 * self.rotation_degree)
            self.direction = new_direction
        elif self.side_state == FishSideState.MOVING_RIGHT:
            new_direction = rotate(self.direction, self.rotation_degree)
            self.direction = new_direction

    def apply_movement(self):
        self.change_direction()
        if self.forward_state == FishForwardState.FORWARD_FORWARD:
            newpos = self.rect.move(*tuple(self.move_rate*x for x in self.direction))
            self.rect = newpos
        newpos = clip_object(self.rect)
        self.rect = newpos

    def get_event(self, event):
        move_type = event.dict["movement"]
        if move_type == ImageInsEnum.RIGHT:
            self.side_state = FishSideState.MOVING_RIGHT
        elif move_type == ImageInsEnum.LEFT:
            self.side_state = FishSideState.MOVING_LEFT
        elif not (move_type == ImageInsEnum.RIGHT or move_type == ImageInsEnum.LEFT):
            self.side_state = FishSideState.SIDE_IDLE
        if move_type == ImageInsEnum.FORWARD:
            self.forward_state = FishForwardState.FORWARD_FORWARD
        elif move_type == ImageInsEnum.PAUSE:
            self.forward_state = FishForwardState.FORWARD_IDLE

    def animate(self):
        self.image = pg.transform.scale2x(self.anim.next())
        angle = calc_angle(self.original_direction, self.direction)
        self.image = pg.transform.rotate(self.image, (360 - math.degrees(angle)))

    def update(self, dt):
        self.apply_movement()
        self.animate()
