'''
Created on 12 Dec 2020

@author: Luke
'''
'''
Created on 12 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(12)

import numpy as np
import re

def get_input(input_type):
    if input_type == "test":
        ret = ["F10", "N3", "F7", "R90", "F11"]
    else:
        with open("input.txt") as f:
            ret = list(map(str.strip, f.readlines()))
    return ret


class Ship(object):
    
    compass_to_direction = {"E":np.array([1,0]),
                            "N":np.array([0,1]),
                            "W":np.array([-1, 0]),
                            "S":np.array([0, -1])}
    direction_to_compass = {tuple(a):b for (b,a) in compass_to_direction.items()}
    
    
    def __init__(self):
        self.waypoint_position = np.array([10,1])
        self.position = np.array([0,0]) # East
        
    def rotate(self, direction, angle):
        """
        Always rotate to the right - rotation to right is 360 minus
        rotation to left
        """
        if direction == "L":
            angle = 360 - angle
        elif direction == "R":
            pass
        else:
            raise RuntimeError(f"Unexpected direction '{direction}'")
        
        # Right rotation by number of degrees
        rotation = {90:np.array([[0, 1], [-1, 0]]),
                    180:np.array([[-1, 0], [0, -1]]),
                    270:np.array([[0, -1], [1, 0]])}
        
        self.waypoint_position = np.matmul(rotation[angle], self.waypoint_position)
        
    def move(self, direction, distance):
        if direction == "F":
            # Move towards ship towards the waypoint
            self.position += distance * self.waypoint_position
        else:
            # Move the waypoint
            self.waypoint_position += distance * self.compass_to_direction[direction]
    
    def parse(self, input_str):
        ret = re.match("([NSEWLRF])([0-9]+)", input_str)
        if ret is None:
            raise RuntimeError(f"Cannot parse string '{input_str}'")
        (order, numeric) = ret.groups()
        if order in ["L", "R"]:
            self.rotate(order, int(numeric))
        else:
            self.move(order, int(numeric))
    
    def manhatten_distance(self):
        return abs(self.position[0]) + abs(self.position[1])
    
    def __str__(self):
        return f"Location: {self.position[0], self.position[1]} (dist {self.manhatten_distance()})"
    
def run(input_type):
    s = Ship()
    for line in get_input(input_type):
        s.parse(line)
    print(s)
        