#! /usr/bin/env python3

import sys


def calc(content) -> int:
    nature = [line.strip() for line in content if line.strip()]

    width, height = len(nature[0]), len(nature)

    pos = 0
    trees = 0

    for i in range(height):
        if i > 0:
            if nature[i][pos] == "#":
                # nature[i][pos] = "X"
                nature[i] = nature[i][:pos] + "X" + nature[i][pos + 1:]
                trees += 1
            else:
                # nature[i][pos] = "O"
                nature[i] = nature[i][:pos] + "O" + nature[i][pos + 1:]

        pos = (pos + 3) % width

    return trees


def main():
    with open(sys.argv[1], "r") as f:
        content = f.readlines()

    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
