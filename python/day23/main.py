#! /usr/bin/env python3

import itertools
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


def p2(content) -> int:
    # ### ---- initialization work ----

    # cups: cups[label] = label of next cup (clockwise)
    cups = [0] * 1_000_001

    # similar to `cups`, but for finding the previous (lower label) cup
    prev_cups = [0] * 1_000_001

    cup_values = list(map(int, list(content[0])))
    curr = cup_values[0]

    a, b = itertools.tee(
        itertools.chain(
            cup_values,
            range(len(cup_values) + 1, 1_000_001),
        )
    )
    next(b)
    for idx, (c1, c2) in enumerate(zip(a, b)):
        cups[c1] = c2
        if idx > len(cup_values):
            prev_cups[idx] = idx - 2
    cups[c2] = cup_values[0]

    for _ in range(2):
        idx += 1
        prev_cups[idx] = idx - 2

    for i in itertools.chain(cups[1:len(cup_values) + 1], [cups[-1]]):
        prev_cups[i] = 10 ** 6 - 1 if i == 1 else cups.index(i - 1)

    # ### ---- helper functions ----

    def find_target(c: int) -> int:
        target_idx = prev_cups[c]
        while cups[target_idx] in to_del:
            target_idx = prev_cups[cups[target_idx]]
        return target_idx

    def safe_inc(x: int) -> int:
        return x + 1 if x < 10 ** 6 else 1

    # ### ---- do stuff ----

    for counter in range(10 ** 7):
        to_del = [cups[curr]]
        for _ in range(2):
            to_del.append(cups[to_del[-1]])

        target = find_target(curr)

        x, y, z, w = cups[curr], cups[to_del[-1]], cups[cups[target]], cups[target]

        # modify our index -> next cup mapping
        cups[curr] = y  # curr -> after-last-pick
        cups[to_del[-1]] = z  # last-pick -> after-target
        cups[w] = x  # target -> first-pick

        # modify index -> prev cup mapping
        prev_cups[safe_inc(y)] = curr
        prev_cups[safe_inc(z)] = to_del[-1]
        prev_cups[safe_inc(x)] = w

        curr = cups[curr]

    return cups[1] * cups[cups[1]]


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
