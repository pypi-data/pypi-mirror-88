import arcade, warnings

from arcade import Color
from arcade import PointList

from .collision import collide

from .point import rotate
from .point import scale_x
from .point import scale_y
from .point import find_center_x_of_points
from .point import find_center_y_of_points
from .point import find_left_of_points
from .point import find_top_of_points
from .point import find_right_of_points
from .point import find_bottom_of_points

from .math import Angle
from .math import Distance
from .math import Direction

class Base:
    
    def collide(self, other):
        return collide(self.boundary(), other.boundary())
    
    def angle(self, other):
        return Angle(self.x, self.y, other.x, other.y)

    def distance(self, other):
        return Distance(self.x, self.y, other.x, other.y)
    
class Point(Base):
    def __init__(self, x: float = 100, y: float = 100, color: Color = (0, 0, 0),
                 size: float = 10):
        
        super()
        
        self._x = x
        self._y = y
        self._color = color
        self._size = size
        
        self.shape = arcade.create_rectangle_filled(0, 0, size, size, color)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self._x
        self.element.center_y = self._y        
        
    def draw(self):
        self.element.draw()
        
    def boundary(self):
        return {'points': arcade.get_rectangle_points(self._x, self._y,
                                                      self._size, self._size,
                                                      0),
                'type': 'polygon'}
    
    def update(self):
        self.shape = arcade.create_rectangle_filled(0, 0, self._size,
                                                    self._size, self._color)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self._x
        self.element.center_y = self._y
        
    def get_top(self):
        return self._y + self._size / 2
    
    def set_top(self, value: float):
        distance = (value - self._size / 2) - self._y
        self._y = value - self._size / 2
        
        self.element.center_y += distance
        
    top = property(get_top, set_top)
    
    def get_bottom(self):
        return self._y - self._size / 2
    
    def set_bottom(self, value: float):
        distance = (value + self._size / 2) - self._y
        self._y = value + self._size / 2
        
        self.element.center_y += distance
        
    bottom = property(get_bottom, set_bottom)
    
    def get_left(self):
        return self._x - self._size / 2
    
    def set_left(self, value: float):
        distance = (value - self._size / 2) - self._x
        self._x = value - self._size / 2
        
        self.element.center_x += distance
        
    left = property(get_left, set_left)
    
    def get_right(self):
        return self._x + self._size / 2
    
    def set_right(self, value: float):
        distance = (value + self._size / 2) - self._x
        self._x = value + self._size / 2
        
        self.element.center_x += distance
        
    right = property(get_right, set_right)
    
    def get_x(self):
        return self._x
    
    def set_x(self, value: float):
        distance = value - self._x
        self._x = value
        
        self.element.center_x += distance
                    
    x = property(get_x, set_x)

    def get_y(self):
        return self._y
    
    def set_y(self, value: float):
        distance = value - self._y
        self._y = value
        
        self.element.center_y += distance
            
    y = property(get_y, set_y)
    
    def get_size(self):
        return self._size
    
    def set_size(self, value: float):
        self._size = value
        
        self.update()
            
    size = property(get_size, set_size)
    
    def get_color(self):
        return self._color
    
    def set_color(self, value: Color):
        self._color = value
        
        self.update()
            
    color = property(get_color, set_color)    
       
