# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

from roboid import *


class Grid(object):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class GridHamster(Hamster):
    def __init__(self, index=0, port_name=None, initial_x=0, initial_y=0, initial_direction=Grid.RIGHT):
        super(GridHamster, self).__init__(index, port_name)
        self._initial_x = initial_x
        self._initial_y = initial_y
        self._initial_direction = initial_direction
        self.reset()

    def reset(self):
        self._old_x = self._x = self._initial_x
        self._old_y = self._y = self._initial_y
        self._old_direction = self._direction = self._initial_direction
        super(GridHamster, self).reset()

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def get_old_x(self):
        return self._old_x

    def set_old_x(self, x):
        self._old_x = x

    def get_old_y(self):
        return self._old_y

    def set_old_y(self, y):
        self._old_y = y

    def get_old_direction(self):
        return self._old_direction

    def set_old_direction(self, direction):
        self._old_direction = direction

    def turn_to_left(self):
        self._old_direction = self._direction
        if self._direction == Grid.RIGHT:
            self.board_left()
            self.board_left()
        elif self._direction == Grid.UP:
            self.board_left()
        elif self._direction == Grid.DOWN:
            self.board_right()
        self._direction = Grid.LEFT

    def turn_to_right(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.board_left()
            self.board_left()
        elif self._direction == Grid.UP:
            self.board_right()
        elif self._direction == Grid.DOWN:
            self.board_left()
        self._direction = Grid.RIGHT

    def turn_to_up(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.board_right()
        elif self._direction == Grid.RIGHT:
            self.board_left()
        elif self._direction == Grid.DOWN:
            self.board_left()
            self.board_left()
        self._direction = Grid.UP

    def turn_to_down(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.board_left()
        elif self._direction == Grid.RIGHT:
            self.board_right()
        elif self._direction == Grid.UP:
            self.board_left()
            self.board_left()
        self._direction = Grid.DOWN

    def move_to_left(self):
        self._old_x = self._x
        self.turn_to_left()
        self.board_forward()
        self._x -= 1

    def move_to_right(self):
        self._old_x = self._x
        self.turn_to_right()
        self.board_forward()
        self._x += 1

    def move_to_up(self):
        self._old_y = self._y
        self.turn_to_up()
        self.board_forward()
        self._y += 1

    def move_to_down(self):
        self._old_y = self._y
        self.turn_to_down()
        self.board_forward()
        self._y -= 1

    def move(self, action):
        if action == Grid.LEFT:
            self.move_to_left()
        elif action == Grid.RIGHT:
            self.move_to_right()
        elif action == Grid.UP:
            self.move_to_up()
        else:
            self.move_to_down()


class GridHamsterS(HamsterS):
    def __init__(self, index=0, port_name=None, initial_x=0, initial_y=0, initial_direction=Grid.RIGHT, cross=True):
        super(GridHamsterS, self).__init__(index, port_name)
        self._initial_x = initial_x
        self._initial_y = initial_y
        self._initial_direction = initial_direction
        self._cross_board = cross
        self.reset()

    def reset(self):
        self._old_x = self._x = self._initial_x
        self._old_y = self._y = self._initial_y
        self._old_direction = self._direction = self._initial_direction
        super(GridHamsterS, self).reset()

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def get_old_x(self):
        return self._old_x

    def set_old_x(self, x):
        self._old_x = x

    def get_old_y(self):
        return self._old_y

    def set_old_y(self, y):
        self._old_y = y

    def get_old_direction(self):
        return self._old_direction

    def set_old_direction(self, direction):
        self._old_direction = direction

    def turn_to_left(self):
        self._old_direction = self._direction
        if self._cross_board:
            if self._direction == Grid.RIGHT:
                self.board_left()
                self.board_left()
            elif self._direction == Grid.UP:
                self.board_left()
            elif self._direction == Grid.DOWN:
                self.board_right()
        else:
            if self._direction == Grid.RIGHT:
                self.turn_left()
                self.turn_left()
            elif self._direction == Grid.UP:
                self.turn_left()
            elif self._direction == Grid.DOWN:
                self.turn_right()
        self._direction = Grid.LEFT

    def turn_to_right(self):
        self._old_direction = self._direction
        if self._cross_board:
            if self._direction == Grid.LEFT:
                self.board_left()
                self.board_left()
            elif self._direction == Grid.UP:
                self.board_right()
            elif self._direction == Grid.DOWN:
                self.board_left()
        else:
            if self._direction == Grid.LEFT:
                self.turn_left()
                self.turn_left()
            elif self._direction == Grid.UP:
                self.turn_right()
            elif self._direction == Grid.DOWN:
                self.turn_left()
        self._direction = Grid.RIGHT

    def turn_to_up(self):
        self._old_direction = self._direction
        if self._cross_board:
            if self._direction == Grid.LEFT:
                self.board_right()
            elif self._direction == Grid.RIGHT:
                self.board_left()
            elif self._direction == Grid.DOWN:
                self.board_left()
                self.board_left()
        else:
            if self._direction == Grid.LEFT:
                self.turn_right()
            elif self._direction == Grid.RIGHT:
                self.turn_left()
            elif self._direction == Grid.DOWN:
                self.turn_left()
                self.turn_left()
        self._direction = Grid.UP

    def turn_to_down(self):
        self._old_direction = self._direction
        if self._cross_board:
            if self._direction == Grid.LEFT:
                self.board_left()
            elif self._direction == Grid.RIGHT:
                self.board_right()
            elif self._direction == Grid.UP:
                self.board_left()
                self.board_left()
        else:
            if self._direction == Grid.LEFT:
                self.turn_left()
            elif self._direction == Grid.RIGHT:
                self.turn_right()
            elif self._direction == Grid.UP:
                self.turn_left()
                self.turn_left()
        self._direction = Grid.DOWN

    def move_to_left(self):
        self._old_x = self._x
        self.turn_to_left()
        if self._cross_board:
            self.board_forward()
        else:
            self.move_forward()
        self._x -= 1

    def move_to_right(self):
        self._old_x = self._x
        self.turn_to_right()
        if self._cross_board:
            self.board_forward()
        else:
            self.move_forward()
        self._x += 1

    def move_to_up(self):
        self._old_y = self._y
        self.turn_to_up()
        if self._cross_board:
            self.board_forward()
        else:
            self.move_forward()
        self._y += 1

    def move_to_down(self):
        self._old_y = self._y
        self.turn_to_down()
        if self._cross_board:
            self.board_forward()
        else:
            self.move_forward()
        self._y -= 1

    def move(self, action):
        if action == Grid.LEFT:
            self.move_to_left()
        elif action == Grid.RIGHT:
            self.move_to_right()
        elif action == Grid.UP:
            self.move_to_up()
        else:
            self.move_to_down()


class GridTurtle(Turtle):
    def __init__(self, index=0, port_name=None, initial_x=0, initial_y=0, initial_direction=Grid.RIGHT):
        super(GridTurtle, self).__init__(index, port_name)
        self._initial_x = initial_x
        self._initial_y = initial_y
        self._initial_direction = initial_direction
        self.reset()

    def reset(self):
        self._old_x = self._x = self._initial_x
        self._old_y = self._y = self._initial_y
        self._old_direction = self._direction = self._initial_direction
        super(GridTurtle, self).reset()

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def get_old_x(self):
        return self._old_x

    def set_old_x(self, x):
        self._old_x = x

    def get_old_y(self):
        return self._old_y

    def set_old_y(self, y):
        self._old_y = y

    def get_old_direction(self):
        return self._old_direction

    def set_old_direction(self, direction):
        self._old_direction = direction

    def turn_to_left(self):
        self._old_direction = self._direction
        if self._direction == Grid.RIGHT:
            self.turn_left()
            self.turn_left()
        elif self._direction == Grid.UP:
            self.turn_left()
        elif self._direction == Grid.DOWN:
            self.turn_right()
        self._direction = Grid.LEFT

    def turn_to_right(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.turn_left()
            self.turn_left()
        elif self._direction == Grid.UP:
            self.turn_right()
        elif self._direction == Grid.DOWN:
            self.turn_left()
        self._direction = Grid.RIGHT

    def turn_to_up(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.turn_right()
        elif self._direction == Grid.RIGHT:
            self.turn_left()
        elif self._direction == Grid.DOWN:
            self.turn_left()
            self.turn_left()
        self._direction = Grid.UP

    def turn_to_down(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.turn_left()
        elif self._direction == Grid.RIGHT:
            self.turn_right()
        elif self._direction == Grid.UP:
            self.turn_left()
            self.turn_left()
        self._direction = Grid.DOWN

    def move_to_left(self):
        self._old_x = self._x
        self.turn_to_left()
        self.move_forward()
        self._x -= 1

    def move_to_right(self):
        self._old_x = self._x
        self.turn_to_right()
        self.move_forward()
        self._x += 1

    def move_to_up(self):
        self._old_y = self._y
        self.turn_to_up()
        self.move_forward()
        self._y += 1

    def move_to_down(self):
        self._old_y = self._y
        self.turn_to_down()
        self.move_forward()
        self._y -= 1

    def move(self, action):
        if action == Grid.LEFT:
            self.move_to_left()
        elif action == Grid.RIGHT:
            self.move_to_right()
        elif action == Grid.UP:
            self.move_to_up()
        else:
            self.move_to_down()


class GridAlbertAi(AlbertAi):
    def __init__(self, index=0, port_name=None, initial_x=0, initial_y=0, initial_direction=Grid.RIGHT):
        super(GridAlbertAi, self).__init__(index, port_name)
        self._initial_x = initial_x
        self._initial_y = initial_y
        self._initial_direction = initial_direction
        self.reset()

    def reset(self):
        self._old_x = self._x = self._initial_x
        self._old_y = self._y = self._initial_y
        self._old_direction = self._direction = self._initial_direction
        super(GridAlbertAi, self).reset()

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def get_old_x(self):
        return self._old_x

    def set_old_x(self, x):
        self._old_x = x

    def get_old_y(self):
        return self._old_y

    def set_old_y(self, y):
        self._old_y = y

    def get_old_direction(self):
        return self._old_direction

    def set_old_direction(self, direction):
        self._old_direction = direction

    def turn_to_left(self):
        self._old_direction = self._direction
        if self._direction == Grid.RIGHT:
            self.turn_left()
            self.turn_left()
        elif self._direction == Grid.UP:
            self.turn_left()
        elif self._direction == Grid.DOWN:
            self.turn_right()
        self._direction = Grid.LEFT

    def turn_to_right(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.turn_left()
            self.turn_left()
        elif self._direction == Grid.UP:
            self.turn_right()
        elif self._direction == Grid.DOWN:
            self.turn_left()
        self._direction = Grid.RIGHT

    def turn_to_up(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.turn_right()
        elif self._direction == Grid.RIGHT:
            self.turn_left()
        elif self._direction == Grid.DOWN:
            self.turn_left()
            self.turn_left()
        self._direction = Grid.UP

    def turn_to_down(self):
        self._old_direction = self._direction
        if self._direction == Grid.LEFT:
            self.turn_left()
        elif self._direction == Grid.RIGHT:
            self.turn_right()
        elif self._direction == Grid.UP:
            self.turn_left()
            self.turn_left()
        self._direction = Grid.DOWN

    def move_to_left(self):
        self._old_x = self._x
        self.turn_to_left()
        self.move_forward()
        self._x -= 1

    def move_to_right(self):
        self._old_x = self._x
        self.turn_to_right()
        self.move_forward()
        self._x += 1

    def move_to_up(self):
        self._old_y = self._y
        self.turn_to_up()
        self.move_forward()
        self._y += 1

    def move_to_down(self):
        self._old_y = self._y
        self.turn_to_down()
        self.move_forward()
        self._y -= 1

    def move(self, action):
        if action == Grid.LEFT:
            self.move_to_left()
        elif action == Grid.RIGHT:
            self.move_to_right()
        elif action == Grid.UP:
            self.move_to_up()
        else:
            self.move_to_down()
