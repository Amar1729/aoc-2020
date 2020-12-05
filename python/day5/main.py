#! /usr/bin/env python3

import itertools
import sys


def convert(s: str) -> int:
    s = s.replace("F", "0")
    s = s.replace("B", "1")

    s = s.replace("L", "0")
    s = s.replace("R", "1")

    return int(s, 2)


def calc(content) -> int:
    seats = sorted(map(convert, content))

    # see itertools: pairwise
    a, b = itertools.tee(iter(seats))
    next(b, None)
    for x, y in zip(a, b):
        if y - x == 2:
            return y - 1

    return 0


def main():
    with open(sys.argv[1], "r") as f:
        content = f.readlines()

    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
