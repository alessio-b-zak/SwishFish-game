import pygame as pg
from graphics import *
from assets import *
from animation import *
from settings import *
from enum import Enum


class BackgroundSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer

        asset = data_dir + "/" + "background_animation.png"
        self.anim = SpriteStripAnim(asset, (0,0, 500,500), 20, loop=True, frames=9)
        self.image = pg.transform.scale(self.anim.next(), (height, width))
        self.rect = self.image.get_rect()
        # self.rect = (0,0)

    def animate(self):
        self.image = pg.transform.scale(self.anim.next(), (height, width))


    def update(self, dt):
        self.animate()

