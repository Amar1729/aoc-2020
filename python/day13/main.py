#! /usr/bin/env python3

import sys
from functools import reduce


def p1(content) -> int:
    start_time = timestamp = int(content[0])
    buses = sorted(map(int, filter(lambda e: e != "x", content[1].split(","))))

    # naively check multiples (i'm sure p2 will require us to optimize this)

    while True:
        for bus in buses:
            if timestamp % bus == 0:
                return bus * (timestamp - start_time)
        timestamp += 1


def e_gcd(a, b):
    ra, r = a, b
    sa, s = 1, 0
    ta, t = 0, 1

    while r != 0:
        q = ra // r
        ra, r = r, ra - q * r
        sa, s = s, sa - q * s
        ta, t = t, ta - q * t

    return sa, ta


def p2(content) -> int:
    buses = filter(
        lambda e: isinstance(e[1], int),
        map(
            lambda i: i if i[1] == "x" else (-i[0], int(i[1])),
            enumerate(content[1].split(",")),
        ),
    )

    def _fold(a1, n1, a2, n2):
        m1, m2 = e_gcd(n1, n2)
        x = (a1 % n1) * m2 * n2 + (a2 % n2) * m1 * n1
        N = n1 * n2
        return x % N, N

    return reduce(lambda x, y: _fold(*x, *y), buses)[0]


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
