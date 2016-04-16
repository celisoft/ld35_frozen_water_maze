#!/usr/bin/env python3

import pygame
import pytmx
from pygame.locals import *


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

        self.screen = pygame.display.set_mode((64*18, 64*12))
        pygame.display.set_caption('Hello Pygame World!')

        # Load data
        tmxdata = pytmx.load_pygame("assets/map.tmx")
        map_tiles = []
        for coord_x in range(0, 18):
            y_tiles = []
            for coord_y in range(0, 12):
                img = tmxdata.get_tile_image(coord_x, coord_y, 0)
                if img is not None:
                    img_rect = img.get_rect().copy()
                    img_rect.left = coord_x*64
                    img_rect.top = coord_y*64
                    y_tiles.append([img, img_rect])
            map_tiles.append(y_tiles)
            del y_tiles

        # Game loop
        while not self.game_ended:
            for map_line in map_tiles:
                for img in map_line:
                    self.screen.blit(img[0], img[1])
            pygame.time.wait(50)
            self.clock.tick(60)
            pygame.display.flip()


if __name__ == "__main__":
    FWMMain()
