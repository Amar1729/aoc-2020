#! /usr/bin/env python3

import copy
import sys


def p1(content):
    counter = 0
    accumulator = 0
    states = set()

    while True:
        try:
            inst, offset = content[counter].split(" ")
        except IndexError:
            return accumulator, True

        if counter in states:
            return accumulator, False

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
    for bad_inst, _ in filter(lambda i: i[1].split(" ")[0] in ["nop", "jmp"], enumerate(content)):
        modified = copy.copy(content)
        if "nop" in modified[bad_inst]:
            modified[bad_inst] = modified[bad_inst].replace("nop", "jmp")
        elif "jmp" in modified[bad_inst]:
            modified[bad_inst] = modified[bad_inst].replace("jmp", "nop")

        result, status = p1(modified)
        if status:
            return result

    raise ValueError("terminating program not found?")


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
