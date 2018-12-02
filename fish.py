import pygame as pg
from graphics import *
from assets import *
from settings import height, width, size
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

        self.direction = (1,0)
        self.angle = 0
        self.move_rate = 10
        self.rotation_degree = 0.05

        self.left_key = controls[0]
        self.right_key = controls[1]
        self.forward_key = controls[2]

    def change_direction(self):
        if self.side_state == FishSideState.MOVING_LEFT:
            new_direction = rotate(self.direction, -1 * self.rotation_degree)
            self.direction = new_direction
            self.angle = (self.angle + 0.5) % 360
        elif self.side_state == FishSideState.MOVING_RIGHT:
            new_direction = rotate(self.direction, self.rotation_degree)
            self.direction = new_direction
            self.angle = (self.angle - 0.5) % 360

    def apply_movement(self):
        self.change_direction()
        if self.forward_state == FishForwardState.FORWARD_FORWARD:
            print(self.direction)
            newpos = self.rect.move(*tuple(self.move_rate*x for x in self.direction))
            self.rect = newpos
        newpos = clip_object(self.rect)
        self.rect = newpos

    def calculate_state(self):
        keys = pg.key.get_pressed()
        if keys[self.right_key]:
            self.side_state = FishSideState.MOVING_RIGHT
        elif keys[self.left_key]:
            self.side_state = FishSideState.MOVING_LEFT
        if not (keys[self.right_key] or keys[self.left_key]):
            self.side_state = FishSideState.SIDE_IDLE
        if keys[self.forward_key]:
            self.forward_state = FishForwardState.FORWARD_FORWARD
        elif not keys[self.forward_key]:
            self.forward_state = FishForwardState.FORWARD_IDLE

    def animate(self):
        self.image = pg.transform.scale2x(self.anim.next())

    def update(self, dt):
        self.calculate_state()
        self.apply_movement()
        self.animate()
