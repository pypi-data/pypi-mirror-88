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

import os
import sys
import time
import shutil
import pygame
import cv2
from hashlib import sha256
from .utils import surf_to_image


class Video:
    def __init__(self, resolution: tuple, fps: int) -> None:
        """
        Initializes video.
        :param resolution: Pixel resolution (x, y) of final video.
        :param fps: Frames per second of video.
        """
        self._resolution = resolution
        self._fps = fps
        self._layers = []

    def export(self, path: str, frames: int) -> None:
        """
        Exports layers to a video.
        :param path: Path to export video (only .mp4).
        :param frames: Total amount of frames to export.
        """
        time_start = time.time()
        parent = os.path.realpath(os.path.dirname(__file__))
        hash = sha256(str(time.time()).encode()).hexdigest()
        while os.path.isdir(os.path.join(parent, hash)):
            hash = sha256(str(time.time()).encode()).hexdigest()

        sys.stdout.write("--------------------------------------\n")
        sys.stdout.write("Exporting video:\n")
        sys.stdout.write(f"  Hash: {hash}\n")
        sys.stdout.write(f"  Resolution: {self._resolution}\n")
        sys.stdout.write(f"  FPS: {self._fps}\n\n")
        sys.stdout.flush()

        tmp_dir = os.path.join(parent, hash)
        os.makedirs(tmp_dir, exist_ok=True)
        
        sys.stdout.write(f"Exporting {frames} frames: ")
        sys.stdout.flush()
        for frame in range(frames):
            msg = f"{frame} of {frames}, {round(time.time()-time_start, 2)} seconds elapsed."
            sys.stdout.write(msg)
            sys.stdout.flush()

            surface = pygame.Surface(self._resolution)
            for layer in self._layers:
                surface.blit(layer._render(frame, self._resolution), (0, 0))
            image = surf_to_image(surface)
            image.save(os.path.join(tmp_dir, f"{frame}.png"))

            sys.stdout.write("\b" * len(msg))
            sys.stdout.write(" " * len(msg))
            sys.stdout.write("\b" * len(msg))

        sys.stdout.write(f"Finished in {round(time.time()-time_start, 3)} seconds.\n")
        sys.stdout.write("Compiling video...\n")
        sys.stdout.flush()

        images = sorted([img for img in os.listdir(tmp_dir)], key=(lambda x: int(x.split(".")[0])))
        frame = cv2.imread(os.path.join(tmp_dir, images[0]))
        height, width, layers = frame.shape
        video = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"MPEG"), self._fps, (width, height))
        for img in images:
            video.write(cv2.imread(os.path.join(tmp_dir, img)))

        video.release()
        cv2.destroyAllWindows()
        shutil.rmtree(tmp_dir)
        sys.stdout.write(f"Finished exporting video in {round(time.time()-time_start, 3)} seconds.\n")
        sys.stdout.write("--------------------------------------\n")
        sys.stdout.flush()

    def add_layer(self, layer) -> None:
        """
        Adds a layer.
        :param layer: graphical_anim layer.
        """
        self._layers.append(layer)