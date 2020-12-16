#! /usr/bin/env python3

import sys


def parse_ticket(line: str):
    return list(map(int, line.split(",")))


def p1(content):
    valid_values = set()

    idx = 0
    while True:
        line = content[idx]
        idx += 1
        if not line.strip():
            break

        field, value = line.split(": ")

        for _r in value.split(" or "):
            start, stop = map(int, _r.split("-"))
            valid_values.update(list(range(start, stop + 1)))

    idx += 1
    # my_ticket = parse_ticket(content[idx])

    idx += 3
    tickets = [parse_ticket(line) for line in content[idx:]]

    error = sum(
        v for ticket in tickets
        for v in ticket
        if v not in valid_values
    )

    return error


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
