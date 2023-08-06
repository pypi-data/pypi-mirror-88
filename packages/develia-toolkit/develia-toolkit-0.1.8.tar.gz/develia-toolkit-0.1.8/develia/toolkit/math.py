import math
import typing


def lerp(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def extrema(array) -> typing.Tuple[typing.Any, typing.Any]:
    min_ = None
    max_ = None

    for item in array:
        if min_ is None or item < min_:
            min_ = item

        if max_ is None or item > max_:
            max_ = item

    return min_, max_


def round_up(number: float, decimals: int) -> float:
    factor = 10 ** decimals
    return math.ceil(number * factor) / factor


def round_down(number: float, decimals: int) -> float:
    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def constrain(x, min, max):
    if x < min:
        return min
    if x > max:
        return max
    return x
