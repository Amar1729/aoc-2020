#! /usr/bin/env python3

import sys


def calc(content) -> int:
    groups = [set(group.replace("\n", "")) for group in content]
    return sum([len(g) for g in groups])


def main():
    with open(sys.argv[1], "r") as f:
        _content = f.read()

    content = _content.split("\n\n")
    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
