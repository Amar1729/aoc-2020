#! /usr/bin/env python3

"""
Had quite some trouble doing part2 with my home-spun parsing approach, so i switched over
to antlr to help me out. learning it on-the-fly is a bit tough, so i came back (much) later
to this challenge to solve it.

Make sure to have antlr installed, and generate grammar files via:
    antlr -Dlanguage=Python3 expr/Expr.g4
"""

from __future__ import annotations

import math
import re
import sys

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from expr.ExprLexer import ExprLexer
from expr.ExprListener import ExprListener
from expr.ExprParser import ExprParser

# #### #### #### #### #### #### #### ####
# ### Listener used for Part 2 ###
# #### #### #### #### #### #### #### ####


class CalcExprListener(ExprListener):
    def __init__(self):
        self.result = {}

    def exitProg(self, ctx: ExprParser.ProgContext):
        self.result["FINAL"] = self.result[ctx.getChild(0)]

    def exitParens(self, ctx: ExprParser.ParensContext):
        assert ctx.getChildCount() == 3
        self.result[ctx] = self.result[ctx.getChild(1)]

    def exitExpr(self, ctx: ExprParser.ExprContext):
        self.result[ctx] = math.prod(
            [self.result[ctx.getChild(i)] for i in range(0, ctx.getChildCount(), 2)]
        )

    def exitAddExpr(self, ctx: ExprParser.AddExprContext):
        self.result[ctx] = sum(
            [self.result[ctx.getChild(i)] for i in range(0, ctx.getChildCount(), 2)]
        )

    def exitInt(self, ctx: ExprParser.IntContext):
        self.result[ctx] = int(ctx.getChild(0).getText())


# #### #### #### #### #### #### #### ####
# ### Part 1 ###
# #### #### #### #### #### #### #### ####


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

            if isinstance(tokens[0], str) and tokens[0] == "(":  # )
                tokens.pop(0)
                s2 = calculate_tokens(tokens)
            elif isinstance(tokens[0], int):
                s2 = tokens.pop(0)
            else:
                raise Exception(s, op, tokens)

            s = eval(f"{s} {op} {s2}")

        elif tokens[0] == "(":  # )
            tokens.pop(0)
            s = calculate_tokens(tokens)

        elif tokens[0] in "+*":
            op = tokens.pop(0)

            if isinstance(tokens[0], int):
                s2 = tokens.pop(0)
            elif isinstance(tokens[0], str) and tokens[0] == "(":  # )
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


# #### #### #### #### #### #### #### ####
# ### Part 2 ###
# #### #### #### #### #### #### #### ####


def parse_antlr(line: str) -> int:
    inp = InputStream(line)
    lexer = ExprLexer(inp)
    tokens = CommonTokenStream(lexer)
    parser = ExprParser(tokens)

    tree = parser.prog()

    listener = CalcExprListener()

    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    print("FINAL: ", listener.result["FINAL"])
    return listener.result["FINAL"]


def p2(content: list[str]) -> int:
    return sum(map(parse_antlr, content))


def main() -> None:
    with open(sys.argv[1]) as f:
        content = [line.strip() for line in f.readlines()]

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
