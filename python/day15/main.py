#! /usr/bin/env python3

import collections
import sys


def p1(content, length=2020) -> int:
    seed = list(map(int, content[0].split(",")))

    d = collections.defaultdict(list)

    prev = 0
    for idx, n in enumerate(seed):
        d[n].append(idx + 1)
        prev = n

    for idx in range(idx + 1, length):
        prev = 0 if len(d[prev]) < 2 else d[prev][-1] - d[prev][-2]
        d[prev].append(idx + 1)
        if len(d[prev]) > 2:
            d[prev].pop(0)

    return prev


def p2(content):
    return p1(content, 30000000)


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