class Line(Base):
    
    def __init__(self, x1: float = 0, y1: float = 0, x2: float = 100,
                 y2: float = 100, thickness: float = 1,
                 color: Color = (0, 0, 0)):
        
        super()
        
        self._x1 = x1
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._thickness = thickness
        self._rotation = 0
        self._color1 = color
        self._color2 = color
        
        self.shape = arcade.create_line(x1 - self.x, y1 - self.y, x2 - self.x,
                                        y2 - self.y, color, thickness)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self.x
        self.element.center_y = self.y
                        
    def draw(self):
        self.element.draw()
        
    def boundary(self):
        points = rotate(((self._x1, self._y1), (self._x2, self._y2)),
                        self._rotation, self.x, self.y)
        
        return {'points': arcade.get_points_for_thick_line(points[0][0],
                                                           points[0][1],
                                                           points[1][0],
                                                           points[1][1],
                                                           self._thickness),
                'type': 'polygon'}
    
    def update(self):
        points = (self._x1 - self.x, self._y1 - self.y), (self._x2 - self.x,
                                                          self._y2 - self.y)
        
        self.shape = arcade.create_lines_with_colors(
            points,
            [self._color1, self._color2],
            line_width = self._thickness)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self.x
        self.element.center_y = self.y
        self.element.angle = self._rotation
        
    def get_x(self):
        return (self.x1 + self.x2) / 2
    
    def set_x(self, value: float):
        difference = value - self.x
        
        self._x1 += difference
        self._x2 += difference
        
        self.element.center_x += difference
                    
    x = property(get_x, set_x)

    def get_y(self):
        return (self.y1 + self.y2) / 2
    
    def set_y(self, value: float):
        difference = value - self.y
        
        self._y1 += difference
        self._y2 += difference
        
        self.element.center_y += difference
            
    y = property(get_y, set_y)
    
    def get_x1(self):
        return self._x1
    
    def set_x1(self, value: float):
        if self._x1 is not value:
            self._x1 = value
                
            self.update()
        
    x1 = property(get_x1, set_x1)
    
    def get_y1(self):
        return self._y1
    
    def set_y1(self, value: float):
        if self._y1 is not value:
            self._y1 = value
        
            self.update()
                
    y1 = property(get_y1, set_y1)
    
    def get_x2(self):
        return self._x2
    
    def set_x2(self, value: float):
        if self._x2 is not value:
            self._x2 = value
        
            self.update()
        
    x2 = property(get_x2, set_x2)
    
    def get_y2(self):
        return self._y2
    
    def set_y2(self, value: float):
        if self._y2 is not value:
            self._y2 = value
        
            self.update()
        
    y2 = property(get_y2, set_y2)
    
    def get_color(self):
        if self._color1 == self._color2:
            return self._color1
        
        return self._color1, self._color2
    
    def set_color(self, value: Color):
        if self._color1 is not value or self._color2 is not value:
            self._color1 = value
            self._color2 = value
        
            self.update()
        
    color = property(get_color, set_color)
    
    def get_color1(self):
        return self._color1
    
    def set_color1(self, value: Color):
        if self._color1 is not value:
            self._color1 = value
        
            self.update()
        
    color1 = property(get_color1, set_color1)
    
    def get_color2(self):
        return self._color2
    
    def set_color2(self, value: Color):
        if self._color2 is not value:
            self._color2 = value
        
            self.update()
        
    color2 = property(get_color2, set_color2)    
    
    def get_thickness(self):
        return self._thickness
    
    def set_thickness(self, value: float):
        if self._thickness is not value:
            self._thickness = value
        
            self.update()
        
    thickness = property(get_thickness, set_thickness)
        
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, value: float):
        difference = value - self._rotation
        self._rotation = value
        
        self.element.angle += difference
            
    rotation = property(get_rotation, set_rotation)

    def get_top(self):
        if self._y1 > self._y2:
            return self._y1
        
        return self._y2
        
        # It doesn't actually find the top of the line, just the highest point.
        
    def set_top(self, value: float):
        if self._y1 > self._y2:
            top = self._y1
            
        else:
            top = self._y2
            
        distance = value - top
        self._y1 += distance
        self._y2 += distance
        
        self.element.center_y += distance
        
    top = property(get_top, set_top)

    def get_bottom(self):
        if self._y1 < self._y2:
            return self._y1
        
        return self._y2
        
    def set_bottom(self, value: float):
        if self._y1 < self._y2:
            bottom = self._y1
            
        else:
            bottom = self._y2
                        
        distance = value - bottom
        self._y1 += distance
        self._y2 += distance
        
        self.element.center_y += distance
        
    bottom = property(get_bottom, set_bottom)

    def get_left(self):
        if self._x1 < self._x2:
            return self._x1
        
        return self._x2
        
    def set_left(self, value: float):
        if self._x1 < self._x2:
            left = self._x1
            
        else:
            left = self._x2
            
        distance = value - left
        self._x1 += distance
        self._x2 += distance
        
        self.element.center_x += distance
        
    left = property(get_left, set_left)

    def get_right(self):
        if self._x1 > self._x2:
            return self._x1
        
        return self._x2
        
    def set_right(self, value: float):
        if self._x1 > self._x2:
            right = self._x1
            
        else:
            right = self._x2      
            
        distance = value - right
        self._x1 += distance
        self._x2 += distance
        
        self.element.center_x += distance
        
    right = property(get_right, set_right)
    
