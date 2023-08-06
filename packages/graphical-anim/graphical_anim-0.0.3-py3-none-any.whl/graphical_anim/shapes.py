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
from .props import FloatProp


class Rect:
    def __init__(self, loc: tuple, size: tuple, color: tuple, border=0) -> None:
        """
        Initializes rectangle.
        :param loc: Location (x, y) of rectangle.
        :param size: Size (x, y) of rectangle.
        :param color: (r, g, b, a) color of rectangle.
        :param border: Border of rectangle
        """
        self._loc_x = FloatProp(value=loc[0])
        self._loc_y = FloatProp(value=loc[1])
        self._size_x = FloatProp(value=size[0])
        self._size_y = FloatProp(value=size[1])
        self._color_r = FloatProp(value=color[0], min=0, max=255)
        self._color_g = FloatProp(value=color[1], min=0, max=255)
        self._color_b = FloatProp(value=color[2], min=0, max=255)
        self._color_a = FloatProp(value=color[3], min=0, max=255)
        self._border = FloatProp(value=border, min=0)

    def keyframe(self, frame: int, datapath: str, value):
        datapath = "_" + datapath
        attr = getattr(self, datapath)
        attr.keyframe(frame, value)

    def _render(self, frame, resolution):
        loc = (self._loc_x.interpolate(frame), self._loc_y.interpolate(frame))
        size = (self._size_x.interpolate(frame), self._size_y.interpolate(frame))
        color = (
            self._color_r.interpolate(frame),
            self._color_g.interpolate(frame),
            self._color_b.interpolate(frame),
            self._color_a.interpolate(frame),
        )
        border = self._border.interpolate(frame)

        surface = pygame.Surface(resolution, pygame.SRCALPHA)
        pygame.draw.rect(surface, color, loc+size, border)
        return surface


class Circle:
    def __init__(self, loc: tuple, radius: float, color: tuple, border=0) -> None:
        """
        Initializes circle.
        :param loc: Location (x, y) of circle.
        :param radius: Radius of circle.
        :param color: (r, g, b, a) color of circle.
        :param border: Border of circle
        """
        self._loc_x = FloatProp(value=loc[0])
        self._loc_y = FloatProp(value=loc[1])
        self._radius = FloatProp(value=radius)
        self._color_r = FloatProp(value=color[0], min=0, max=255)
        self._color_g = FloatProp(value=color[1], min=0, max=255)
        self._color_b = FloatProp(value=color[2], min=0, max=255)
        self._color_a = FloatProp(value=color[3], min=0, max=255)
        self._border = FloatProp(value=border, min=0)

    def keyframe(self, frame: int, datapath: str, value):
        datapath = "_" + datapath
        attr = getattr(self, datapath)
        attr.keyframe(frame, value)

    def _render(self, frame, resolution):
        loc = (self._loc_x.interpolate(frame), self._loc_y.interpolate(frame))
        radius = self._radius.interpolate(frame)
        color = (
            self._color_r.interpolate(frame),
            self._color_g.interpolate(frame),
            self._color_b.interpolate(frame),
            self._color_a.interpolate(frame),
        )
        border = self._border.interpolate(frame)

        surface = pygame.Surface(resolution, pygame.SRCALPHA)
        pygame.draw.circle(surface, color, loc, radius, border)
        return surface


class Polygon:
    def __init__(self, verts: tuple, color: tuple, border=0) -> None:
        """
        Initializes polygon.
        :param verts: Verticies ((x1, y1), (x2, y2), ...) of polygon.
        :param color: (r, g, b, a) color of polygon.
        :param border: Border of polygon
        """
        self._verts = verts
        self._loc_x = FloatProp(value=0)
        self._loc_y = FloatProp(value=0)
        self._color_r = FloatProp(value=color[0], min=0, max=255)
        self._color_g = FloatProp(value=color[1], min=0, max=255)
        self._color_b = FloatProp(value=color[2], min=0, max=255)
        self._color_a = FloatProp(value=color[3], min=0, max=255)
        self._border = FloatProp(value=border, min=0)

    def keyframe(self, frame: int, datapath: str, value):
        datapath = "_" + datapath
        attr = getattr(self, datapath)
        attr.keyframe(frame, value)

    def _render(self, frame, resolution):
        color = (
            self._color_r.interpolate(frame),
            self._color_g.interpolate(frame),
            self._color_b.interpolate(frame),
            self._color_a.interpolate(frame),
        )
        border = self._border.interpolate(frame)
        x_offset = self._loc_x.interpolate(frame)
        y_offset = self._loc_y.interpolate(frame)

        surface = pygame.Surface(resolution, pygame.SRCALPHA)
        pygame.draw.polygon(surface, color, [(x + x_offset, y + y_offset) for x, y in self._verts], border)
        return surface