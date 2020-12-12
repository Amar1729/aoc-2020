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
    x, y = 0, 0

    # these coordinates are relative to the ship
    w_x, w_y = 10, 1

    for instruction in content:
        direction, value = instruction[0], int(instruction[1:])

        if direction == "N":
            w_y += value
        elif direction == "S":
            w_y -= value
        elif direction == "W":
            w_x -= value
        elif direction == "E":
            w_x += value
        elif direction == "L":
            # do steps by 90-degree turns
            for step in range(value // 90):
                w_x, w_y = -w_y, w_x
        elif direction == "R":
            # do steps by 90-degree turns
            for step in range(value // 90):
                w_x, w_y = w_y, -w_x
        elif direction == "F":
            x += value * w_x
            y += value * w_y
        else:
            raise Exception

    return abs(x) + abs(y)


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
