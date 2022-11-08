from random import seed, randint

from .c_seed import create_seed


def perimeter_task(figure: str, app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
    new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
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
