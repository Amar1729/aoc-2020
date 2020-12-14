#! /usr/bin/env python3

import collections
import itertools
import re
import sys


def bitmask(value: str, mask: str) -> int:
    return int(
        "".join(map(lambda x: x[0] if x[1] == "X" else x[1], zip(value, mask))), 2
    )


def bitmask_p2(reg: str, mask: str):
    masked = "".join(map(lambda x: x[0] if x[1] == "0" else x[1], zip(reg, mask)))

    floating = list(map(lambda x: x[0], filter(lambda x: x[1] == 'X', enumerate(masked))))

    if floating:
        for digits in itertools.product([0, 1], repeat=len(floating)):
            s = masked
            for digit in digits:
                s = s.replace("X", str(digit), 1)
            yield s
    else:
        yield masked


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
    mem = collections.defaultdict(int)

    mask = ""

    for line in content:
        instruction, value = line.split(" = ")

        if instruction == "mask":
            mask = value
        else:
            reg = int(re.search(r"\d+", instruction).group())
            for masked_reg in bitmask_p2(f"{reg:0>36b}", mask):
                mem[int(masked_reg, 2)] = int(value)

    return sum(mem.values())


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
