import pygame as pg
from graphics import *
from assets import *
from animation import *
from settings import *
from enum import Enum


class BackgroundSprite(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) #call Sprite initializer

        asset = data_dir + "/" + "fish_background.png"
        self.image = pg.transform.scale(pg.image.load(asset), size)
        self.rect = self.image.get_rect()
        # self.rect = (0,0)

    def animate(self):
        pass

    def update(self, dt):
        pass
