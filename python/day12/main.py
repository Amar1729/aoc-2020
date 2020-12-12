#! /usr/bin/env python3

import sys


def p1(content):
    x, y = 0, 0
    facing = 0

    for instruction in content:
        direction, value = instruction[0], int(instruction[1:])

        if direction == "N":
            y += value
        elif direction == "S":
            y -= value
        elif direction == "W":
            x -= value
        elif direction == "E":
            x += value
        elif direction == "L":
            facing = (facing + value) % 360
        elif direction == "R":
            facing = (facing - value) % 360
        elif direction == "F":
            if facing == 0:
                x += value
            elif facing == 90:
                y += value
            elif facing == 180:
                x -= value
            elif facing == 270:
                y -= value
            else:
                raise Exception
        else:
            raise Exception

    return abs(x) + abs(y)


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
