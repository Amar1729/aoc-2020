#! /usr/bin/env python3

import sys


def parse(content):
    deck1 = []
    deck2 = []

    c = 1
    while True:
        if content[c].strip():
            deck1.append(int(content[c]))
            c += 1
        else:
            c += 2
            break

    while True:
        if c < len(content) and content[c].strip():
            deck2.append(int(content[c]))
            c += 1
        else:
            c += 1
            break

    return deck1, deck2


def score(deck) -> int:
    return sum((idx + 1) * v for idx, v in enumerate(deck[::-1]))


def p1(content):
    deck1, deck2 = parse(content)

    def round():
        if deck1[0] > deck2[0]:
            deck1.append(deck1.pop(0))
            deck1.append(deck2.pop(0))
        else:
            deck2.append(deck2.pop(0))
            deck2.append(deck1.pop(0))

    while deck1 and deck2:
        round()

    return score(deck1) if deck1 else score(deck2)


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
