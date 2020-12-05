#! /usr/bin/env python3

import sys


def is_valid(pw: str, policy: str) -> bool:
    _range, letter = policy.split(" ")
    lower, higher = map(int, _range.split("-"))

    return lower <= sum(map(lambda x: x == letter, pw)) <= higher


def calc(content) -> int:
    total = 0
    for line in content:
        policy, pw = line.split(": ")
        total += is_valid(pw, policy)
    return total


def main():
    with open(sys.argv[1], "r") as f:
        content = f.readlines()

    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
