import pygame


class Grid(pygame.Surface):
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
