import arcade, sys

from arcade import Color

from .collision import collide

from .math import Angle
from .math import Distance
from .math import Direction

module = sys.modules['__main__']

class Screen(arcade.Window):
    
    def __init__(screen):
        super().__init__(800, 600, 'JoBase', resizable = True,
                         antialiasing = False)
                
        # The code above gets all the colors stored in 'arcade.color' and makes
        # global variables with the same name.        
        
        screen.module = module
        screen.resize = 0
        screen.time = 0
        screen.quit = 0
        screen._color = (255, 255, 255)
        screen._rate = 60
        screen._fullscreen = 0
        screen._visible = 1
        
        arcade.set_background_color((255, 255, 255))
        screen.set_update_rate(1 / 60)
                
        # The code above finds all the variables starting with 'CURSOR_' and
        # makes new global variables without the 'CURSOR_' prefix.
                
    def collide(screen, other):
        # This function checks if 'other' is on the screen.
        return collide(screen.boundary(), other.boundary())
        
    def boundary(screen):
        # This dictionary is eventually passed into the collision function.
        return {'left': 0,
                'top': screen.height,
                'right': screen.width,
                'bottom': 0,
                'type': 'rect'}
    
    def getvisible(screen):
        return screen._visible
    
    def setvisible(screen, value: bool):
        # 'set_visible' is an arcade function.
        screen.set_visible(value)
        screen._visible = value
        
    visible = property(getvisible, setvisible)
    
    def getx(screen):
        # 'get_location' is an arcade function.
        return screen.get_location()[0]
    
    def setx(screen, value: float):
        # 'set_location' is an arcade function.
        screen.set_location(value, screen.y)
        
    x = property(getx, setx)
        
    def gety(screen):
        return screen.get_location()[1]
    
    def sety(screen, value: float):
        screen.set_location(screen.x, value)
        
    y = property(gety, sety)
    
    def gettitle(screen):
        return screen.caption
    
    def settitle(screen, value: str):
        screen.set_caption(value)
        
    title = property(gettitle, settitle)
    
    def getfullscreen(screen):
        return screen._fullscreen
    
    def setfullscreen(screen, value: bool):
        screen.set_fullscreen(value)
        screen.resize = 1
        # 'screen.resize' becomes true when it enters fullscreen mode.
        
    fullscreen = property(getfullscreen, setfullscreen)
    
    def getrate(screen):
        return screen._rate
    
    def setrate(screen, value: float):
        # We write '1 / value' to make the user set the frames per second.
        screen.set_update_rate(1 / value)
        screen._rate = value
        
    rate = property(getrate, setrate)
    
    def getcolor(screen):
        return screen._color
    
    def setcolor(screen, value: Color):
        arcade.set_background_color(value)
        screen._color = value
        
    color = property(getcolor, setcolor)
        
    def centralize(screen):
        # A JoBase user could just use 'center_window'.
        screen.center_window()
        
    def exit(screen):
        screen.quit = 1
        
    def on_update(screen, time):
        screen.time = 1 / time
        
        arcade.start_render()
        
        if 'loop' in dir(module):
            module.loop()
        
        KEY.press = 0
        KEY.release = 0
        SCREEN.resize = 0
        MOUSE.press = 0
        MOUSE.release = 0
        MOUSE.up = 0
        MOUSE.down = 0
        MOUSE.move = 0
        MOUSE.scroll = 0
        
        if screen.quit:
            arcade.close_window()
            
        """
        When the user presses the close button, the 'module.loop()' function
        runs once before the window closes.
        """
        
    def on_close(screen):
        screen.quit = 1
        
    def on_mouse_motion(screen, x, y, dx, dy):
        MOUSE.move = 1
        MOUSE._x = x
        MOUSE._y = y        

    def on_mouse_scroll(screen, x, y, button, direction):
        MOUSE.scroll = 1
        
        if direction == 1.0:
            MOUSE.up = 1
            
        elif direction == -1.0:
            MOUSE.down = 1

    def on_mouse_press(screen, x, y, button, modifiers):
        MOUSE.press = 1
        
        if button == 1:
            MOUSE.left = 1
            
        elif button == 4:
            MOUSE.right = 1
            
        elif button == 2:
            MOUSE.middle = 1

    def on_mouse_release(screen, x, y, button, modifiers):
        MOUSE.release = 1
        
        if button == 1:
            MOUSE.left = 0
            
        elif button == 4:
            MOUSE.right = 0
            
        elif button == 2:
            MOUSE.middle = 0
        
    def on_resize(screen, width, height):
        super().on_resize(width, height)
        screen.resize = 1

    def on_key_press(screen, key, modifiers):
        KEY.press = 1
        
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key,
                                                            str(keys)):
                keys = keys.lower()
                setattr(KEY, str(keys), 1)
                
        # The code above finds all the values in 'arcade.key'. If a key is true,
        # we set the same JoBase key to true.

    def on_key_release(screen, key, modifiers):
        KEY.release = 1
        
        for keys in dir(arcade.key):
            if not keys.startswith('__') and key == getattr(arcade.key,
                                                            str(keys)):
                keys = keys.lower()
                setattr(KEY, str(keys), 0)
                
class Key:
    
    def __init__(key):
        key.press = 0
        key.release = 0
        
        for keys in dir(arcade.key):
            if not keys.startswith('__'):
                keys = keys.lower()
                setattr(key, str(keys), 0)
                
        # The code above finds all the values in 'arcade.key' and makes a
        # JoBase key with the same name (lowercase).
        
class Mouse:
    
    def __init__(mouse):
        mouse.press = 0
        mouse.release = 0
        mouse.left = 0
        mouse.right = 0
        mouse.middle = 0
        mouse.up = 0
        mouse.down = 0
        mouse.move = 0
        mouse.scroll = 0
        mouse._x = 0
        mouse._y = 0
        mouse._visible = True
        mouse._cursor = None
        
    def collide(mouse, other):
        return collide(other.boundary(), mouse.boundary())
        
    def boundary(mouse):
        return {'x': mouse._x, 'y': mouse._y, 'type': 'point'}
    
    def angle(mouse, other):
        return Angle(mouse.x, mouse.y, other.x, other.y)

    def distance(mouse, other):
        return Distance(mouse.x, mouse.y, other.x, other.y)
    
    def getvisible(mouse):
        return mouse._visible
    
    def setvisible(mouse, value: bool):
        SCREEN.set_mouse_visible(value)
        mouse._visible = value
        
    visible = property(getvisible, setvisible)
    
    def getcursor(mouse):
        return mouse._cursor
    
    def setcursor(mouse, name):
        SCREEN.set_mouse_cursor(SCREEN.get_system_mouse_cursor(name))
        mouse._cursor = name
        
    cursor = property(getcursor, setcursor)
        
    def getx(mouse):
        return mouse._x
    
    def setx(mouse, value: float):
        SCREEN.set_mouse_position(value, mouse._y)
        
    x = property(getx, setx)
    
    def gety(mouse):
        return mouse._y
    
    def sety(mouse, value: float):
        SCREEN.set_mouse_position(mouse._x, value)
        
    y = property(gety, sety)
    
KEY = Key()
MOUSE = Mouse()
SCREEN = Screen()