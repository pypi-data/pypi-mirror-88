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


class BoolProp:
    supported_types = (bool,)

    def __init__(self, value=False):
        self._value = value
        self._keyframes = []

    def keyframe(self, frame, value):
        for i, key in enumerate(self._keyframes):
            if key["frame"] == frame:
                del self._keyframes[i]
        
        if isinstance(value, self.supported_types):
            self._keyframes.append({"frame": frame, "value": value})

    def interpolate(self, frame):
        if len(self._keyframes) == 0:
            return self._value
        
        min_index = None
        for i, key in enumerate(self._keyframes):
            if key["frame"] <= frame or min_index is None:
                min_index = i
        return self._keyframes[min_index]["value"]

    def get_value(self):
        return self._value

    def set_value(self, value):
        if isinstance(value, self.supported_types):
            self._value = value


class FloatProp:
    supported_types = (int, float)

    def __init__(self, value=0, min=None, max=None):
        self._value = value
        self._keyframes = []
        self.min = float("-inf") if min is None else min
        self.max = float("inf") if max is None else max

    def keyframe(self, frame, value):
        for i, key in enumerate(self._keyframes):
            if key["frame"] == frame:
                del self._keyframes[i]
        
        if isinstance(value, self.supported_types):
            self._keyframes.append({"frame": frame, "value": min(max(value, self.min), self.max)})

    def interpolate(self, frame):
        if len(self._keyframes) == 0:
            return self._value

        keys = self._keyframes
        min_index = max_index = None
        for i, key in enumerate(keys):
            if min_index is None and key["frame"] <= frame:
                min_index = i
            elif min_index is not None and key["frame"] <= frame and key["frame"] > keys[min_index]["frame"]:
                min_index = i

            if max_index is None and key["frame"] > frame:
                max_index = i
            elif max_index is not None and key["frame"] > frame and key["frame"] < keys[max_index]["frame"]:
                max_index = i

        if max_index is None:
            return keys[min_index]["value"]
        elif min_index is None:
            return keys[max_index]["value"]
        else:
            min_frame = keys[min_index]["frame"]
            max_frame = keys[max_index]["frame"]
            min_value = keys[min_index]["value"]
            max_value = keys[max_index]["value"]

            fac = (frame-min_frame) / (max_frame-min_frame)
            return (max_value-min_value) * fac + min_value

    def get_value(self):
        return self._value

    def set_value(self, value):
        if isinstance(value, self.supported_types):
            self._value = value