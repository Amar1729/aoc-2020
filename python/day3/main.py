#! /usr/bin/env python3

import sys
import functools


SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def calc(content, slope) -> int:
    nature = [line.strip() for line in content if line.strip()]

    x, y = slope
    width, height = len(nature[0]), len(nature)

    pos = 0
    trees = 0

    for i in range(0, height, y):
        if i > 0:
            if nature[i][pos] == "#":
                # nature[i][pos] = "X"
                nature[i] = nature[i][:pos] + "X" + nature[i][pos + 1:]
                trees += 1
            else:
                # nature[i][pos] = "O"
                nature[i] = nature[i][:pos] + "O" + nature[i][pos + 1:]

        pos = (pos + x) % width

    return trees


def main():
    with open(sys.argv[1], "r") as f:
        content = f.readlines()

    # result = calc(content)
    result = functools.reduce(lambda x, y: x * y, [calc(content, s) for s in SLOPES])
    print(result)


if __name__ == "__main__":
    main()
