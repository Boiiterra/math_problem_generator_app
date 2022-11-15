from random import seed, randint

from .c_seed import create_seed


def lin_equation(top, app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
	new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
	seed(new_seed)

	x = randint(-top, top)
	a = randint(-top, top)
	if a == 0: a += [-1, 1][randint(0, 1)]

	return x, f"{a}x = {a*x}", new_seed
