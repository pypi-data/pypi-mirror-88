def index_of_min(array):
    output = None
    min_ = None

    for index, item in enumerate(array):
        if output is None or item < min_:
            min_ = item
            output = index

    return output


def groupby(fn, array):
    keys = []
    values = []

    for item in array:
        key = fn(item)
        try:
            index = keys.index(key)
            values[index].append(item)
        except ValueError:
            keys.append(key)
            values.append([item])

    return {k: v for k, v in zip(keys, values)}


def index_of_max(array):
    output = None
    max_ = None

    for index, item in enumerate(array):
        if output is None or item > max_:
            max_ = item
            output = index

    return output


def last_index_of_min(array):
    output = None
    min_ = None

    for index, item in enumerate(array):
        if output is None or item <= min_:
            min_ = item
            output = index

    return output


def last_index_of_max(array):
    output = None
    max_ = None

    for index, item in enumerate(array):
        if output is None or item >= max_:
            max_ = item
            output = index

    return output
