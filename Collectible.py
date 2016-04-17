import os
import pygame


class Collectible(pygame.sprite.Sprite):
    SPRITE_WITH = 36
    SPRITE_HEIGHT = 32

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Retrieve the image file to load it as spritesheet
        path = os.path.dirname(__file__) + os.sep + "assets/spritesheet_point.png"
        self.spritesheet = pygame.image.load(path)

        # Define the player sprites from the spritesheet (64x64)
        self.sprites = []
        for sprite_id in range(4):
            self.sprites.append(
                    self.spritesheet.subsurface(self.SPRITE_WITH * sprite_id, 0, self.SPRITE_WITH,
                                                self.SPRITE_HEIGHT))

        # Default sprite is the droplet one
        self.current_shape = 0
        self.image = self.sprites[self.current_shape]

        # Define the default rect
        self.rect = pygame.Rect(x * 64, y * 64, self.SPRITE_WITH, self.SPRITE_HEIGHT)

        # Set the group as a single sprite one
        self.group = pygame.sprite.GroupSingle(self)

    def display(self, screen):
        """
        Display the sprite on the given surface
        :param screen: The surface where the sprite will be blitted
        """
        if self.current_shape == 3:
            self.current_shape = 0
        else:
            self.current_shape += 1
        self.image = self.sprites[self.current_shape]
        self.group.draw(screen)
