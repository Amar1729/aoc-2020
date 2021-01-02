#! /usr/bin/env python3

import sys
import re

from typing import List, Union, Tuple


def lex_rec(expr: str):
    def tokenize_str(m):
        return m.group(), expr[m.span()[1]:]

    m_int = re.match(r"\d+", expr)
    if m_int:
        t, s = tokenize_str(m_int)
        return int(t), s

    m_op = re.match(r"[+*()]", expr)
    if m_op:
        return tokenize_str(m_op)


def parse_tokens(expr: str):
    tokens = []

    s = expr.lstrip()
    while s:
        token, s = lex_rec(s)
        s = s.lstrip()
        if token:
            tokens.append(token)

    return tokens


def calculate_tokens(tokens) -> int:
    if len(tokens) == 1 and isinstance(tokens[0], int):
        return tokens.pop(0)

    s = None

    while tokens:
        if isinstance(tokens[0], int):
            s = tokens.pop(0)
            op = tokens.pop(0)

            if op == ")":
                return s

            if isinstance(tokens[0], str) and tokens[0] == "(":
                tokens.pop(0)
                s2 = calculate_tokens(tokens)
            elif isinstance(tokens[0], int):
                s2 = tokens.pop(0)
            else:
                raise Exception(s, op, tokens)

            s = eval(f"{s} {op} {s2}")

        elif tokens[0] == "(":
            tokens.pop(0)
            s = calculate_tokens(tokens)

        elif tokens[0] in "+*":
            op = tokens.pop(0)

            if isinstance(tokens[0], int):
                s2 = tokens.pop(0)
            elif isinstance(tokens[0], str) and tokens[0] == "(":
                tokens.pop(0)
                s2 = calculate_tokens(tokens)

            s = eval(f"{s} {op} {s2}")

        if tokens and tokens[0] == ")":
            tokens.pop(0)
            break

    if s is None:
        raise Exception
    return s


def parse(line):
    return calculate_tokens(parse_tokens(line))


def p1(content):
    return sum(list(map(parse, content)))


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