class Strip(Base):
    
    def __init__(self,
                 points: PointList = ((0, 0), (100, 100), (150, 50), (0, 0)),
                 color: Color = (0, 0, 0)):
        
        super()
        
        self._points = [list(point) for point in points]
        self._color = color
        self._thickness = 1
        self._rotation = 0
        
        positions = []
        
        for point in points:
            position = (point[0] - self.x, point[1] - self.y)
            
            positions.append(position)
                    
        self.shape = arcade.create_line_strip(positions, color, self._thickness)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self.x
        self.element.center_y = self.y
                        
    def draw(self):
        self.element.draw()
                
    def boundary(self):
        return {'type': 'none'}
    
    def update(self):
        positions = []
        
        for point in self._points:
            position = (point[0] - self.x, point[1] - self.y)
            
            positions.append(position)
        
        self.shape = arcade.create_line_strip(positions, self._color,
                                              self._thickness)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self.x
        self.element.center_y = self.y
        self.element.angle = self._rotation
    
    def get_x(self):
        return find_center_x_of_points(self._points)
    
    def set_x(self, value: float):
        distance = value - self.x
        
        for point in self._points:
            point[0] += distance
            
        self.element.center_x += distance
            
    x = property(get_x, set_x)

    def get_y(self):
        return find_center_y_of_points(self._points)
    
    def set_y(self, value: float):
        distance = value - self.y
        
        for point in self.points:
            point[1] += distance
            
        self.element.center_y += distance
            
    y = property(get_y, set_y)
                  
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, value: float):
        distance = value - self._rotation
        self._rotation = value
            
        self.element.angle += distance
    
    rotation = property(get_rotation, set_rotation)
    
    def get_top(self):
        return find_top_of_points(self._points)
    
    def set_top(self, value: float):
        distance = value - self.top
        
        for point in self.points:
            point[1] += distance
            
        self.element.center_y += distance
            
    top = property(get_top, set_top)
    
    def get_bottom(self):
        return find_bottom_of_points(self._points)
    
    def set_bottom(self, value: float):
        distance = value - self.bottom
        
        for point in self.points:
            point[1] += distance
            
        self.element.center_y += distance
            
    bottom = property(get_bottom, set_bottom)
    
    def get_left(self):
        return find_left_of_points(self._points)
    
    def set_left(self, value: float):
        distance = value - self.left
        
        for point in self.points:
            point[0] += distance
            
        self.element.center_x += distance
            
    left = property(get_left, set_left)
    
    def get_right(self):
        return find_right_of_points(self._points)
    
    def set_right(self, value: float):
        distance = value - self.right
        
        for point in self.points:
            point[0] += distance
            
        self.element.center_x += distance
            
    right = property(get_right, set_right)
    
    def get_points(self):
        return self._points
    
    def set_points(self, value: PointList):
        if self._points is not value:
            self._points = value
            
            self.update()
            
    points = property(get_points, set_points)
    
    def get_color(self):
        return self._color
    
    def set_color(self, value: Color):
        if self._color is not value:
            self._color = value
            
            self.update()
            
    color = property(get_color, set_color)
    
    def get_thickness(self):
        return self._thickness
    
    def set_thickness(self, value: float):
        if self._thickness is not value:
            self._thickness = value
            
            self.update()
            
    thickness = property(get_thickness, set_thickness)
        
