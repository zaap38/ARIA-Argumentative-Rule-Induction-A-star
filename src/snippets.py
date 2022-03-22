import random as rd


def pick(choices):
    return choices[rd.randint(0, len(choices) - 1)]
