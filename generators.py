"""This file contains all generators used in the application"""
from time import time, sleep
from random import seed, randint
from ctypes import windll, Structure, c_long, byref


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def getCursorPosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}


def get_seed() -> float:
    cursor_position = getCursorPosition()
    x, y = cursor_position['x'], cursor_position['y']
    rule_1 = ((((int(str(x + 1) + str(y + 1)) * 2) // ((x + 1 * y + 1) + 1)) * (x + 1 + y + 1)) - (x + y)) * (x + 1 + y + 1)
    sleep(0.001) # stoping program for 1 millisecond to get different time number
    return rule_1 + time()


def perimeter_task(figure: str):
    new_seed = get_seed()
    seed(new_seed)
    if figure == 'square_task':
        return randint(2, 100)
    elif figure == 'rectangle':
        a = randint(10, 120)
        b = randint(5, 75) + (a//2) + 1
        return a, b


def square_task(figure: str):
    new_seed = get_seed()
    seed(new_seed)
    if figure == 'square_task':
        return randint(2, 100)
    elif figure == 'rectangle':
        a = randint(10, 120)
        b = randint(5, 75) + (a//2) + 1
        return a, b