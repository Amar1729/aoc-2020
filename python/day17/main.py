#! /usr/bin/env python3

import sys
import time

from typing import List, Optional, Tuple, Set, Union


P3 = Tuple[int, int, int]
P4 = Tuple[int, int, int, int]

D3 = Union[Set[P3], List[P3]]
D4 = Union[Set[P4], List[P4]]


def compare(c: int, nc: Optional[Tuple[int, int]]) -> Tuple[int, int]:
    if nc is None:
        nc = (c, c)
    else:
        nc = (min(c, nc[0]), (max(c, nc[1])))
    return nc


def graph(points: Union[D3, D4]) -> str:
    x = max(p[0] for p in points)
    y = max(p[1] for p in points)

    grid = [["." for _ in range(x + 1)] for _ in range(y + 1)]
    for x, y, *_ in points:
        grid[y][x] = "#"

    while True:
        if all(c == "." for c in grid[0]):
            grid.pop(0)
        elif all(c == "." for c in grid[-1]):
            grid.pop(len(grid) - 1)
        elif all(c[0] == "." for c in zip(grid)):
            for y in range(len(grid)):
                grid[y].pop(0)
        else:
            break

    return "\n".join("".join(row) for row in grid)


class Grid:
    def __init__(self, initial):
        self.x = (0, 0)
        self.y = (0, 0)
        self.z = (0, 0)
        self.w = (0, 0)

        self.points: Set[Tuple[int, int, int, int]] = set()
        for y, row in enumerate(initial):
            for x, c in enumerate(row.strip()):
                if c == "#":
                    self.points.update([(x, y, 0, 0)])
                    self.update_bounds(x, y, 0, 0)

    def __str__(self):
        zr = sorted(list(set(map(lambda p: p[2], self.points))))
        wr = sorted(list(set(map(lambda p: p[3], self.points))))

        st = ""
        for w in wr:
            for z in zr:
                points = list(filter(lambda p: p[2] == z and p[3] == w, self.points))
                # print(points)
                st += f"z={z}, w={w}\n"
                # st += str(points) + "\n"
                st += graph(points) + "\n"
            st += "\n"
        return st

        # points = sorted(list(self.points), key=lambda p: p[2])
        # return str(points)

    def update_bounds(self, x, y, z, w):
        # set bounds so we don't have to query points every time
        self.x = (min(x, self.x[0]), max(x, self.x[1]))
        self.y = (min(y, self.y[0]), max(y, self.y[1]))
        self.z = (min(z, self.z[0]), max(z, self.z[1]))
        self.w = (min(w, self.w[0]), max(w, self.w[1]))

    def neighbors(self, coord: Tuple[int, int, int, int]):
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
        wr = range(self.w[0] - 1, self.w[1] + 2)

        nc = [None] * 4

        for x in xr:
            for y in yr:
                for z in zr:
                    for w in wr:
                        nb = list(self.neighbors((x, y, z, w)))
                        if (x, y, z, w) in self.points:
                            if len(nb) in [2, 3]:
                                new_points.update([(x, y, z, w)])
                                # self.update_bounds(x, y, z)
                                nc[0] = compare(x, nc[0])
                                nc[1] = compare(y, nc[1])
                                nc[2] = compare(z, nc[2])
                                nc[3] = compare(w, nc[3])
                        else:
                            if len(nb) == 3:
                                new_points.update([(x, y, z, w)])
                                # self.update_bounds(x, y, z)
                                nc[0] = compare(x, nc[0])
                                nc[1] = compare(y, nc[1])
                                nc[2] = compare(z, nc[2])
                                nc[3] = compare(w, nc[3])

        self.points = new_points
        self.x = nc[0]
        self.y = nc[1]
        self.z = nc[2]
        self.w = nc[3]


def p1(content):
    grid = Grid(content)

    print(grid)

    for i in range(6):
        s = time.time()
        grid.step()
        print(f"Step: {i+1}: {time.time() - s}")
        print(f"({len(grid.points)})")
        # print(grid)

    return len(grid.points)


def p2(content):
    # made all p2 changes in Grid object
    return p1(content)


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
