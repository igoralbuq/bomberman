import numpy as np
from pygame import locals

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents


class Character(GameObject):
    """
    Abstract class for a BomberBoy character.
    """

    def __init__(self, initial_tile, sprite_name):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        :param sprite_name: String to select the character sprite.
        Possibilities: white_bomberboy.
        """

        super().__init__(initial_tile, sprite_name)

        self.__speed = Constants.INITIAL_SPEED
        self.__velocity = np.array([0, 0])
        self.__icon = self._sprite['down']
        self.__placed_bombs = 0
        self.__total_bombs = 1
        self.__fire = Constants.INITIAL_FIRE
        self.__event = CharacterEvents.STOP_DOWN
        self.__new_event = CharacterEvents.STOP_DOWN
        self.__got_special_event = False

        self.__setup_animations()

    def update(self, clock, tilemap=None):
        """
        Updates the character according to its intrinsic status.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array with the map information.
        :return: True if the object still exists.
        """

        # If the dying animation ended, returns False: this character must not
        # be drawed.
        if self.__die_animation.done():
            return False

        # Handles event variables
        self.__event = self.__new_event
        if self.__got_special_event:
            self.__got_special_event = False

        # Finite state machine
        if self.__new_event == CharacterEvents.MOVE_UP:
            self.__move((0, -1), clock, tilemap)
        elif self.__new_event == CharacterEvents.MOVE_DOWN:
            self.__move((0, 1), clock, tilemap)
        elif self.__new_event == CharacterEvents.MOVE_RIGHT:
            self.__move((1, 0), clock, tilemap)
        elif self.__new_event == CharacterEvents.MOVE_LEFT:
            self.__move((-1, 0), clock, tilemap)
        elif self.__new_event == CharacterEvents.INCREASE_SPEED:
            self.__speed += Constants.SPEED_INCREMENT
            if self.__speed > Constants.MAX_SPEED:
                self.__speed = Constants.MAX_SPEED

            step_frequency = Constants.STEPS_PER_SQUARE * (
                    Constants.INITIAL_SPEED + self.__speed / Constants.MAX_SPEED)
            self.__move_up_animation.set_durations(
                np.ones(2) / step_frequency)
            self.__move_down_animation.set_durations(
                np.ones(2) / step_frequency)
            self.__move_right_animation.set_durations(
                np.ones(2) / step_frequency)
            self.__move_left_animation.set_durations(
                np.ones(2) / step_frequency)

            self.__new_event = None
        elif self.__new_event == CharacterEvents.INCREASE_BOMB:
            self.__total_bombs += 1
            self.__new_event = None
        elif self.__new_event == CharacterEvents.INCREASE_FIRE:
            self.__fire += Constants.FIRE_INCREMENT
            self.__new_event = None

        return True

    def draw(self, display):
        """
        Updates the the character icon on the screen, according to its
        animations. Note: This function should be called after update(), and
        only if update() returns True.
        :param display: Pygame display object.
        """

        # Finite state machine
        if self.__event == CharacterEvents.MOVE_UP:
            self.__icon = self.__move_up_animation.update()
        elif self.__event == CharacterEvents.STOP_UP:
            self.__icon = self._sprite['up']
        elif self.__event == CharacterEvents.MOVE_DOWN:
            self.__icon = self.__move_down_animation.update()
        elif self.__event == CharacterEvents.STOP_DOWN:
            self.__icon = self._sprite['down']
        elif self.__event == CharacterEvents.MOVE_LEFT:
            self.__icon = self.__move_left_animation.update()
        elif self.__event == CharacterEvents.STOP_LEFT:
            self.__icon = self._sprite['left']
        elif self.__event == CharacterEvents.MOVE_RIGHT:
            self.__icon = self.__move_right_animation.update()
        elif self.__event == CharacterEvents.STOP_RIGHT:
            self.__icon = self._sprite['right']
        elif self.__event == CharacterEvents.WIN:
            self.__icon = self.__win_animation.update()
        elif self.__event == CharacterEvents.DIE:
            self.__icon = self.__die_animation.update()

        # Positioning the blit according to the icon size
        display.blit(self.__icon, (self._pose.x - 0.5 * Constants.SQUARE_SIZE,
                                   self._pose.y + Constants.SQUARE_SIZE / 2 -
                                   self.__icon.get_size()[1] +
                                   Constants.DISPLAY_HEIGTH))

    def key_up(self, key):
        """
        Updates the character velocity and events given that a key was released.
        :param key: pygame.locals key id.
        """

        if not (self.__new_event == CharacterEvents.WIN or
                self.__new_event == CharacterEvents.DIE):
            if key == locals.K_LEFT:
                self.__velocity += (1, 0)
                self.__new_event = CharacterEvents.STOP_LEFT
            elif key == locals.K_RIGHT:
                self.__velocity += (-1, 0)
                self.__new_event = CharacterEvents.STOP_RIGHT
            elif key == locals.K_UP:
                self.__velocity += (0, 1)
                self.__new_event = CharacterEvents.STOP_UP
            elif key == locals.K_DOWN:
                self.__velocity += (0, -1)
                self.__new_event = CharacterEvents.STOP_DOWN

            if not self.__got_special_event:
                if self.__velocity[1] == 1:
                    self.__new_event = CharacterEvents.MOVE_DOWN
                elif self.__velocity[1] == -1:
                    self.__new_event = CharacterEvents.MOVE_UP
                elif self.__velocity[0] == 1:
                    self.__new_event = CharacterEvents.MOVE_RIGHT
                elif self.__velocity[0] == -1:
                    self.__new_event = CharacterEvents.MOVE_LEFT

    def key_down(self, key):
        """
        Updates the character velocity and events given that a key was pressed.
        :param key: pygame.locals key id.
        """

        if not (self.__new_event == CharacterEvents.WIN or
                self.__new_event == CharacterEvents.DIE):
            if key == locals.K_LEFT:
                self.__velocity += (-1, 0)
            elif key == locals.K_RIGHT:
                self.__velocity += (1, 0)
            elif key == locals.K_UP:
                self.__velocity += (0, -1)
            elif key == locals.K_DOWN:
                self.__velocity += (0, 1)

            if not self.__got_special_event:
                if self.__velocity[1] == 1:
                    self.__new_event = CharacterEvents.MOVE_DOWN
                elif self.__velocity[1] == -1:
                    self.__new_event = CharacterEvents.MOVE_UP
                elif self.__velocity[0] == 1:
                    self.__new_event = CharacterEvents.MOVE_RIGHT
                elif self.__velocity[0] == -1:
                    self.__new_event = CharacterEvents.MOVE_LEFT

    def place_bomb(self):
        """
        Tries placing a bomb.
        :return: True if it was successful.
        """

        if self.__placed_bombs < self.__total_bombs:
            self.__placed_bombs += 1
            return True
        else:
            return False

    def bomb_exploded(self):
        """
        Informs the character that one of his bombs exploded, allowing him to
        place another bomb.
        """

        self.__placed_bombs -= 1

    def special_event(self, event):
        """
        Updates the character status given that a special event (win, die,
        picked powerup) occurred.
        :param event: CharacterEvent event id.
        """

        self.__new_event = event
        self.__got_special_event = True

    def __setup_animations(self):
        """
        Sets up the character animations, creating an object for each one.
        """

        # Movements
        step_frequency = self.__speed * Constants.STEPS_PER_SQUARE
        self.__move_up_animation = Animation(
            [self._sprite['move_up1'], self._sprite['move_up2']],
            np.ones(2) / step_frequency)
        self.__move_down_animation = Animation(
            [self._sprite['move_down1'], self._sprite['move_down2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))
        self.__move_right_animation = Animation(
            [self._sprite['move_right1'], self._sprite['move_right2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))
        self.__move_left_animation = Animation(
            [self._sprite['move_left1'], self._sprite['move_left2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))

        # Winning
        self.__win_animation = Animation([
            self._sprite['win1'], self._sprite['win2'],
            self._sprite['win3']], np.array([0.25, 0.25, 0.5]))

        # Dying: The character spins 5 times than falls on the ground.
        die_sprites = np.concatenate([np.tile(
            [self._sprite['die_down'], self._sprite['die_right'],
             self._sprite['die_up'], self._sprite['die_left']], 5),
            [self._sprite['die_down'],
             self._sprite['die1'], self._sprite['die1'],
             self._sprite['die3'], self._sprite['die4'],
             self._sprite['die5'], self._sprite['die6']]])
        die_durations = np.concatenate([np.tile(0.1, 20),
                                        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]])
        self.__die_animation = Animation(die_sprites, die_durations, stop=True)

    def __move(self, direction, clock, tilemap):
        """
        Moves the character according to obstacles.
        :param direction: Tuple with x and y directions.
        :param tilemap: Numpy array with the map information.
        """

        # Auxiliar variables
        sq = Constants.SQUARE_SIZE
        obstacles = np.array([Constants.UNIT_BLOCK, Constants.UNIT_FIXED_BLOCK,
                              Constants.UNIT_BOMB,
                              Constants.UNIT_POWERUP_FIRE_HIDE,
                              Constants.UNIT_POWERUP_VELOCITY_HIDE,
                              Constants.UNIT_POWERUP_BOMB_HIDE])

        x = self._pose.x
        x_tile = int(x / sq)

        # Choosing most natural movement upwards according to blocked blocks
        y = self._pose.y + sq / 2
        y_tile = int(y / sq)
        if self.__event == CharacterEvents.MOVE_UP:
            if not np.any(obstacles == tilemap[y_tile - 1, x_tile]):
                if sq * 0.45 < x % sq < sq * 0.55:
                    self._pose.x = (x_tile + 0.5) * sq
                elif x % sq <= sq * 0.45:
                    direction = (1, 0)
                    self.__event = CharacterEvents.MOVE_RIGHT
                else:
                    direction = (-1, 0)
                    self.__event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile - 1]) and
                  0 < x % sq < sq / 4):
                direction = (-1, 0)
                self.__event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile + 1]) and
                  3 * sq / 4 < x % sq < sq):
                direction = (1, 0)
                self.__event = CharacterEvents.MOVE_RIGHT
            else:
                direction = (0, 0)
                self.__event = CharacterEvents.STOP_UP

        # Choosing most natural movement downwards according to blocked blocks
        y = self._pose.y - sq / 2 - 1
        y_tile = int(y / sq)
        if self.__event == CharacterEvents.MOVE_DOWN:
            if not np.any(obstacles == tilemap[y_tile + 1, x_tile]):
                if sq * 0.45 < x % sq < sq * 0.55:
                    self._pose.x = (x_tile + 0.5) * sq
                elif x % sq <= sq * 0.45:
                    direction = (1, 0)
                    self.__event = CharacterEvents.MOVE_RIGHT
                else:
                    direction = (-1, 0)
                    self.__event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile - 1]) and
                  0 <= x % sq < sq / 4):
                direction = (-1, 0)
                self.__event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile + 1]) and
                  3 * sq / 4 < x % sq < sq):
                direction = (1, 0)
                self.__event = CharacterEvents.MOVE_RIGHT
            else:
                direction = (0, 0)
                self.__event = CharacterEvents.STOP_DOWN

        y = self._pose.y
        y_tile = int(y / sq)

        # Choosing most natural movement rightwards according to blocked blocks
        x = self._pose.x - sq / 2 - 1
        x_tile = int(x / sq)
        if self.__event == CharacterEvents.MOVE_RIGHT:
            if not np.any(obstacles == tilemap[y_tile, x_tile + 1]):
                if sq * 0.45 < y % sq < sq * 0.55:
                    self._pose.y = (y_tile + 0.5) * sq
                elif y % sq <= sq * 0.45:
                    direction = (0, 1)
                    self.__event = CharacterEvents.MOVE_DOWN
                else:
                    direction = (0, -1)
                    self.__event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile + 1]) and
                  0 <= y % sq < sq / 4):
                direction = (0, -1)
                self.__event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile + 1]) and
                  3 * sq / 4 < y % sq < sq):
                direction = (0, 1)
                self.__event = CharacterEvents.MOVE_DOWN
            else:
                direction = (0, 0)
                self.__event = CharacterEvents.STOP_RIGHT

        # Choosing most natural movement leftwards according to blocked blocks
        x = self._pose.x + sq / 2
        x_tile = int(x / sq)
        if self.__event == CharacterEvents.MOVE_LEFT:
            if not np.any(obstacles == tilemap[y_tile, x_tile - 1]):
                if sq * 0.45 < y % sq < sq * 0.55:
                    self._pose.y = (y_tile + 0.5) * sq
                elif y % sq <= sq * 0.45:
                    direction = (0, 1)
                    self.__event = CharacterEvents.MOVE_DOWN
                else:
                    direction = (0, -1)
                    self.__event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile - 1]) and
                  0 <= y % sq < sq / 4):
                direction = (0, -1)
                self.__event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile - 1]) and
                  3 * sq / 4 < y % sq < sq):
                direction = (0, 1)
                self.__event = CharacterEvents.MOVE_DOWN
            else:
                direction = (0, 0)
                self.__event = CharacterEvents.STOP_LEFT

        # Walking towards best direction
        self._pose.x += (direction[0] * self.__speed *
                         Constants.SQUARE_SIZE / clock.get_fps())
        self._pose.y += (direction[1] * self.__speed *
                         Constants.SQUARE_SIZE / clock.get_fps())
