#!/usr/bin/env python3
import os

import pygame
import pytmx
from pygame.locals import *
from pygame.sprite import collide_rect

from Collectible import Collectible
from GamePlayer import Player
from GameTile import GameTile
from Dangers import Fire, Water
from Grid import Grid


class FWMMain():
    def __init__(self):
        """ Init pygame """
        pygame.init()

        # Boolean values to know where we are in the game
        self.game_started = False
        self.game_paused = False
        self.game_ended = False
        self.text = "Too bad !"
        # Clock
        self.clock = pygame.time.Clock()

        # Setting up the display
        pygame.display.set_caption('Frozen Water Maze')
        icon_path = os.path.dirname(__file__) + os.sep + "assets/ico.png"
        pygame.display.set_icon(pygame.image.load(icon_path))
        self.screen = pygame.display.set_mode((64 * 18, 64 * 12))

        self.font = pygame.font.Font(None, 36)

        # Load data
        tmxpath = os.path.dirname(__file__) + os.sep + "assets/map.tmx"
        tmxdata = pytmx.load_pygame(tmxpath)
        self.game_tiles = []
        self.game_fires = []
        self.game_waters = []
        self.game_collectibles = []
        self.game_grids = []
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
                collectible = tmxdata.get_tile_image(coord_x, coord_y, 3)
                if collectible is not None:
                    self.game_collectibles.append(Collectible(coord_x, coord_y))
                grid = tmxdata.get_tile_image(coord_x, coord_y, 4)
                if grid is not None:
                    self.game_grids.append(Grid(grid, coord_x, coord_y))

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

        # Init get sound
        get_path = os.path.dirname(__file__) + os.sep + "assets/sfx/get.ogg"
        self.get_sfx = pygame.mixer.Sound(get_path)
        self.get_sfx.set_volume(0.2)

        # Init game
        # ground
        bg_path = os.path.dirname(__file__) + os.sep + "assets/bg.jpg"
        self.background_img = pygame.image.load(bg_path)

        # Init player
        self.player = Player()

        # Init score
        self.score = 0
        self.score_image = self.font.render(str(self.score), True, (255, 255, 255))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 5
        self.score_rect.left = 64

        # Init timer
        self.timer = 20
        timer_path = os.path.dirname(__file__) + os.sep + "assets/timer.png"
        self.timer_image = pygame.image.load(timer_path)
        self.timer_rect = self.timer_image.get_rect()
        self.timer_rect.top = 5
        self.timer_rect.left = self.screen.get_width() - 64
        self.timer_text_image = self.font.render(str(self.timer), True, (255, 255, 255))
        self.timer_text_rect = self.timer_text_image.get_rect()
        self.timer_text_rect.top = 24
        self.timer_text_rect.left = self.screen.get_width() - 92

        # Startup screen display
        startup_img_path = os.path.dirname(__file__) + os.sep + "assets/title.jpg"
        self.startup_image = pygame.image.load(startup_img_path)
        self.screen.fill((0, 0, 0))
        startup_screen_display = True

        while startup_screen_display:
            self.screen.blit(self.startup_image, Rect(0, 0, self.screen.get_width(), self.screen.get_height()))
            pygame.display.flip()
            pygame.time.wait(3000)
            startup_screen_display = False

        # Init internal event -> droplet fall
        pygame.time.set_timer(pygame.USEREVENT, 5000)

        # Init internal event -> timer decrease
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

        # Game loop
        while not self.game_ended:
            self.screen.fill((0, 0, 0))
            self.check_game_event()

            self.screen.blit(self.background_img, Rect(0, 0, 64 * 18, 64 * 12))

            self.screen.blit(self.score_image, self.score_rect)
            self.screen.blit(self.timer_image, self.timer_rect)
            self.screen.blit(self.timer_text_image, self.timer_text_rect)

            is_player_falling = False
            if self.player.current_shape != Player.PLAYER_CLOUD:
                is_player_falling = True

            for tile in self.game_tiles:
                tile.display(self.screen)
                if self.player.rect.bottom == tile.rect.top and self.player.rect.left == tile.rect.left:
                    is_player_falling = False

            for tile in self.game_grids:
                tile.display(self.screen)
                if self.player.rect.bottom == tile.rect.top and self.player.rect.left == tile.rect.left and self.player.current_shape == Player.PLAYER_ICE:
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

            for point in self.game_collectibles:
                point.display(self.screen)
                if collide_rect(self.player, point):
                    self.score += 1
                    self.get_sfx.play()
                    self.game_collectibles.remove(point)
                    self.score_image = self.font.render(str(self.score), True, (255, 255, 255))

            if self.game_collectibles.__len__()==0:
                self.game_ended=True
                self.text = "Congrat's !!"
            self.player.display(self.screen)

            pygame.time.wait(50)
            self.clock.tick(60)
            pygame.display.flip()

        self.startup_screen_display = True
        cpt = 0
        while self.startup_screen_display:
            self.screen.blit(self.background_img, (0, 0))
            # Endscreen text ( by default text is "Too bad !" )
            # ( if game_collectibles(len) == 0: "Congrat's!"  )
            font = pygame.font.SysFont('Arial', 100, True)
            text= font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.midtop = ( 550, 300)
            self.screen.blit(text, text_rect)

            pygame.time.wait(300)
            pygame.display.flip()
            cpt += 1
            if cpt ==10:
                self.startup_screen_display = False
        pygame.quit()

    def check_game_event(self):
        """ Check game events """
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.ambient_droplet.play()
            elif event.type == pygame.USEREVENT + 1:
                if self.timer == 0:
                    self.game_ended = True
                self.timer -= 1
                self.timer_text_image = self.font.render(str(self.timer), True, (255, 255, 255))
            elif event.type == pygame.USEREVENT + 2:
                self.player.shapeshift(Player.PLAYER_DROPLET)
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.player.shapeshift(Player.PLAYER_ICE)
                elif event.key == pygame.K_c:
                    self.player.shapeshift(Player.PLAYER_CLOUD)
                    pygame.time.set_timer(pygame.USEREVENT + 2, 2000)
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
                elif event.key == pygame.K_ESCAPE:
                    self.game_ended = True
            elif event.type == pygame.QUIT:
                self.game_ended = True


if __name__ == "__main__":
    FWMMain()
