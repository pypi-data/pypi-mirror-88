import arcade, math, random

def Distance(x1: float, y1: float, x2: float, y2: float):
    return arcade.get_distance(x1, x2, y1, y2)

def Angle(x1: float, y1: float, x2: float, y2: float):
    x, y = x2 - x1, y2 - y1
    radians = math.atan2(y, x)
    radians %= 2 * math.pi
    degrees = math.degrees(radians)
    
    return degrees

def Direction(length: float, angle: float):
    x = length * math.cos(math.radians(angle))
    y = length * math.sin(math.radians(angle))
    
    return x, y

def Random(int1: int, int2: int):
    if int1 > int2:
        return random.randint(int2, int1)

    return random.randint(int1, int2)
    
def Random_Angle():
    return Random(1, 360)
    
def Pause(time: float):
    arcade.pause(time)