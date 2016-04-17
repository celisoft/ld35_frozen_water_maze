#!/usr/bin/env python3
import os

import pygame
import pytmx
from pygame.locals import *
from pygame.sprite import collide_rect

from GamePlayer import Player
from GameTile import GameTile
from Dangers import Fire, Water


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
        self.game_tiles = []
        self.game_fires = []
        self.game_waters = []
        for coord_x in range(18):
            for coord_y in range(12):
                img = tmxdata.get_tile_image(coord_x, coord_y, 0)
                if img is not None:
                    self.game_tiles.append(GameTile(img, coord_x, coord_y))
                fire = tmxdata.get_tile_image(coord_x, coord_y, 1)
                if fire is not None:
                    self.game_fires.append(Fire(coord_x, coord_y))
                water = tmxdata.get_tile_image(coord_x, coord_y, 2)
                if water is not None:
                    self.game_waters.append(Water(water, coord_x, coord_y))

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

        # Init game background
        bg_path = os.path.dirname(__file__) + os.sep + "assets/bg.jpg"
        background = pygame.image.load(bg_path)

        # Init player
        self.player = Player()

        # Init internal event -> droplet fall
        pygame.time.set_timer(pygame.USEREVENT, 5000)

        # Game loop
        while not self.game_ended:
            self.screen.fill((0, 0, 0))
            self.check_game_event()

            self.screen.blit(background, Rect(0, 0, 64 * 18, 64 * 12))

            is_player_falling = False
            if self.player.current_shape != Player.PLAYER_CLOUD:
                is_player_falling = True

            for tile in self.game_tiles:
                tile.display(self.screen)
                if self.player.rect.bottom == tile.rect.top and self.player.rect.left == tile.rect.left:
                    is_player_falling = False

            for danger in self.game_waters:
                danger.display(self.screen)
                if self.player.rect.bottom == danger.rect.top and self.player.rect.left == danger.rect.left:
                    if self.player.current_shape != Player.PLAYER_CLOUD:
                        self.game_ended = True
                        is_player_falling = False
                elif collide_rect(self.player, danger):
                    self.game_ended = True
                    is_player_falling = False

            if is_player_falling:
                self.player.fall()

            for danger in self.game_fires:
                danger.display(self.screen)
                if collide_rect(self.player, danger):
                    self.game_ended = True

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
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_UP:
                    is_move_possible = True
                    for tile in self.game_tiles:
                        if self.player.rect.top == tile.rect.bottom and self.player.rect.left == tile.rect.left:
                            is_move_possible = False
                    if is_move_possible:
                        self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    is_move_possible = True
                    for tile in self.game_tiles:
                        if self.player.rect.bottom == tile.rect.top and self.player.rect.left == tile.rect.left:
                            is_move_possible = False
                    if is_move_possible:
                        self.player.move_down()
                elif event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.QUIT:
                self.game_ended = True


if __name__ == "__main__":
    FWMMain()
