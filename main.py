import pygame as pg
import sys
import os
import time
import select
from graphics import load_image
from fish import FishSprite
from background import *
from settings import width, height, data_dir, ImageInsEnum, control_mapping

class Scene():
    def __init__(self, players):
        self.background_sprite_group = pg.sprite.LayeredUpdates()
        self.fish_sprite_group = pg.sprite.LayeredUpdates()
        self.sprite_groups = [self.background_sprite_group, self.fish_sprite_group]
        self.background_sprite_group.add(BackgroundSprite())
        self.instruction_receivers = []
        self.read_input = 0
        for i in range(1,players+1):
            self.fish_sprite_group.add(FishSprite((width/2 + (10*i), height/2), i))
            self.instruction_receivers.append(InstructionReceiver("pipe_", i))

    def get_event(self, event):
        if event.type == pg.USEREVENT:
            if "movement" in event.dict:
                self.fish_sprite_group.get_sprite(event.dict["id"]-1).get_event(event)

    def update(self, screen, dt):
        for group in self.sprite_groups:
            group.update(dt)
        self.draw(screen)
        # print("Reading input")
        self.read_input = 0
        for instruction_receiver in self.instruction_receivers:
            instruction_receiver.update()
        self.read_input += dt

    def calculate_collisions(self):
        pass

    def draw(self, screen):
        for group in self.sprite_groups:
            group.draw(screen)

class InstructionReceiver:
    def __init__(self, pipe_name, insid):
        self.id = insid
        # self.write_dir = write_dir + str(insid) + "/"
        # if not os.path.isdir(self.write_dir):
        #     os.mkdir(self.write_dir)

        if not os.path.exists(pipe_name + str(insid)):
            os.mkfifo(pipe_name + str(insid))
        self.pipein = open(pipe_name + str(insid), 'r')

    def fetch_code(self):
        r, w, e = select.select([ self.pipein ], [], [], 0)
        if self.pipein in r:
            return self.pipein.readline()[:-1]
        else:
             return None

    def decode_txt(self, line):
        try:
            moving_map = control_mapping[line]
            # print("found input ")
            return moving_map
        except:
            pass

    def raise_event(self, moving_enum):
        move_player_event =  pg.event.Event(pg.USEREVENT, {"movement": moving_enum, "id": self.id} )
        pg.event.post(move_player_event)

    def update(self):
        # print("updating")
        text_file = self.fetch_code()
        if text_file is not None:
            event = self.decode_txt(text_file)
            self.raise_event(event)

class TitleScene:
    def __init__(self):
        self.back_im, _ = load_image(data_dir, "title.png")

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # print("here")
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
            elif event.type == pg.USEREVENT and not self.title and ("start_game" in event.dict):
                self.title = True
                self.state = Scene(3)
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
