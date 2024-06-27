from math import *


def f1(x, z):
    # return sqrt(x * x + z * z) + 3 * cos(sqrt(x * x + z * z)) - 5
    return sin(x) * cos(z / 2) + cos(x) * sin(z / 2)


def f2(x, z):
    return cos(x) * sin(z)


def f3(x, z):
    return exp(cos(x) * sin(z))


def f4(x, z):
    return sin(x * z)


def f5(x, z):
    return x * z


def f6(x, z):
    a = (x - pi) ** 2 + (z - pi) ** 2
    return (1 / 5) * sin(x) * cos(z) - (3 / 2) * cos(7 * a / 4) * exp(-a)


funcs_module = {
    '(1 / 5) * sin(x) * cos(z) - (3 / 2) * cos(7 * a / 4) * exp(-a)': f6,
    'exp(cos(x) * sin(z))': f3,
    'sin(x * z)': f4,
    'x * z': f5,
    'sin(x) * cos(z / 2) + cos(x) * sin(z / 2)': f1,
    'cos(x) * sin(z)': f2
}
