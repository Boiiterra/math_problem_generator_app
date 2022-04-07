"""This file contains all generators used in the MAIN application"""
from requests.exceptions import RequestException
from pyautogui import position as mouse_pos
from random import seed, randint
from time import time, sleep
# Created by TerraBoii


def __create_seed(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int) -> float:
    # Getting application version from internet page, can be the same as installed one
    x, y = mouse_pos()
    # Rule 1 for generating seed: getting cursor position and manipulating with x, y values
    rule_1 = ((((int(str(x + 1) + str(y + 1)) * 2) // ((x + 1 * y + 1) + 1)) * (x + 1 + y + 1)) - (x + y)) * (x + 1 + y + 1)
    sleep(0.001)  # stoping program for 1 millisecond to get different time number
    # Rule 2: getting and manipulating with time
    rule_2 = int(''.join(str(time()).split('.'))) * ((int(str(time()).split('.')[0])) // (int(str(time()).split('.')[1])))
    # Rule 3: manipulating with app versions
    rule_3 = int((''.join(app_version.split('.'))) + (''.join(app_version.split('.')))) * \
             int((''.join(app_version.split('.'))) + (''.join(app_version.split('.'))))
    # Rule 4: manipulating with screen size data and window size
    dif_x = screen_width - app_width + 1 # (+ 1) in case of getting 0
    dif_y = screen_height - app_height + 1 # (+ 1) in case of getting 0
    rule_4 = ((((screen_width // dif_x) * app_width) + ((screen_height // dif_y) * app_height)) +
               (screen_width + screen_height + dif_x + dif_y + app_width + app_height))
    new_seed = ((rule_1 * rule_3) + rule_2) * rule_4
    return new_seed


def perimeter_task(figure: str, app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
    new_seed = __create_seed(app_version, app_width, app_height, screen_width, screen_height)
    seed(new_seed)
    if figure == 'square':
        side = randint(2, 100)
        answer = 4 * side
        return side, answer, new_seed
    elif figure == 'rectangle':
        height = randint(10, 120)
        width = randint(5, 75) + (height // 2) + 1
        answer = 2 * (height + width)
        return height, width, answer, new_seed


def area_task(figure: str, app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
    new_seed = __create_seed(app_version, app_width, app_height, screen_width, screen_height)
    seed(new_seed)
    if figure == 'square':
        side = randint(2, 100)
        answer = side * side
        return side, answer, new_seed
    elif figure == 'rectangle':
        height = randint(10, 120)
        width = randint(5, 75) + (height//2) + 1
        answer = height * width
        return height, width, answer, new_seed

def square_equation(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
    new_seed = __create_seed(app_version, app_width, app_height, screen_width, screen_height)
    seed(new_seed)
    x1 = randint(-10, 10)
    x2 = randint(-10, 10)
    a = randint(0, 4)

    if a == 0:
        a =1
    if x2 == 0 == x1:
        x2 += randint(1, 10)

    # Equation constructor
    equation = f"{a}(x^2)"
    if a == 1:
        equation = "(x^2)"

    if (-a*(x1+x2)) == 0:
        equation += f""
    elif (-a*(x1+x2)) < 0:
        equation += f"{-a*(x1+x2)}x"
    elif (-a*(x1+x2)) > 0:
        equation += f"+{-a*(x1+x2)}x"

    if (a*x1*x2) < 0:
        equation += f"{a*x1*x2}"
    elif (a*x1*x2) > 0:
        equation += f"+{a*x1*x2}"
    elif (a*x1*x2) == 0:
        equation += f""

    return x1, x2, equation, new_seed
