#! /usr/bin/env python3

import collections
import sys

WIDTH = 25


def p1(content):
    numbers = list(map(int, content))
    d = collections.deque(numbers[:WIDTH], maxlen=WIDTH)

    def check_correct(j) -> False:
        for x in d:
            if j - x in d:
                return True
        return False

    for n in numbers[WIDTH:]:
        if check_correct(n):
            d.append(n)
        else:
            return n


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
