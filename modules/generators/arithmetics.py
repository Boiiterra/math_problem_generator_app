from random import seed, randint, choice

from .c_seed import create_seed


def arithmetics(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
    new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
    seed(new_seed)

    actions = ["+", "-", "*", "/"]

    a, b = randint(-100, 100), randint(-100, 100)
    action = choice(actions)
    text = ""

    if a == b == 0:
        b += 1

    if action == "/" and a % b != 0:
        action = choice(actions[:-1])

    if a < 0:
        text += f"({a}) {action} "
    else:
        text += f"{a} {action} "

    if b < 0:
        text += f"({b})"
    else:
        text += f"{b}"

    match action:
        case "+":
            return text, a + b, new_seed
        case "-":
            return text, a - b, new_seed
        case "*":
            return text, a * b, new_seed
        case "/":
            return text, a / b, new_seed
