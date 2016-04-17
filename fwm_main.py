#!/usr/bin/env python3
import os

import pygame
import pytmx
from pygame.locals import *

from GamePlayer import Player
from GameTile import GameTile


class FWMMain():
    def __init__(self):
        """ Init pygame """
        pygame.init()

        # Boolean values to know where we are in the game
        self.game_started = False
        self.game_paused = False
        self.game_ended = False

        # Clock
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((64 * 18, 64 * 12))
        pygame.display.set_caption('Frozen Water Maze')

        # Load data
        tmxdata = pytmx.load_pygame("assets/map.tmx")
        game_tiles = []
        for coord_x in range(18):
            for coord_y in range(12):
                img = tmxdata.get_tile_image(coord_x, coord_y, 0)
                if img is not None:
                    game_tiles.append(GameTile(img, coord_x, coord_y))

        # Init music
        music_path = os.path.dirname(__file__) + os.sep + "assets/sfx/bg_music.ogg"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

        # Init ambient motor sound
        ambient_motor_path = os.path.dirname(__file__) + os.sep + "assets/sfx/motor.ogg"
        ambient_motor = pygame.mixer.Sound(ambient_motor_path)
        ambient_motor.set_volume(0.15)
        ambient_motor.play(loops=-1)

        # Init ambient droplet fall sound
        droplet_path = os.path.dirname(__file__) + os.sep + "assets/sfx/droplet.ogg"
        self.ambient_droplet = pygame.mixer.Sound(droplet_path)
        self.ambient_droplet.set_volume(0.3)

        # Init player
        self.player = Player()

        # Init internal event -> droplet fall
        pygame.time.set_timer(pygame.USEREVENT, 5000)

        # Game loop
        while not self.game_ended:
            self.screen.clear()
            self.check_game_event()
            for tile in game_tiles:
                tile.display(self.screen)
            self.player.display(self.screen)
            pygame.time.wait(50)
            self.clock.tick(60)
            pygame.display.flip()

        pygame.quit()

    def check_game_event(self):
        """ Check game events """
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.ambient_droplet.play()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.player.shapeshift(Player.PLAYER_ICE)
                elif event.key == pygame.K_c:
                    self.player.shapeshift(Player.PLAYER_CLOUD)
                elif event.key == pygame.K_d:
                    self.player.shapeshift(Player.PLAYER_DROPLET)
            elif event.type == pygame.QUIT:
                self.game_ended = True

if __name__ == "__main__":
    FWMMain()
