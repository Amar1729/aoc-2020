#! /usr/bin/env python3

from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest

# pip install antlr4-python3-runtime
from antlr4 import CommonTokenStream, InputStream


class Rule:
    content: str | list[list[int]]

    def __init__(self, _content: str):
        addr, content = _content.split(": ")
        self.addr = int(addr)

        self.literal = '"' in content

        if self.literal:
            self.content = content.strip('"')
        else:
            self.content = list(map(lambda g: list(map(int, g.split(" "))), content.split(" | ")))

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self)

    def antlr(self) -> str:
        if isinstance(self.content, str):
            s = f"'{self.content}'"
        else:
            s = " | ".join([" ".join([f"g{i}" for i in order]) for order in self.content])
        return f"g{self.addr}: {s};"

    def parse(self, s: str, d: dict[int, Rule], depth=0):
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
                    status, s = next_rule.parse(s, d, depth + 1)

                    if not status:
                        break

                    order.pop(0)

                if status and not order:
                    # successfully applied all the rules in 'order'
                    # print("-" * depth + f"{self.addr} -> {immut_order}")
                    assert len(s) < len(old_s)
                    return True, s

            return False, old_s


def parse_rules(lines: list[str]) -> tuple[int, dict[int, Rule]]:
    rules = {}

    c = 0
    while True:
        if c >= len(lines):
            break

        if lines[c].strip():
            rule = Rule(lines[c].strip())
            rules[rule.addr] = rule
            c += 1
        else:
            c += 1
            break

    return c, rules


def p1(content: list[str]) -> int:
    idx, rules = parse_rules(content)

    messages = content[idx:]

    def valid(m: str) -> bool:
        if not m.strip():
            return False
        status, s = rules[0].parse(m, rules)
        if status and not s.strip():
            return True
        return False

    valid_messages = filter(lambda m: valid(m), messages)
    return len(list(valid_messages))


def write_antlr_grammar(rules: dict[int, Rule]) -> None:
    """Convert rules dictionary to antlr4 grammar."""

    pth = Path("solution")
    pth.mkdir(exist_ok=True)
    grammar_pth = pth / "Problem.g4"

    with grammar_pth.open("w") as f:
        f.write("grammar Problem;\n")
        f.write("prog: g0 EOF;\n")
        f.write("NEWLINE : [\\r\\n]+ -> skip;")

        for rule in rules.values():
            f.write(rule.antlr())
            f.write("\n")

    subprocess.run(
        # don't worry, this argument's been checked
        ["/opt/homebrew/bin/antlr", "-Dlanguage=Python3", str(grammar_pth)],  # noqa: S603
        check=True,
    )


def parse(line: str) -> bool:
    from solution.ProblemLexer import ProblemLexer
    from solution.ProblemParser import ProblemParser

    inp = InputStream(line)
    lexer = ProblemLexer(inp)
    tokens = CommonTokenStream(lexer)
    parser = ProblemParser(tokens)
    tree = parser.prog()

    return tree.parser.getNumberOfSyntaxErrors() == 0


def p2(content: list[str]) -> int:
    idx, rules = parse_rules(content)

    rules[8] = Rule("8: 42 | 42 8")
    rules[11] = Rule("11: 42 31 | 42 11 31")

    write_antlr_grammar(rules)
    return sum(parse(msg) for msg in content[idx:])


@pytest.mark.parametrize(
    ("msg", "expected"),
    [
        ("aaaaabbaabaaaaababaa", 1),
        ("aaaabbaabbaaaaaaabbbabbbaaabbaabaaa", 1),
        ("aaabbbbbbaaaabaababaabababbabaaabbababababaaa", 1),
        ("aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba", 1),
        ("ababaaaaaabaaab", 1),
        ("ababaaaaabbbaba", 1),
        ("abbbbabbbbaaaababbbbbbaaaababb", 1),
        ("baabbaaaabbaaaababbaababb", 1),
        ("babbbbaabbbbbabbbbbbaabaaabaaa", 1),
        ("bbabbbbaabaabba", 1),
        ("bbbababbbbaaaaaaaabbababaaababaabab", 1),
        ("bbbbbbbaaaabbbbaaabbabaaa", 1),
    ],
)
def test_p2(msg: str, expected: int) -> None:
    # not instant to run this test, as it runs antlr each time.
    with open("complex.txt") as f:
        content = f.read().split("\n\n")
    assert len(content) == 2  # noqa: S101,PLR2004

    content[-1] = msg
    content = "\n\n".join(content).split("\n")

    assert p2(content) == expected  # noqa: S101


def main():
    with open(sys.argv[1]) as f:
        content = f.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
