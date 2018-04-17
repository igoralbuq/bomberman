from pygame.locals import *
import pygame
import sys

from source.core.engine.Match import Match
from source.core.ui.Menu import Menu
from source.core.ui.Setup import Setup
from source.core.ui.SpriteHandler import SpriteHandler
from source.core.utils.Constants import *


class Engine:
    """
    Game engine class. This is the class that runs the game and contains the
    map, elements, sounds, status etc.
    """

    def __init__(self):
        """
        Set variables required for window creation.
        """
        pygame.init()

        self.fpsClock = pygame.time.Clock()

        self.__game_name = GAME_NAME
        self.__surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption(self.__game_name)

        self.__song = pygame.mixer.Sound("assets/song/song.ogg")
        self.__sprites = SpriteHandler().sprites

        self.__state = MENU
        self.__menu = None
        self.__setup = None
        self.__match = None

    def play(self):
        # self.__song.play(-1)
        while True:
            if self.__state == MENU:
                if not self.__menu:  # Verify that the pointer is null
                    self.__menu = Menu()
                    del self.__match
                    self.__match = None
                    del self.__setup
                    self.__setup = None
                self.__menu.draw(self.__surface)
                self.__state = self.__menu.update()

            elif self.__state == SETUP:
                if not self.__setup:
                    self.__setup = Setup(self.__sprites)
                    del self.__menu
                    self.__menu = None
                self.__setup.draw(self.__surface)
                self.__state = self.__setup.update()

            elif self.__state == PLAYING:
                if not self.__match:  # Verify that the pointer is null
                    self.__match = Match(self.__setup.get_characters(),
                                         self.__sprites)
                    del self.__setup
                    self.__setup = None
                self.__state = self.__match.play(self.fpsClock, self.__surface)

            elif self.__state == FINISH:
                pygame.quit()
                sys.exit()

            pygame.display.update()

            self.fpsClock.tick(MAX_FPS)