class Shape(Base):
    
    def __init__(self,
                 points: PointList = ((0, 0), (100, 200), (150, 100), (90, 10)),
                 color: Color = (0, 0, 0), outline: float = 0):
                
        super()
        
        self._points = [list(point) for point in points]
        self._color = color
        self._outline = outline
        self._rotation = 0
        
        positions = []
        
        for point in points:
            position = (point[0] - self.x, point[1] - self.y )
            
            positions.append(position)
                    
        if self.outline == 0:
            self.shape = arcade.create_polygon(positions, color)
            
        else:
            self.shape = arcade.create_line_loop(positions, color, outline)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self.x
        self.element.center_y = self.y        
        
    def draw(self):
        self.element.draw()
        
    def boundary(self):
        positions = rotate(self._points, self._rotation, self.x, self.y)
                
        return {'points': positions,
                'type': 'polygon'}
    
    def update(self):
        positions = []
        
        for point in self._points:
            position = (point[0] - self.x, point[1] - self.y)
            
            positions.append(position)
                    
        if self.outline == 0:
            self.shape = arcade.create_polygon(positions, self._color)
            
        else:
            self.shape = arcade.create_line_loop(positions, self._color,
                                                 self._outline)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self.x
        self.element.center_y = self.y
        self.element.angle = self._rotation

    def get_x(self):
        return find_center_x_of_points(self._points)
    
    def set_x(self, value: float):
        difference = value - self.x
        
        for point in self._points:
            point[0] += difference
            
        self.element.center_x += difference
            
    x = property(get_x, set_x)

    def get_y(self):
        return find_center_y_of_points(self._points)
    
    def set_y(self, value: float):
        difference = value - self.y
        
        for point in self.points:
            point[1] += difference
            
        self.element.center_y += difference
            
    y = property(get_y, set_y)
    
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, value: float):
        difference = value - self._rotation
        self._rotation = value
            
        self.element.angle += difference
    
    rotation = property(get_rotation, set_rotation)
    
    def get_top(self):
        return find_top_of_points(self._points)
    
    def set_top(self, value: float):
        distance = value - self.top
        
        for point in self.points:
            point[1] += distance
            
        self.element.center_y += distance
            
    top = property(get_top, set_top)
    
    def get_bottom(self):
        return find_bottom_of_points(self._points)
    
    def set_bottom(self, value: float):
        distance = value - self.bottom
        
        for point in self.points:
            point[1] += distance
            
        self.element.center_y += distance
            
    bottom = property(get_bottom, set_bottom)
    
    def get_left(self):
        return find_left_of_points(self._points)
    
    def set_left(self, value: float):
        distance = value - self.left
        
        for point in self.points:
            point[0] += distance
            
        self.element.center_x += distance
            
    left = property(get_left, set_left)
    
    def get_right(self):
        return find_right_of_points(self._points)
    
    def set_right(self, value: float):
        distance = value - self.right
        
        for point in self.points:
            point[0] += distance
            
        self.element.center_x += distance
            
    right = property(get_right, set_right)
    
    def get_points(self):
        return self._points
    
    def set_points(self, value: PointList):
        if self._points is not value:
            self._points = value
            
            self.update()
            
    points = property(get_points, set_points)
    
    def get_color(self):
        return self._color
    
    def set_color(self, value: Color):
        if self._color is not value:
            self._color = value
            
            self.update()
            
    color = property(get_color, set_color)
    
    def get_outline(self):
        return self._outline
    
    def set_outline(self, value: bool):
        if self._outline is not value:
            self._outline = value
            
            self.update()
            
    outline = property(get_outline, set_outline)
    
class Circle(Base):
    
    def __init__(self, x: float = 100, y: float = 100, size: float = 50,
                 color: Color = (0, 0, 0), outline: float = 1):
        
        super()
        
        self._x = x
        self._y = y
        self._size = size
        self._color1 = color
        self._color2 = color
        self._outline = outline
        self.resolution = 32
        
        self.update()
        
    def draw(self):
        self.element.draw()
        
    def boundary(self):
        positions = []
        
        for index in range(1, self.resolution):
            x, y = Direction(self._size, index * 360 / self.resolution)
            point = [self._x + x, self.y + y]
            
            positions.append(point)
                        
        return {'points': positions,
                'type': 'polygon'}
        
    def update(self):
        if self._outline == 0:
            self.shape = arcade.create_ellipse_filled_with_colors(0, 0,
                                                                  self._size,
                                                                  self._size,
                                                                  self._color1,
                                                                  self._color2)
            
        else:
            self.shape = arcade.create_ellipse(0, 0, self._size, self._size,
                                               self._color1, self._outline)
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self._x
        self.element.center_y = self._y        
    
    def get_x(self):
        return self._x
    
    def set_x(self, value: float):
        distance = value - self._x
        
        self._x = value
            
        self.element.center_x += distance
            
    x = property(get_x, set_x)
    
    def get_y(self):
        return self._y
    
    def set_y(self, value: float):
        distance = value - self._y
        
        self._y = value
            
        self.element.center_y += distance
            
    y = property(get_y, set_y)
    
    def get_top(self):
        return self._y + self._size
    
    def set_top(self, value: float):
        distance = value - self.top
        
        self._y = value - self._size
            
        self.element.center_y += distance
            
    top = property(get_top, set_top)
    
    def get_bottom(self):
        return self._y - self._size
    
    def set_bottom(self, value: float):
        distance = value - self.bottom
        
        self._y = value + self._size
            
        self.element.center_y += distance
            
    bottom = property(get_bottom, set_bottom)
    
    def get_left(self):
        return self._x - self._size
    
    def set_left(self, value: float):
        distance = value - self.left
        
        self._x = value + self._size
            
        self.element.center_x += distance
            
    left = property(get_left, set_left)
    
    def get_right(self):
        return self._x + self._size
    
    def set_right(self, value: float):
        distance = value - self.right
        
        self._x = value - self._size
            
        self.element.center_x += distance
            
    right = property(get_right, set_right)
    
    def get_size(self):
        return self._size
    
    def set_size(self, value: float):
        self._size = value
            
        self.update()
            
    size = property(get_size, set_size)
    
    def get_color(self):
        if self._color1 == self._color2:
            return self._color1
        
        return self._color1, self._color2
    
    def set_color(self, value: Color):
        self._color1 = value
        self._color2 = value
        
        self.update()
        
    color = property(get_color, set_color)
    
    def get_color1(self):
        return self._color1
    
    def set_color1(self, value: Color):
        self._color1 = value
        
        self.update()
        
    color1 = property(get_color1, set_color1)
    
    def get_color2(self):
        return self._color2
    
    def set_color2(self, value: Color):
        self._color2 = value
        
        self.update()
        
    color2 = property(get_color2, set_color2)
    
    def get_outline(self):
        return self._outline
    
    def set_outline(self, value: float):
        self._outline = value
        
        self.update()
        
    outline = property(get_outline, set_outline)
            
