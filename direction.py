'''
This module implement Enumerations to overcome
the multiple definition of directions and rotations
functions of the class Tello
'''
from enum import Enum


class Direction(Enum):
    '''Describes the direction
    value you can choose
    '''
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    FORWARD = 'forward'
    BACK = 'BACK'


class Clockwise(Enum):
    '''Descibes the rotation direction you can
    choose: clockwise or counterclockwise
    '''
    CW = 'cw'
    CCW = 'ccw'
