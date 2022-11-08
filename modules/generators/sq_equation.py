from random import seed, randint

from .c_seed import create_seed


def square_equation(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
    new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
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
