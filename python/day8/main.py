#! /usr/bin/env python3

import sys


def p1(content):
    counter = 0
    accumulator = 0
    states = set()

    while True:
        inst, offset = content[counter].split(" ")

        if counter in states:
            return accumulator

        if inst == "nop":
            states.add(counter)
            counter += 1
        elif inst == "acc":
            accumulator += int(offset)
            states.add(counter)
            counter += 1
        elif inst == "jmp":
            states.add(counter)
            counter = counter + int(offset)


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
