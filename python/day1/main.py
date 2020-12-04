#! /usr/bin/env python3

"""
sample.txt:
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.
"""

import sys


def calc(content) -> int:
    entries = set(map(lambda e: int(e.strip()), content))

    for e in entries:
        if (2020 - e) in entries:
            return e * (2020 - e)

    return 0


def main():
    with open(sys.argv[1], "r") as f:
        content = f.readlines()

    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