class Rectangle(Base):
    
    def __init__(self, x: float = 100, y: float = 100, width: float = 50,
                 height: float = 30, color: Color = (0, 0, 0),
                 outline: float = 0):
        
        super()
        
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color1 = color
        self._color2 = color
        self._color3 = color
        self._color4 = color
        self._outline = outline
        self._rotation = 0
        
        if outline == 0:
            self.shape = arcade.create_rectangle_filled_with_colors(
                arcade.get_rectangle_points(0, 0, width, height),
                (color, color, color, color))
            
        else:
            self.shape = arcade.create_rectangle_outline(0, 0, width, height,
                                                         color, outline)    
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = x
        self.element.center_y = y
        
    def draw(self):
        self.element.draw()
        
    def boundary(self):
        return {'points': arcade.get_rectangle_points(self._x, self._y,
                                                      self._width, self._height,
                                                      self._rotation),
                'type': 'polygon'}
    
    def update(self):
        if self._outline == 0:
            self.shape = arcade.create_rectangle_filled_with_colors(
                arcade.get_rectangle_points(0, 0, self._width, self._height),
                (self._color1, self._color2, self._color3, self._color4))
        
        else:
            self.shape = arcade.create_rectangle_outline(0, 0, self._width,
                                                         self._height,
                                                         self._color1,
                                                         self._outline)        
        
        self.element = arcade.ShapeElementList()
        self.element.append(self.shape)
        
        self.element.center_x = self._x
        self.element.center_y = self._y
        self.element.angle = self._rotation
    
    def get_top(self):
        return find_top_of_points(arcade.get_rectangle_points(self._x,
                                                              self._y,
                                                              self._width,
                                                              self._height,
                                                              self._rotation))
    
    def set_top(self, value: float):
        distance = value - self.top
        
        self._y += distance
        self.element.center_y += distance
        
    top = property(get_top, set_top)
    
    def get_bottom(self):
        return find_bottom_of_points(arcade.get_rectangle_points(
            self._x,
            self._y,
            self._width,
            self._height,
            self._rotation))
    
    def set_bottom(self, value: float):
        distance = value - self.bottom
        
        self._y += distance
        self.element.center_y += distance
        
    bottom = property(get_bottom, set_bottom)
    
    def get_left(self):
        return find_left_of_points(arcade.get_rectangle_points(self._x,
                                                               self._y,
                                                               self._width,
                                                               self._height,
                                                               self._rotation))
    
    def set_left(self, value: float):
        distance = value - self.left
        
        self._x += distance
        self.element.center_x += distance
        
    left = property(get_left, set_left)
    
    def get_right(self):
        return find_right_of_points(arcade.get_rectangle_points(self._x,
                                                                self._y,
                                                                self._width,
                                                                self._height,
                                                                self._rotation))
    
    def set_right(self, value: float):
        distance = value - self.right
        
        self._x += distance
        self.element.center_x += distance
        
    right = property(get_right, set_right)
    
    def get_x(self):
        return self._x
    
    def set_x(self, value: float):
        difference = value - self.x
        
        self._x += difference
        self.element.center_x += difference
            
    x = property(get_x, set_x)

    def get_y(self):
        return self._y
    
    def set_y(self, value: float):
        difference = value - self.y
        
        self._y += difference
        self.element.center_y += difference
            
    y = property(get_y, set_y)
    
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, value: float):
        difference = value - self._rotation
        
        self._rotation = value
        self.element.angle += difference
    
    rotation = property(get_rotation, set_rotation)
    
    def get_width(self):
        return self._width
    
    def set_width(self, value: float):
        if self._width is not value:
            self._width = value
            
            self.update()
    
    width = property(get_width, set_width)
    
    def get_height(self):
        return self._height
    
    def set_height(self, value: float):
        if self._height is not value:
            self._height = value
            
            self.update()
    
    height = property(get_height, set_height)
    
    def get_color(self):
        if self._color1 == self._color2 == self.color3 == self.color4:
            return self._color1
        
        return self._color1, self._color2, self._color3, self._color4
    
    def set_color(self, value: Color):
        if (self._color1 is not value or self._color2 is not value
            or self._color3 is not value or self._color4 is not value):
            
            self._color1 = value
            self._color2 = value
            self._color3 = value
            self._color4 = value            
        
            self.update()
        
    color = property(get_color, set_color)
    
    def get_color1(self):
        return self._color1
    
    def set_color1(self, value: Color):
        if self._color1 is not value:
            self._color1 = value
        
            self.update()
        
    color1 = property(get_color1, set_color1)
    
    def get_color2(self):
        return self._color2
    
    def set_color2(self, value: Color):
        if self._color2 is not value:
            self._color2 = value
        
            self.update()
            
    color2 = property(get_color2, set_color2)
            
    def get_color3(self):
        return self._color3
    
    def set_color3(self, value: Color):
        if self._color3 is not value:
            self._color3 = value
        
            self.update()
            
    color3 = property(get_color3, set_color3)
            
    def get_color4(self):
        return self._color4
    
    def set_color4(self, value: Color):
        if self._color4 is not value:
            self._color4 = value
        
            self.update()
            
    color4 = property(get_color4, set_color4)
    
    def get_outline(self):
        return self._outline
    
    def set_outline(self, value: float):
        if self._outline is not value:
            self._outline = value
            
            self.update()
    
    outline = property(get_outline, set_outline)    
            
