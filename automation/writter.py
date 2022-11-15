#!/usr/bin/python

from sys import argv

to_add = argv[1]


def add_generator(generator):
    data = None

    with open("./modules/__init__.py", "r") as file:
        data = file.read()

    data = data.split("\n")
    sep = [el for el in data if "from .generators import" in el][0]
    pos = data.index(sep)
    sep += f", {generator}"
    data[pos] = sep
    data = "\n".join(data)

    with open("./modules/__init__.py", "w") as file:
        file.write(data)


def add_page(page):
    with open("./modules/pages/__init__.py", "a") as file:
        file.write(f"from .{page}_page import {page.title()}Page\n")

    data = None

    with open("./modules/__init__.py", "r") as file:
        data = file.read()

    data = data.split("\n")
    sep = [el for el in data if "from .pages import" in el][0]
    pos = data.index(sep)
    sep += f", {page.title()}Page"
    data[pos] = sep
    data = "\n".join(data)

    with open("./modules/__init__.py", "w") as file:
        file.write(data)


add_generator(to_add)
add_page(to_add)