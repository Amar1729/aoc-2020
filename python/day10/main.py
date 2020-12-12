#! /usr/bin/env python3

import itertools
import sys

from typing import Dict


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


def p2(content) -> int:
    adapters = sorted(map(int, content))
    adapters = [0] + adapters

    # try calculating from the end first
    memo: Dict[int, int] = {}

    def recurse(i: int, prev) -> int:
        if i < 0:
            return 0

        if prev - adapters[i] > 3:
            return 0

        if i == 0:
            return 1

        # don't redo work - use memoization !
        if i in memo:
            return memo[i]

        prev = adapters[i]
        total = sum(recurse(i - x, prev) for x in reversed(range(1, 4)))
        memo[i] = total
        return total

    return recurse(len(adapters) - 1, adapters[-1] + 3)


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
