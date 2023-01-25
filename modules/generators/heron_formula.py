"""More details at: https://github.com/TerraBoii/math_problem_generator_app/issues/31"""
from random import seed, randint
from math import sqrt

from .c_seed import create_seed


def __round(num):
	return int(num + 0.5)


def __p(a, b, c):
	return (a + b + c) / 2


def __S(a, b, c):
	p = __p(a, b, c)
	return __round(sqrt(p * (p - a) * (p - b) * (p - c)))


def heron_formula(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):
	new_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)
	seed(new_seed)

	a = b = 1
	c = 10

	while (a + b < c) or (a + c < b) or (c + b < a) or (a + b == c) or (a + c == b) or (c + b == a): # This is protection from bad results
		a = randint(1, 100)
		b = randint(1, 100)
		c = randint(1, 100)

	return __S(a, b, c), a, b, c, new_seed
