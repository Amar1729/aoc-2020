#! /usr/bin/env python3

import collections
import sys

WIDTH = 25


def p1(content):
    numbers = list(map(int, content))
    d = collections.deque(numbers[:WIDTH], maxlen=WIDTH)

    def check_correct(j) -> bool:
        for x in d:
            if j - x in d:
                return True
        return False

    for idx, n in enumerate(numbers[WIDTH:]):
        if check_correct(n):
            d.append(n)
        else:
            return idx, n


def p2(content):
    idx, total = p1(content)
    numbers = list(map(int, content[:idx]))

    # i and j are lower/upper bounds for a contiguous range in our valid numbers
    i = 0
    j = 1

    curr_sum = numbers[0] + numbers[1]
    while True:
        # optimize this list access out (manually keep track of additions/subtractions)
        # curr_sum = sum(numbers[i:j + 1])

        if curr_sum == total:
            print(f"Range: {i} - {j}")
            print(numbers[i:j + 1])
            answer = sorted(numbers[i:j + 1])
            return answer[0] + answer[-1]
        elif curr_sum < total:
            # too small: range should be increased
            j += 1
            curr_sum += numbers[j]
        elif curr_sum > total:
            # too large: range should be decreased
            curr_sum -= numbers[i]
            i += 1

    return total


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
