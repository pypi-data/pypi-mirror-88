import math, warnings, arcade

from arcade import PointList

def collide(type1: dict, type2: dict):
    # The code below checks every combination of collision. At the moment there
    # are three types of collision: point, rectangle and circle.
    
    if type1['type'] == 'none' or type2['type'] == 'none':
        warnings.warn("You entered a shape that doesn't have collision.")
        
    elif type1['type'] == 'point' and type2['type'] == 'point':
        
        if rect_to_point_collision(type1['x'], type1['y'],
                                   type2['x'], type2['y']):
            return True
        
        return False
    
    elif type1['type'] == 'polygon' and type2['type'] == 'polygon':
        
        if polygon_to_polygon_collision(type1['points'], type2['points']):
            return True
        
        return False
    
    elif type1['type'] == 'point' and type2['type'] == 'polygon':
        
        if point_to_polygon_collision(type1['x'], type1['y'], type2['points']):
            return True
        
        return False
    
    elif type1['type'] == 'polygon' and type2['type'] == 'point':
        
        if point_to_polygon_collision(type2['x'], type2['y'], type1['points']):
            return True
        
        return False
    
def point_to_point_collision(x1: float, y1: float, x2: float, y2: float):
    return x1 == x2 and y1 == y2

def polygon_to_polygon_collision(points1: PointList, points2: PointList):
    if arcade.are_polygons_intersecting(points1, points2):
        return True
    
    return False

def point_to_polygon_collision(x1: float, y1: float, points2: PointList):
    return arcade.is_point_in_polygon(x1, y1, points2)