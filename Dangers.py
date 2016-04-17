import os
import pygame

class Water(pygame.Surface):
    def __init__(self, surface, coord_x, coord_y):
        """
        Initialize the tile properties
        :param surface: the surface retrieved from Tiled file (.tmx)
        :param coord_x: the x coordinate
        :param coord_y: the y coordinate
        """
        pygame.Surface.__init__(self, surface.get_size())

        self.surface = surface
        self.rect = surface.get_rect()
        self.rect.x = coord_x * 64
        self.rect.y = coord_y * 64

    def display(self, screen):
        """
        Display the tile on the given surface
        :param screen: The surface where the tile will be blitted
        """
        screen.blit(self.surface, self.rect)


class Fire(pygame.sprite.Sprite):
    SPRITE_WITH = 64
    SPRITE_HEIGHT = 64

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Retrieve the image file to load it as spritesheet
        path = os.path.dirname(__file__) + os.sep + "assets/spritesheet_fire.png"
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
        self.rect = pygame.Rect(x * self.SPRITE_WITH, y * self.SPRITE_HEIGHT, self.SPRITE_WITH, self.SPRITE_HEIGHT)

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
