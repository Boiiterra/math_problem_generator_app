from random import seed, randint

from .c_seed import create_seed


def cb_root(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
	new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
	seed(new_seed)

	num = randint(1, 100)

	return num, num ** 3, new_seed
