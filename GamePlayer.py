import os

import pygame

from pygame import image


class Player(pygame.sprite.Sprite):
    PLAYER_CLOUD = 0
    PLAYER_DROPLET = 1
    PLAYER_ICE = 2

    PLAYER_WIDTH = 64
    PLAYER_HEIGHT = 64

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Retrieve the image file to load it as spritesheet
        path = os.path.dirname(__file__) + os.sep + "assets/playersheet.png"
        self.spritesheet = pygame.image.load(path)

        # Define the player sprites from the spritesheet (64x64)
        self.sprites = []
        for sprite_id in range(3):
            self.sprites.append(
                self.spritesheet.subsurface(self.PLAYER_WIDTH * sprite_id, 0, self.PLAYER_WIDTH, self.PLAYER_HEIGHT))

        # Default sprite is the droplet one
        self.image = self.sprites[self.PLAYER_DROPLET]

        # Define the default rect
        self.rect = (0, 0, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

        # Set the group as a single sprite one
        self.group = pygame.sprite.GroupSingle(self)

    def display(self, screen):
        """
        Display the sprite on the given surface
        :param screen: The surface where the sprite will be blitted
        """
        self.group.draw(screen)
