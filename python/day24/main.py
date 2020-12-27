#! /usr/bin/env python3

import sys


def parse_directions(s):
    sd = list(s)
    dirs = []
    while sd:
        if sd[0] in "ew":
            dirs.append(sd.pop(0))
        elif sd[0] in "ns":
            dirs.append("".join([sd.pop(0), sd.pop(0)]))
    return dirs


def p1(content):
    dirs = list(map(parse_directions, content))
    points = set()

    dmap = {
        "e": (1, 0),
        "se": (0, -1),
        "sw": (-1, -1),
        "w": (-1, 0),
        "ne": (1, 1),
        "nw": (0, 1),
    }

    for d in dirs:
        p = (0, 0)
        for t in d:
            np = dmap[t]
            p = (p[0] + np[0], p[1] + np[1])

        if p in points:
            # print(f"removing: {p}")
            points.remove(p)
        else:
            # print(f"adding: {p}")
            points.add(p)

    return len(points)


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
