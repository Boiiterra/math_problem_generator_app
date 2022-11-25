from random import seed, randint

from .c_seed import create_seed


def power_number(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
	new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
	seed(new_seed)

	exp = randint(0, 8)
	num = 1

	if exp < 3:
		num = randint(1, 100)
	elif exp < 5:
		num = randint(1, 30)
	else:
		num = randint(1, 2)

	return pow(num, exp), num, exp, new_seed
