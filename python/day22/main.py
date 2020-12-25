#! /usr/bin/env python3

import copy
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


def game(deck1, deck2, depth=1) -> int:
    """ 0 if p1 wins, 1 if p2 wins """
    deck_states = []

    while deck1 and deck2:
        if (deck1, deck2) in deck_states:
            return 0
        else:
            deck_states.append((copy.copy(deck1), copy.copy(deck2)))

        d1 = deck1[0]
        d2 = deck2[0]

        if d1 <= len(deck1) - 1 and d2 <= len(deck2) - 1:
            winner = game(deck1[1:d1 + 1], deck2[1:d2 + 1], depth + 1)
            if winner == 0:
                deck1.append(deck1.pop(0))
                deck1.append(deck2.pop(0))
            else:
                deck2.append(deck2.pop(0))
                deck2.append(deck1.pop(0))
        else:
            if d1 > d2:
                deck1.append(deck1.pop(0))
                deck1.append(deck2.pop(0))
            else:
                deck2.append(deck2.pop(0))
                deck2.append(deck1.pop(0))

    return 0 if deck1 else 1


def p2(content):
    deck1, deck2 = parse(content)

    game(deck1, deck2)

    return score(deck1) if deck1 else score(deck2)


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
