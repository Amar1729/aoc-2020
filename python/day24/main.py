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


def p1(content, p2=False):
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

    # return the points set for our p2 work
    return len(points) if not p2 else points


def p2(content):
    points = p1(content, True)

    def yield_adj(p):
        """ yield all adjacent points to p """
        yield (p[0] + 1, p[1])
        yield (p[0], p[1] - 1)
        yield (p[0] - 1, p[1] - 1)
        yield (p[0] - 1, p[1])
        yield (p[0] + 1, p[1] + 1)
        yield (p[0], p[1] + 1)

    def check_adj(p) -> int:
        """ return number of adjacent black tiles """
        return sum(_p in points for _p in yield_adj(p))

    for i in range(100):
        new_points = set()
        already_white = set()

        for point in points:
            adj_black = 0
            for _point in yield_adj(point):
                if _point in points:
                    adj_black += 1
                else:
                    if _point not in already_white:
                        already_white.add(_point)
                        if check_adj(_point) == 2:
                            new_points.add(_point)

            if adj_black in [1, 2]:
                new_points.add(point)

        points = new_points
        # print(f"Day {i+1}: {len(points)}")

    return len(points)


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
