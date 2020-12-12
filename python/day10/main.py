#! /usr/bin/env python3

import itertools
import sys


def pairwise(itr):
    a, b = itertools.tee(iter(itr))
    next(b, None)
    for e in zip(a, b):
        yield e


def p1(content) -> int:
    adapters = sorted(list(map(int, content)))

    count_1 = 0
    count_3 = 0
    for x, y in pairwise(adapters):
        if y - x == 1:
            count_1 += 1
        elif y - x == 3:
            count_3 += 1
        elif y - x > 3:
            # not large a gap between adapters
            raise Exception

    if adapters[0] == 1:
        count_1 += 1
    elif adapters[0] == 3:
        count_3 += 1

    count_3 += 1

    return count_1 * count_3


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
