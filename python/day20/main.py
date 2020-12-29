#! /usr/bin/env python3

import collections
import copy
import functools
import itertools
import sys

from typing import Dict, List


SEA1 = "                  # "
SEA2 = "#    ##    ##    ###"
SEA3 = " #  #  #  #  #  #   "


class Tile:
    def __init__(self, number, layout):
        self.number = number
        assert isinstance(layout, list)
        assert all(isinstance(s, str) for s in layout)
        self.layout = [line.strip() for line in layout]

        # original orientation (changes upon mirroing / rotations)
        self.orientation = (0, 0)

    def __str__(self):
        # return f"{self.number} {self.orientation}\n" + "\n".join("".join(list(row)) for row in self.layout)
        return "\n".join("".join(list(row)) for row in self.layout)

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
        self.layout = ["".join(row[::-1]) for row in zip(*self.layout)]
        self.orientation = (self.orientation[0], (self.orientation[1] + 1) % 4)

    def mirror_x(self):
        """ Flips the grid across the x axis """
        self.layout = self.layout[::-1]
        self.orientation = ((self.orientation[0] ^ 1), self.orientation[1])

    def set_orientation(self, flipped: int, rotation: int):
        if flipped ^ self.orientation[0]:
            self.mirror_x()

        while self.orientation[1] != rotation:
            self.rotate()

    def remove_bounds(self):
        self.layout = [row[1:-1] for row in self.layout[1:-1]]

    def add_sea_monster(self, x, y, monster):
        row = self.layout[y]

        assert len(monster) <= len(row[x:])

        self.layout[y] = "".join([
            row[:x],
            "".join([
                "O" if y == "#" else x
                for x, y in itertools.zip_longest(row[x:], monster, fillvalue=" ")
            ]),
            # row[x + len(monster):],
        ])

    def roughness(self) -> int:
        return sum(sum(x == "#" for x in row) for row in self.layout)


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


def p1(content, p2=False):
    tiles = parse_input(content)
    tiles_sorted = sorted(tiles.items(), key=lambda p: p[0])

    matches = collections.defaultdict(set)

    def append_match(t1i, t2i, direction):
        t1 = tiles[t1i]
        t2 = tiles[t2i]
        t = (t1.orientation, t2.orientation, direction, t1.matches(direction, t2))
        matches[(t1i, t2i)].add(t)

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

    if p2:
        return tiles, matches

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


def yield_adj(x: int, y: int, _l: int):
    if y > 0:
        yield "up", x, y - 1
    if x > 0:
        yield "left", x - 1, y
    if x < _l - 1:
        yield "right", x + 1, y
    if y < _l - 1:
        yield "down", x, y + 1


def inverse(d: str) -> str:
    mapping = {
        "up": "down",
        "left": "right",
        "down": "up",
        "right": "left",
    }
    return mapping[d]


def line_matches_monster(s: str, sea_body: str, start: int = -1):
    if start >= 0:
        if all(map(lambda p: p[1] != "#" or (p[1] == "#" and p[0] in "O#"), zip(s[start:], sea_body))):
            yield start
        return

    for start in range(len(s) - len(sea_body) + 1):
        if all(map(lambda p: p[1] != "#" or (p[1] == "#" and p[0] in "O#"), zip(s[start:], sea_body))):
            yield start


