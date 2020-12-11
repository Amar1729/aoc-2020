#! /usr/bin/env python3

import sys

from typing import List


class Map:
    def __init__(self, layout):
        self.layout = list(map(lambda l: l.strip(), layout))

        self.wth = len(self.layout[0])
        self.hgt = len(self.layout)

    def __hash__(self):
        return hash("".join(self.layout))

    def _surrounding(self, x, y, seat):
        """ check for surrounding seats of type `seat` around x, y """
        tot = 0

        up = y - 1
        down = y + 1
        left = x - 1
        right = x + 1

        if up >= 0:
            if left >= 0:
                if self.layout[up][left] == seat:
                    tot += 1
            if self.layout[up][x] == seat:
                tot += 1
            if right < self.wth:
                if self.layout[up][right] == seat:
                    tot += 1

        if left >= 0:
            if self.layout[y][left] == seat:
                tot += 1

        if right < self.wth:
            if self.layout[y][right] == seat:
                tot += 1

        if down < self.hgt:
            if left >= 0:
                if self.layout[down][left] == seat:
                    tot += 1
            if self.layout[down][x] == seat:
                tot += 1
            if right < self.wth:
                if self.layout[down][right] == seat:
                    tot += 1

        return tot

    def step(self):
        """ build next step for the layout """
        new_layout: List[str] = []
        for y in range(self.hgt):
            new_row = ""
            for x in range(self.wth):
                curr = self.layout[y][x]

                if curr == ".":
                    new_row += curr
                elif curr == "L":
                    new_row += "#" if self._surrounding(x, y, "#") == 0 else "L"
                elif curr == "#":
                    new_row += "L" if self._surrounding(x, y, "#") >= 4 else "#"

            new_layout.append(new_row)

        self.layout = new_layout

    def occupied(self) -> int:
        return sum(
            seat == "#"
            for row in self.layout
            for seat in row
        )


def p1(content) -> int:
    layout = Map(content)
    prev = hash(layout)

    while True:
        layout.step()

        if hash(layout) == prev:
            return layout.occupied()

        prev = hash(layout)


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
