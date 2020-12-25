#! /usr/bin/env python3

import sys


def p1(content):
    cups = list(map(int, list(content[0])))

    def step(idx):
        curr = cups[idx]

        picked = []
        for _ in range(3):
            try:
                picked.append(cups.pop(idx + 1))
            except IndexError:
                picked.append(cups.pop(0))

        # incurs sorting every run, not good
        sc = sorted(cups)
        target_cup = sc[sc.index(curr) - 1]
        target = cups.index(target_cup)

        for p in picked[::-1]:
            cups.insert(target + 1, p)

        return (cups.index(curr) + 1) % len(cups)

    idx = 0
    for _ in range(100):
        idx = step(idx)

        # print(" ".join(list(map(lambda p: f"({p[1]})" if p[0] == idx else str(p[1]), enumerate(cups)))))
        # print()

    one = cups.index(1)
    st = ""
    for i in range(1, len(cups)):
        st += str(cups[(one + i) % len(cups)])
    return st


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
