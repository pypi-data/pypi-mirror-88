#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame


class BoolProp:
    def __init__(self, size, border_size, bg_col, check_col, border_col):
        """
        Initializes boolean property.
        :param size: Radius (pixels) of circle.
        :param border_size: Thickness (pixels) of border.
        :param bg_col: Color (RGB) of unchecked circle.
        :param check_col: Color (RGB) when checked.
        :param border_col: Color (RGB) of border.
        """
        self._size = size
        self._border_size = border_size
        self._colors = (bg_col, check_col)
        self._border_col = border_col

        self.value = True

    def draw(self, window, events, loc, text):
        """
        Draws boolean property.
        :param window: Window to draw boolean on.
        :param events: Pygame events.
        :param location: Location (x, y) of upper left corner.
        :param text: Text to accompany the boolean (pygame.Surface)
        """
        color = self._colors[1] if self.value else self.colors[0]