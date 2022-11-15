from random import seed, randint

from .c_seed import create_seed

def pythagorean_theorem(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
	new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
	seed(new_seed)

	c = 0.5
	while c % 1 != 0:
		a = randint(1, 99)
		b = randint(1, 99)
		c = pow(pow(a, 2) + pow(b, 2), 0.5)

	return c, a, b, new_seed
