#! /usr/bin/env python3

import collections
import functools
import sys

from typing import Dict, List


class Tile:
    def __init__(self, number, layout):
        self.number = number
        assert isinstance(layout, list)
        assert all(isinstance(s, str) for s in layout)
        self.layout = [line.strip() for line in layout]

        # original orientation (changes upon mirroing / rotations)
        self.orientation = (0, 0)

    def __str__(self):
        return f"{self.number} {self.orientation}\n" + "\n".join("".join(list(row)) for row in self.layout)

    def __repr__(self):
        return str(self)

    def column(self, c: int) -> str:
        return "".join(list(zip(*self.layout))[c])

    def matches(self, direction: str, tile: "Tile") -> bool:
        """ checks if `tile` `direction` of `self` matches up """
        if direction == "left":
            return all(t == o for t, o in zip(self.column(0), tile.column(-1)))
        elif direction == "right":
            return all(t == o for t, o in zip(self.column(-1), tile.column(0)))
        elif direction == "up":
            return all(t == o for t, o in zip(self.layout[0], tile.layout[-1]))
        elif direction == "down":
            return all(t == o for t, o in zip(self.layout[-1], tile.layout[0]))
        else:
            raise Exception

    def rotate(self):
        """ Rotate the grid by 90 deg clockwise """
        self.layout = [row[::-1] for row in zip(*self.layout)]
        self.orientation = (self.orientation[0], (self.orientation[1] + 1) % 4)

    def mirror_x(self):
        """ Flips the grid across the x axis """
        self.layout = self.layout[::-1]
        self.orientation = ((self.orientation[0] ^ 1), self.orientation[1])


def parse_input(content) -> Dict[int, Tile]:
    c = 0
    tiles = {}

    tile_num = 0
    tile_lines = []
    while c <= len(content):
        if c < len(content) and content[c].strip():
            if ":" in content[c]:
                tile_num = int(content[c].split(" ")[1].rstrip(":"))
            else:
                tile_lines.append(content[c])
        else:
            tile = Tile(tile_num, tile_lines)
            tiles[tile.number] = tile
            tile_num = 0
            tile_lines = []
        c += 1

    return tiles


def p1(content):
    tiles = parse_input(content)
    tiles_sorted = sorted(tiles.items(), key=lambda p: p[0])

    matches = collections.defaultdict(list)

    def append_match(t1i, t2i, direction):
        t1 = tiles[t1i]
        t2 = tiles[t2i]
        t = (t1.orientation, t2.orientation, direction, t1.matches(direction, t2))
        matches[(t1i, t2i)].append(t)

    for idx, (t1_idx, t1) in enumerate(tiles_sorted):
        for t2_idx, t2 in tiles_sorted[idx + 1:]:
            for direction in ["left", "right", "up", "down"]:
                # edit: this loop runs pretty quick, so who cares about optimization
                # the problem with this is that it doesn't keep track of already-checked orientations
                # between t1 / t2
                # t1.(0, 0), t2.(0, 0), left
                # same as
                # t1.(0, 1), t2.(0, 1), right
                for _ in range(2):
                    for _ in range(4):
                        append_match(t1_idx, t2_idx, direction)
                        t1.rotate()
                    t1.mirror_x()

    num_matches = collections.defaultdict(int)

    for (t1i, t2i), sl in sorted(matches.items(), key=lambda p: p[0][1]):
        for t1o, t2o, d, b in sl:
            if b:
                # print(f"{t2i} ({d} of) {t1i} : {t1o} {t2o}")
                num_matches[t1i] += 1
                num_matches[t2i] += 1

    corner_tiles = list(filter(lambda p: p[1] == 2, num_matches.items()))
    assert len(corner_tiles) == 4

    return functools.reduce(
        lambda x, y: x * y,
        (c[0] for c in corner_tiles),
        1,
    )


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
