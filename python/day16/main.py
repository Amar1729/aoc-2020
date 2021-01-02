#! /usr/bin/env python3

import collections
import sys

from functools import reduce


def parse_ticket(line: str):
    return list(map(int, line.split(",")))


def parse(content, p1=True):
    ordered = []

    idx = 0
    while True:
        line = content[idx]
        idx += 1
        if not line.strip():
            break

        field, value = line.split(": ")

        valid = []
        for _r in value.split(" or "):
            start, stop = map(int, _r.split("-"))
            valid.append(range(start, stop + 1))

        ordered.append((field, valid))

    idx += 1
    my_ticket = parse_ticket(content[idx])

    idx += 3
    tickets = [parse_ticket(line) for line in content[idx:]]

    valid_values = set()
    for _, v in ordered:
        for r in v:
            valid_values.update(r)

    if p1:
        return sum(
            v for ticket in tickets
            for v in ticket
            if v not in valid_values
        )

    good_tickets = list(filter(
        lambda t: all(v in valid_values for v in t),
        tickets
    ))

    return my_ticket, good_tickets, ordered


def p1(content):
    return parse(content)


def p2(content):
    my_ticket, good_tickets, ordered = parse(content, False)
    fields = dict(ordered)

    # key -> index of ticket column
    # value -> set of indexes of `ordered` that column might be
    good_indexes = collections.defaultdict(set)

    columns = {
        ct: set(list(zip(*good_tickets))[ct])
        for ct in range(len(my_ticket))
    }

    for ct in range(len(my_ticket)):
        for fi, (_, valid) in enumerate(ordered):
            if all(x in valid[0] or x in valid[1] for x in columns[ct]):
                good_indexes[ct].add(fi)

    determined = [0] * len(ordered)

    # assumes every index can be determined from reducing possibilities from prior knowledge
    # (i.e. no searching/guessing necessary)
    while good_indexes:
        for i, s in good_indexes.items():
            if len(s) == 1:
                determined[i] = s.pop()
                break

        keys_to_delete = []
        for k in good_indexes:
            if determined[i] in good_indexes[k]:
                good_indexes[k].remove(determined[i])
            if not good_indexes[k]:
                keys_to_delete.append(k)

        for k in keys_to_delete:
            del good_indexes[k]

    reordered_fields = {idx: ordered[p][0] for idx, p in enumerate(determined)}

    for ticket in good_tickets:
        for i, v in enumerate(ticket):
            valid = fields[reordered_fields[i]]
            assert v in valid[0] or v in valid[1]

    return reduce(
        lambda x, y: x * y,
        (
            my_ticket[p]
            for p, i in reordered_fields.items()
            if i.startswith("departure")
        ),
        1,
    )


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