def p2(content):
    # generate grid from the fast matches p1 gives us
    tiles, matches = p1(content, True)

    match_pointers = collections.defaultdict(set)

    for (t1i, t2i), sl in sorted(matches.items(), key=lambda p: p[0][1]):
        for t1o, t2o, d, b in sl:
            if b:
                match_pointers[t1i].add(t2i)
                match_pointers[t2i].add(t1i)

    _l = int(len(match_pointers) ** 0.5)
    grid = [[0 for _ in range(_l)] for _ in range(_l)]

    def find(lm):
        return next(filter(lm, match_pointers.items()))

    # ### ---- place the tiles in the grid ----
    for x in range(_l):
        for y in range(_l):
            curr = grid[y][x]

            if (x, y) == (0, 0):
                next_tile, neighbors = find(lambda e: len(e[1]) == 2)
                grid[y][x] = next_tile
                g = iter(neighbors)
                grid[y + 1][x] = next(g)
                grid[y][x + 1] = next(g)
            elif (x, y) == (_l - 1, 0):
                # top-right corner
                prev = grid[y][x - 1]
                next_tile = (match_pointers[curr] ^ set([prev])).pop()
                grid[y + 1][x] = next_tile
            elif (x, y) == (0, _l - 1):
                # bottom-left corner
                prev = grid[y - 1][x]

                next_tile = (match_pointers[curr] ^ set([prev])).pop()
                grid[y][x + 1] = next_tile
            elif (x, y) == (_l - 1, _l - 1):
                # everything should be done at this point
                pass
            elif y == 0:
                # top edge
                prev = grid[y][x - 1]
                next_tile, neighbors = find(lambda e: curr in e[1] and len(e[1]) <= 3 and e[0] != prev)

                grid[y][x + 1] = next_tile
                adj_4 = (match_pointers[curr] ^ set([next_tile, prev])).pop()
                grid[y + 1][x] = adj_4
            elif x == 0:
                # left edge
                prev = grid[y - 1][x]
                next_tile, neighbors = find(lambda e: curr in e[1] and len(e[1]) <= 3 and e[0] != prev)

                grid[y + 1][x] = next_tile
                adj_4 = (match_pointers[curr] ^ set([next_tile, prev])).pop()
                grid[y][x + 1] = adj_4
            elif x == _l - 1:
                # right edge
                prev = grid[y - 1][x]
                next_tile, neighbors = find(lambda e: curr in e[1] and len(e[1]) <= 3 and e[0] != prev)

                grid[y + 1][x] = next_tile
                adj_4 = (match_pointers[curr] ^ set([next_tile, prev])).pop()
                # this should already be placed? right?
                assert grid[y][x - 1] == adj_4
            elif y == _l - 1:
                # bottom edge
                prev = grid[y][x - 1]
                next_tile, neighbors = find(lambda e: curr in e[1] and len(e[1]) <= 3 and e[0] != prev)

                grid[y][x + 1] = next_tile
                # this should already be placed? right?
                adj_4 = (match_pointers[curr] ^ set([next_tile, prev])).pop()
                assert grid[y - 1][x] == adj_4
            else:
                # 4-adj tiles
                upper = grid[y - 1][x]
                left = grid[y][x - 1]
                upper_left = grid[y - 1][x - 1]

                this_tile, _ = find(lambda e: upper in e[1] and left in e[1] and upper_left != e[0])

                grid[y][x] = this_tile

    # uses outer-scoped variable `tiles`
    def join_grid(dbg: bool = False) -> List[str]:
        ret = []
        for row in grid:
            row_tiles = [copy.deepcopy(tiles[tile_idx]) for tile_idx in row]
            if not dbg:
                list(map(lambda t: t.remove_bounds(), row_tiles))
            sep = " " if dbg else ""
            ret.extend([sep.join(tile_row) for tile_row in zip(*map(lambda t: t.layout, row_tiles))])
            if dbg:
                ret.append("")
        return ret

    permuted_matches = {}

    # ### ---- figure out correct orientations ----
    # optimizations for this loop -
    # abstract to function call, and return upon finding all orientations for one tile
    # the set intersect those to find the correct orientation
    # if the resulting set in length one, return and subsequently format our entire grid
    # according to that rule
    for x in range(_l):
        for y in range(_l):
            curr_tile = copy.deepcopy(tiles[grid[y][x]])

            if curr_tile.number not in permuted_matches:
                permuted_matches[curr_tile.number] = {}

            for d, nx, ny in yield_adj(x, y, _l):
                nt = tiles[grid[ny][nx]]
                if nt.number not in permuted_matches[curr_tile.number]:
                    permuted_matches[curr_tile.number][nt.number] = set()
                    s = permuted_matches[curr_tile.number][nt.number]

                    next_tile = copy.deepcopy(nt)

                    if nt.number not in permuted_matches:
                        permuted_matches[nt.number] = {}

                    if curr_tile.number not in permuted_matches[nt.number]:
                        permuted_matches[nt.number][curr_tile.number] = set()

                    s2 = permuted_matches[nt.number][curr_tile.number]

                    for _ in range(2):
                        for _ in range(4):

                            for _ in range(2):
                                for _ in range(4):

                                    if curr_tile.matches(d, next_tile):
                                        s.add((d, curr_tile.orientation, next_tile.orientation))
                                        s2.add((inverse(d), next_tile.orientation, curr_tile.orientation))

                                    next_tile.rotate()
                                next_tile.mirror_x()

                            curr_tile.rotate()
                        curr_tile.mirror_x()

    for tile_idx, other in permuted_matches.items():
        correct = set()
        for orientations in other.values():
            if not correct:
                correct = set([o[1] for o in orientations])
            else:
                correct &= set([o[1] for o in orientations])
        # print(tile_idx, correct)
        assert len(correct) == 1

        tiles[tile_idx].set_orientation(*correct.pop())

    final = Tile(0, join_grid())

    def find_monsters(tile: Tile):
        for idx in range(1, len(tile.layout) - 2):
            for m in line_matches_monster(tile.layout[idx], SEA2):
                for _ in line_matches_monster(tile.layout[idx - 1], SEA1, m):
                    for _ in line_matches_monster(tile.layout[idx + 1], SEA3, m):
                        yield idx, m

    for orientation in range(8):
        results = list(find_monsters(final))
        if not results:
            final.rotate()
            if orientation == 4:
                final.mirror_x()
        else:
            break

    for y, x in results:
        final.add_sea_monster(x, y - 1, SEA1)
        final.add_sea_monster(x, y, SEA2)
        final.add_sea_monster(x, y + 1, SEA3)

    return final.roughness()


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
