#! /usr/bin/env python3

import string
import sys


def calc(content) -> int:
    return sum(
        [
            sum(
                [
                    all(c in person for person in group.strip().split("\n"))
                    for c in string.ascii_lowercase
                ]
            )
            for group in content
        ]
    )


def main():
    with open(sys.argv[1], "r") as f:
        _content = f.read()

    content = _content.split("\n\n")
    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
