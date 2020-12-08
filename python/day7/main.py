#! /usr/bin/env python3

import re
import sys


class Bag:
    def __init__(self, rule):
        _col = re.match(r"(\w+ \w+) bags", rule)
        assert _col is not None
        self.color = _col.group(1)

        def parse_child(child):
            num, *_color = child.split(" ")
            return " ".join(_color), int(num)

        self.children = dict(map(parse_child, re.findall(r"(\d+ \w+ \w+) bag", rule)))


def calc(content) -> int:
    bags = list(map(Bag, content))

    def find_parents(color):
        return list(map(lambda b: b.color, filter(lambda b: color in b.children, bags)))

    visited = set()
    parents = find_parents("shiny gold")
    while parents:
        intermediate = parents.pop(0)
        visited.update([intermediate])
        [parents.append(p) for p in find_parents(intermediate) if p not in visited]

    return len(visited)


def p2(content) -> int:
    rules = list(map(Bag, content))
    counts = {b.color: 0 for b in rules}

    def bag_count(color) -> int:
        if counts[color]:
            return counts[color]
        else:
            bag = next(filter(lambda b: color == b.color, rules))
            if not bag.children:
                counts[bag.color] = 0
                return counts[bag.color]
            else:
                counts[color] = sum(quant * (1 + bag_count(col)) for col, quant in bag.children.items())
                return counts[color]

    return bag_count("shiny gold")


def main():
    with open(sys.argv[1], "r") as f:
        content = f.readlines()

    result = p2(content)
    print(result)


if __name__ == "__main__":
    main()
