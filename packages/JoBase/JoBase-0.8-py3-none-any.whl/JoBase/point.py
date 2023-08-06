import math, arcade

from arcade import PointList

from .math import Angle
from .math import Distance
from .math import Direction

def scale_x(points, center_x, x_scale):
    
    positions = []
    
    for point in points:
        distance_x = point[0] - center_x
        positions.append((center_x + distance_x * x_scale, point[1]))
        
    return positions
        
def scale_y(points, center_y, y_scale):
    
    positions = []
    
    for point in points:
        distance_y = point[1] - center_y
        positions.append((point[0], center_y + distance_y * y_scale))
        
    return positions
            
def rotate(points: PointList, rotation: float, center_x: float,
           center_y: float):
    
    positions = []
    
    for point in points:        
        positions.append(arcade.rotate_point(point[0], point[1], center_x,
                                             center_y, rotation))
        
    return positions
        
def find_center_x_of_points(points: PointList):
    center_x = 0
    
    for point in points:
        center_x += point[0]
        
    center_x /= len(points)
    
    return center_x

def find_center_y_of_points(points: PointList):
    center_y = 0
    
    for point in points:
        center_y += point[1]
        
    center_y /= len(points)
    
    return center_y
            
def find_left_of_points(points: PointList):
    left = 0
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[0] < left:
                left = point[0]
                
        else:
            left = point[0]
            
    return left

def find_top_of_points(points: PointList):
    top = 0
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[1] > top:
                top = point[1]
                
        else:
            top = point[1]
            
    return top

def find_right_of_points(points: PointList):
    right = 0  
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[0] > right:
                right = point[0]
                
        else:
            right = point[0]
            
    return right

def find_bottom_of_points(points: PointList):
    bottom = 0    
    
    for point in points:
        
        if not points.index(point) == 0:
            
            if point[1] < bottom:
                bottom = point[1]
                
        else:
            bottom = point[1]
            
    return bottom