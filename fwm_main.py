#!/usr/bin/env python3

import pygame
import pytmx
from pygame.locals import *

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
        for coord_x in range(0, 18):
            for coord_y in range(0, 12):
                img = tmxdata.get_tile_image(coord_x, coord_y, 0)
                if img is not None:
                    game_tiles.append(GameTile(img, coord_x, coord_y))

        # Game loop
        while not self.game_ended:
            for tile in game_tiles:
                tile.display(self.screen)
            pygame.time.wait(50)
            self.clock.tick(60)
            pygame.display.flip()


if __name__ == "__main__":
    FWMMain()
