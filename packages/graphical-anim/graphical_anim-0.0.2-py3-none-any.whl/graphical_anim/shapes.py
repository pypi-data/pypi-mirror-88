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
import numpy
from PIL import Image
from .props import BoolProp, FloatProp
from .utils import surf_to_image


class Rect:
    _loc_x = FloatProp(value=0)
    _loc_y = FloatProp(value=0)
    _size_x = FloatProp(value=100)
    _size_y = FloatProp(value=100)

    def __init__(self, loc: tuple, size: tuple, color: tuple) -> None:
        """
        Initializes rectangle.
        :param loc: Location (x, y) of rectangle.
        :param size: Size (x, y) of rectangle.
        :param color: (r, g, b) color of rectangle.
        """
        self._loc_x.set_value(loc[0])
        self._loc_y.set_value(loc[1])
        self._size_x.set_value(size[0])
        self._size_y.set_value(size[1])

    def keyframe(self, frame: int, datapath: str, value):
        datapath = "_" + datapath
        attr = getattr(self, datapath)
        attr.keyframe(frame, value)

    def _render(self, frame, resolution):
        loc = (self._loc_x.interpolate(frame), self._loc_y.interpolate(frame))
        size = (self._size_x.interpolate(frame), self._size_y.interpolate(frame))

        surface = pygame.Surface(resolution)
        pygame.draw.rect(surface, (255, 255, 255), loc+size)
        return surface