#! /usr/bin/env python3

import collections
import re
import sys


def bitmask(value: str, mask: str) -> int:
    return int(
        "".join(map(lambda x: x[0] if x[1] == "X" else x[1], zip(value, mask))), 2
    )


def p1(content) -> int:
    mem = collections.defaultdict(int)

    mask = ""

    for line in content:
        instruction, value = line.split(" = ")

        if instruction == "mask":
            mask = value
        else:
            reg = int(re.search(r'\d+', instruction).group())
            value = f"{int(value):0>36b}"
            mem[reg] = bitmask(value, mask)

    return sum(mem.values())


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
