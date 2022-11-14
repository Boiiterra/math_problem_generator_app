from random import seed, randint

from .c_seed import create_seed

def gauss_sum(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
	new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
	seed(new_seed)

	top = 1
	while top % 2 != 0:
		top = randint(10, 10000)

	return sum([el for el in range(1, top+1)]), top, new_seed
