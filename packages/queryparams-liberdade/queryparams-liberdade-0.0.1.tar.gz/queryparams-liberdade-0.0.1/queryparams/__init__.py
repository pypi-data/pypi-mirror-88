from re import compile


def include(obj, keys, value):
    key = keys[0]

    if key not in obj:
        obj[key] = dict()

    if len(keys) > 1:
        to_include = include(obj[key], keys[1:], value)
        obj[key] = to_include
    else:
        obj[key] = value

    return obj


def parse(indexes):
    obj = {}
    split_brackets_regex = compile("[\[\]]")

    for key, value in indexes.items():
        keys = [k for k in split_brackets_regex.split(key) if k != '']
        obj = include(obj, keys, value)

    return obj


if __name__ == '__main__':
    pass
