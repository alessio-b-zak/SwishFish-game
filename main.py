import pygame as pg
import sys
import os
from graphics import load_image
from fish import FishSprite
from background import *
from settings import width, height, data_dir

class Scene():
    def __init__(self):
        self.background_sprite_group = pg.sprite.LayeredUpdates()
        self.fish_sprite_group = pg.sprite.LayeredUpdates()
        self.sprite_groups = [self.background_sprite_group, self.fish_sprite_group]
        self.background_sprite_group.add(BackgroundSprite())
        self.fish_sprite_group.add(FishSprite((width/2, height/2), (pg.K_a, pg.K_d, pg.K_w)))

    def get_event(self, event):
        pass

    def update(self, screen, dt):
        for group in self.sprite_groups:
            group.update(dt)
        self.calculate_collisions()
        self.draw(screen)

    def calculate_collisions(self):
        pass

    def draw(self, screen):
        for group in self.sprite_groups:
            group.draw(screen)

class TitleScene:
    def __init__(self):
        self.back_im, _ = load_image(data_dir, "title.png")

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            print("here")
            start_game_event = pg.event.Event(pg.USEREVENT, {"start_game": True})
            pg.event.post(start_game_event)


    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        back_im_scaled = pg.transform.scale(self.back_im, (height,width))
        screen.blit(back_im_scaled, (0,0))

class Game:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.title = False
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
        self.state = TitleScene()
    def update(self, dt):
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            self.state.get_event(event)
            if event.type == pg.QUIT:
                self.done = True
            #To allow title screen
            elif event.type == pg.USEREVENT and not self.title:
                self.title = True
                self.state = Scene()
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()

if __name__ == '__main__':
    pg.init()
    settings = {
        'size':(width, height),
        'fps' :60
    }

    app = Game(**settings)
    app.main_game_loop()
    pg.quit()
