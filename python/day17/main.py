#! /usr/bin/env python3

import collections
import sys

from typing import Tuple, Set


def compare(c: int, nc: Tuple[int, int]) -> Tuple[int, int]:
    if nc is None:
        nc = (c, c)
    else:
        nc = (min(c, nc[0]), (max(c, nc[1])))
    return nc


class Grid:
    def __init__(self, initial):
        self.x = (0, 0)
        self.y = (0, 0)
        self.z = (0, 0)

        self.points: Set[Tuple[int, int, int]] = set()
        for y, row in enumerate(initial):
            for x, c in enumerate(row.strip()):
                if c == "#":
                    self.points.update([(x, y, 0)])
                    self.update_bounds(x, y, 0)

    def __str__(self):
        points = sorted(list(self.points), key=lambda p: p[2])
        return str(points)

    def update_bounds(self, x, y, z):
        # set bounds so we don't have to query points every time
        self.x = (min(x, self.x[0]), max(x, self.x[1]))
        self.y = (min(y, self.y[0]), max(y, self.y[1]))
        self.z = (min(z, self.z[0]), max(z, self.z[1]))

    def neighbors(self, coord):
        def diff(a, a1) -> bool:
            return a in range(a1 - 1, a1 + 2)

        for p in self.points:
            if all(diff(p1, c1) for p1, c1 in zip(p, coord)):
                if not all(p1 == c1 for p1, c1 in zip(p, coord)):
                    yield p

    def step(self):
        # check every point within 1 index of bounds to check whether its state should change
        new_points = set()

        xr = range(self.x[0] - 1, self.x[1] + 2)
        yr = range(self.y[0] - 1, self.y[1] + 2)
        zr = range(self.z[0] - 1, self.z[1] + 2)

        nc = [None] * 3

        for x in xr:
            for y in yr:
                for z in zr:
                    nb = list(self.neighbors((x, y, z)))
                    if (x, y, z) in self.points:
                        if len(nb) in [2, 3]:
                            new_points.update([(x, y, z)])
                            # self.update_bounds(x, y, z)
                            nc[0] = compare(x, nc[0])
                            nc[1] = compare(y, nc[1])
                            nc[2] = compare(z, nc[2])
                    else:
                        if len(nb) == 3:
                            new_points.update([(x, y, z)])
                            # self.update_bounds(x, y, z)
                            nc[0] = compare(x, nc[0])
                            nc[1] = compare(y, nc[1])
                            nc[2] = compare(z, nc[2])

        self.points = new_points
        self.x = nc[0]
        self.y = nc[1]
        self.z = nc[2]


def p1(content):
    grid = Grid(content)

    for i in range(6):
        print(f"Step: {i} ...")
        grid.step()

    return len(grid.points)


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