class Image(Base):
    
    def __init__(self, name: str = 'man.png', x: float = 100,
                 y: float = 100, flip_horizontally: bool = False,
                 flip_vertically: bool = False,
                 flip_diagonally: bool = False,
                 rotation: float = 0, detail: float = 5):
        
        super()

        self.texture = arcade.load_texture(str(name), 0, 0, 0, 0,
                                           flip_horizontally, flip_vertically,
                                           flip_diagonally)
        
        self._x = x
        self._y = y
        self._width = self.texture.width
        self._height = self.texture.height
        self._detail = detail
        self._rotation = rotation
        
        self.calculate()
        
    def draw(self):
        arcade.draw_texture_rectangle(self._x, self._y, self._width,
                                      self._height, self.texture,
                                      self._rotation)
        
    def boundary(self):                            
        return {
            'points': self.collision,
            'type': 'polygon'}
    
    def calculate(self):
        self.collision = [list(point)
                          for point in arcade.calculate_hit_box_points_detailed(
                              self.texture.image, self._detail)]
        
        for point in self.collision:
            point[0] += self._x
            point[1] += self._y
            
        self.collision = rotate(self.collision, self._rotation, self._x,
                                self._y)
        
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, value: float):
        difference = value - self._rotation
        
        self._rotation = value
        
        self.collision = rotate(self.collision, difference, self._x, self._y)
    
    rotation = property(get_rotation, set_rotation)
    
    def get_detail(self):
        return self._detail
    
    def set_detail(self, value: float):
        if self._detail is not value:
            self._detail = value
        
            self.calculate()
    
    detail = property(get_detail, set_detail)    
    
    def get_x(self):
        return self._x
    
    def set_x(self, value: float):
        difference = value - self._x
        
        for point in self.collision:
            point[0] += difference
            
        self._x = value
            
    x = property(get_x, set_x)

    def get_y(self):
        return self._y
    
    def set_y(self, value: float):
        difference = value - self._y
        
        for point in self.collision:
            point[1] += difference
            
        self._y = value
            
    y = property(get_y, set_y)
    
    def get_width(self):
        return self._width
    
    def set_width(self, value: float):
        difference = value / self._width
        
        self.collision = rotate(self.collision, -self._rotation, self._x,
                                self._y)        
        self.collision = scale_x(self.collision, self._x, difference)
        self.collision = rotate(self.collision, self._rotation, self._x,
                                self._y)        
            
        self._width = value
            
    width = property(get_width, set_width)
    
    def get_height(self):
        return self._height
    
    def set_height(self, value: float):
        difference = value / self._height
        
        self.collision = rotate(self.collision, -self._rotation, self._x,
                                self._y)
        self.collision = scale_y(self.collision, self._y, difference)
        self.collision = rotate(self.collision, self._rotation, self._x,
                                self._y)
            
        self._height = value
            
    height = property(get_height, set_height)

    def get_top(self):
        return find_top_of_points(self.collision)
    
    def set_top(self, value: float):
        distance = value - self.top
            
        self.y += distance
            
    top = property(get_top, set_top)
    
    def get_bottom(self):
        return find_bottom_of_points(self.collision)
    
    def set_bottom(self, value: float):
        distance = value - self.bottom
            
        self.y += distance
            
    bottom = property(get_bottom, set_bottom)
    
    def get_left(self):
        return find_left_of_points(self.collision)
    
    def set_left(self, value: float):
        distance = value - self.left
            
        self.x += distance
            
    left = property(get_left, set_left)
    
    def get_right(self):
        return find_right_of_points(self.collision)
    
    def set_right(self, value: float):
        distance = value - self.right
            
        self.x += distance
            
    right = property(get_right, set_right)
                
