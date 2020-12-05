#! /usr/bin/env python3

"""
sample.txt:
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.
"""

import sys

from typing import Set


def find_sum_to(entries: Set[int], limit: int) -> int:
    # if two entries in `entries` sum to `limit`, return their product
    for e in entries:
        if (limit - e) in entries:
            return e * (limit - e)

    return 0


def calc(content) -> int:
    entries = set(map(lambda e: int(e.strip()), content))
    for e in entries:
        result = find_sum_to(entries - {e}, 2020 - e)
        if result:
            return e * result

    return 0


def main():
    with open(sys.argv[1], "r") as f:
        content = f.readlines()

    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
