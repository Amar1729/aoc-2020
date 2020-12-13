#! /usr/bin/env python3

import sys


def p1(content) -> int:
    start_time = timestamp = int(content[0])
    buses = sorted(map(int, filter(lambda e: e != "x", content[1].split(","))))

    # naively check multiples (i'm sure p2 will require us to optimize this)

    while True:
        for bus in buses:
            if timestamp % bus == 0:
                return bus * (timestamp - start_time)
        timestamp += 1


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
