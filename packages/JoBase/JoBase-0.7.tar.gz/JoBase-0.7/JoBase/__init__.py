"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

# Welcome to JoBase.
# This is a Python educational resource.

import arcade, os

from .setup import SCREEN
from .setup import MOUSE
from .setup import KEY

from .draw import Point
from .draw import Line
from .draw import Strip
from .draw import Shape
from .draw import Circle
from .draw import Rectangle
from .draw import Image
from .draw import Text

from .math import Distance
from .math import Angle
from .math import Direction
from .math import Random
from .math import Random_Angle

from .data import Sound
from .data import Read
from .data import Write

for name in dir(arcade.color):
    if not name.startswith('__'):
        globals()[name] = getattr(arcade.color, str(name))

for name in dir(SCREEN):
    if name.startswith('CURSOR_'):
        globals()[name[7:]] = getattr(SCREEN, name)
        
def Random_Screen_X():
    return Random(0, SCREEN.width)
    
def Random_Screen_Y():
    return Random(0, SCREEN.height)
    
def Random_Screen_Pos():
    return Random(0, SCREEN.width), Random(0, SCREEN.height)

def run():
    arcade.run()