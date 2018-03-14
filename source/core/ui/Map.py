import sys
import pygame
from pygame.locals import *

from source.core.utils.Constants import *
from source.core.map.Grid import Grid


class Map:

    def __init__(self):
        self.__brick = pygame.image.load("../../../assets/image/brick.png")
        self.__block = pygame.image.load("../../../assets/image/block.png")

        self.__grid = Grid()
        self.__dim = self.__grid.get_dimension()

        self.__block = pygame.transform.scale(self.__block, (SQUARE_SIZE,
                                                         SQUARE_SIZE))
        self.__brick = pygame.transform.scale(self.__brick, (SQUARE_SIZE,
                                                         SQUARE_SIZE))

    def draw(self, surface):
        surface.fill(GREEN)

        pos = (0, DISPLAY_HEIGTH)

        for x in range(self.__dim[0]):
            for y in range(self.__dim[1]):
                if self.__grid.__getattr__(position=(x, y)) == UNIT_FIXED_BLOCK:
                    surface.blit(self.__block, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_BLOCK:
                    surface.blit(self.__brick, pos)

                pos = (pos[0]+SQUARE_SIZE, pos[1])

            pos = (0, pos[1]+SQUARE_SIZE)

    def update(self):
        pass