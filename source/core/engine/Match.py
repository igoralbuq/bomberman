import pygame
import sys
from pygame.locals import *

from source.core.game_objects.Character.Character import Character
from source.core.ui.Map import Map
from source.core.utils import Constants


class Match:

    def __init__(self):
        self.__menu_font = pygame.font.Font("assets/font/04B_30__.TTF",
                                            Constants.FONT_SIZE)
        self.__msg = self.__menu_font.render("funcao nao disponivel", True,
                                             Constants.RED)

        self.__map = Map()
        self.__player = Character((1, 1), 'bomberboy_white')

    def play(self, clock, surface):
        self.__map.draw(surface)

        # Checking for keyboard events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_BACKSPACE:
                    return Constants.MENU
                elif event.key == K_ESCAPE:
                    return Constants.PAUSE
                else:
                    self.__player.key_up(event.key)

            if event.type == KEYDOWN:
                self.__player.key_down(event.key)

        # Updates and draws character
        if self.__player.update(clock, self.__map.get_grid().get_tilemap()):
            self.__player.draw(surface)

        return Constants.PLAYING_SINGLE
