#! /usr/bin/env python3

import sys


N = 20201227


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def find_loop(pub):
    p, q = 7, pub
    ns = int(N ** 0.5)

    pns = p ** ns
    mp = modinv(p, N)

    qset = {}

    rhs = q
    qset[rhs] = 0
    for j in range(1, ns + 1):
        # rhs = (q * mp ** j) % N
        rhs = (rhs * mp) % N
        qset[rhs] = j

    lhs = 1
    if lhs in qset:
        return qset[lhs]
    for i in range(1, ns + 1):
        # lhs = (p ** (i * ns)) % N
        lhs = (lhs * pns) % N
        if lhs in qset:
            return i * ns + qset[lhs]


def p1(content):
    pub_card = int(content[0])
    pub_door = int(content[1])

    p = find_loop(pub_card)
    q = find_loop(pub_door)

    # print(f"Found card loop: {p}\nFound door loop: {q}")

    enc = pow(pub_card, q, N)
    assert enc == pow(pub_door, p, N)

    return enc


def p2(content):
    pass


def main():
    content = sys.stdin.read().rstrip().split("\n")

    print(p1(content))
    # print(p2(content))


if __name__ == "__main__":
    main()
