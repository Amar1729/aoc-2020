#! /usr/bin/env python3

import copy
import sys

from typing import Dict


class Rule:
    def __init__(self, content):
        addr, content = content.split(": ")
        self.addr = int(addr)

        self.literal = True if '"' in content else False

        if self.literal:
            self.content = content.strip('"')
        else:
            self.content = list(map(lambda g: list(map(int, g.split(" "))), content.split(" | ")))

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self)

    def parse(self, s: str, d: Dict[int, "Rule"], depth=0):
        if self.literal:
            if s[0] == self.content:
                return True, s[1:]
            else:
                return False, s
        else:
            old_s = s

            for immut_order in self.content:
                status = True
                order = copy.copy(immut_order)
                s = old_s
                while order and status and s.strip():
                    next_rule = d[order[0]]
                    status, s = next_rule.parse(s, d, depth+1)

                    if not status:
                        break

                    order.pop(0)

                if status and not order:
                    # successfully applied all the rules in 'order'
                    # print("-" * depth + f"{self.addr} -> {immut_order}")
                    assert len(s) < len(old_s)
                    return True, s

            return False, old_s


def p1(content):
    rules = {}

    c = 0
    while True:
        if c >= len(content):
            break

        if content[c].strip():
            rule = Rule(content[c].strip())
            rules[rule.addr] = rule
            c += 1
        else:
            c += 1
            break

    messages = content[c:]

    def valid(m: str) -> bool:
        if not m.strip():
            return False
        status, s = rules[0].parse(m, rules)
        if status and not s.strip():
            return True
        return False

    valid_messages = filter(lambda m: valid(m), messages)
    return len(list(valid_messages))


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
