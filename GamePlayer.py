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
                    self.spritesheet.subsurface(self.PLAYER_WIDTH * sprite_id, 0, self.PLAYER_WIDTH,
                                                self.PLAYER_HEIGHT))

        # Default sprite is the droplet one
        self.current_shape = self.PLAYER_DROPLET
        self.image = self.sprites[self.current_shape]

        # Define the default rect
        self.rect = pygame.Rect(0, 0, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

        # Set the group as a single sprite one
        self.group = pygame.sprite.GroupSingle(self)

    def display(self, screen):
        """
        Display the sprite on the given surface
        :param screen: The surface where the sprite will be blitted
        """
        self.group.draw(screen)

    def move_up(self):
        if self.current_shape == Player.PLAYER_CLOUD:
            self.rect.top -= 1 * 64

    def move_down(self):
        if self.current_shape == Player.PLAYER_CLOUD:
            self.rect.top += 1 * 64

    def move_left(self):
        self.rect.left -= 1 * 64

    def move_right(self):
        self.rect.left += 1 * 64

    def shapeshift(self, shape_id):
        """
        Change the shape of our player
        :param shape_id: Player.PLAYER_CLOUD, Player.PLAYER_DROPLET, Player.PLAYER_ICE
        :return:
        """
        possibilities = {self.PLAYER_CLOUD, self.PLAYER_DROPLET, self.PLAYER_ICE} - {self.current_shape}
        if shape_id in possibilities:
            self.current_shape = shape_id
            self.image = self.sprites[shape_id]
