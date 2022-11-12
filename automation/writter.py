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


add_generator(to_add)