class Text(Base):
    
    def __init__(self, content: str = 'hello', x: float = 100, y: float = 100,
                 color: Color = (0, 0, 0), size: float = 40):
        
        super()
        
        self.content = content
        self._x = x
        self._y = y
        self.color = color
        self.size = size
        self._rotation = 0
        
        self.data = arcade.draw_text(self.content, self._x, self._y,
                                     self.color, self.size,
                                     rotation = self._rotation)

    def draw(self):
        self.data = arcade.draw_text(self.content, self._x, self._y,
                                     self.color, self.size,
                                     rotation = self._rotation)
    
    def calculate(self):
        self.collision = [list(point)
                          for point in arcade.calculate_hit_box_points_simple(
                              self.data.texture.image)]
            
        self.collision = rotate(self.collision, self._rotation, 0, 0)
        
        for point in self.collision:
            point[0] += self.x
            point[1] += self.y
            
    def clear(self):
        text.content = ''
        
    def boundary(self):
        self.calculate()
        
        return {'points': self.collision,
                'type': 'polygon'}
    
    def get_x(self):
        return self._x + self.data.width / 2
    
    def set_x(self, value: float):
        difference = value - self.x
        
        self._x += difference
        
    x = property(get_x, set_x)
    
    def get_y(self):
        return self._y + self.data.height / 2
    
    def set_y(self, value: float):
        difference = value - self.y

        self._y += difference        
        
    y = property(get_y, set_y)
    
    def get_rotation(self):
        return self._rotation
    
    def set_rotation(self, value: float):
        self._rotation = value
            
    rotation = property(get_rotation, set_rotation)    
        
    def get_width(self):
        return self.data.width
    
    def set_width(self, value: float):
        self.data.width = value
        
    width = property(get_width, set_width)
    
    def get_height(self):
        return self.data.height
    
    def set_height(self, value: float):
        self.data.height = value
        
    height = property(get_height, set_height)    

    def get_top(self):
        return self._y + self.data.height
    
    def set_top(self, value: float):
        self.y = value - self.data.height / 2
        
    top = property(get_top, set_top)
    
    def get_bottom(self):
        return self._y
    
    def set_bottom(self, value: float):
        self.y = value + self.data.height / 2
        
    bottom = property(get_bottom, set_bottom)
    
    def get_left(self):
        return self._x
    
    def set_left(self, value: float):
        self.x = value + self.data.width / 2
        
    left = property(get_left, set_left)
    
    def get_right(self):
        return self._x + self.data.width
    
    def set_right(self, value: float):
        self.x = value - self.data.width / 2
        
    right = property(get_right, set_right)