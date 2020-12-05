#! /usr/bin/env python3

import sys


def is_valid(pw: str, policy: str) -> bool:
    _range, letter = policy.split(" ")
    s = set(map(lambda x: pw[int(x) - 1], _range.split("-")))

    if len(s) == 2 and letter in s:
        return True

    return False


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
