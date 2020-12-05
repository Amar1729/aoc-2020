#! /usr/bin/env python3

import sys


class Passport:
    def __init__(self, info: str):
        self.byr = None
        self.iyr = None
        self.eyr = None
        self.hgt = None
        self.hcl = None
        self.ecl = None
        self.pid = None
        self.cid = None

        self.parse_info(info)

    def parse_info(self, info: str):
        for field in info.strip().split(" "):
            key, value = field.split(":")
            if key in dir(self):
                setattr(self, key, value)

    def valid(self) -> bool:
        # check all required attributes are set
        return all(
            map(
                lambda l: getattr(self, l) is not None,
                [
                    "byr",
                    "iyr",
                    "eyr",
                    "hgt",
                    "hcl",
                    "ecl",
                    "pid",
                ],
            )
        )


def calc(content):
    content = content.replace("\n", " ")
    passports = map(Passport, content.split("  "))

    return sum(map(lambda p: p.valid(), passports))


def main():
    with open(sys.argv[1], "r") as f:
        content = f.read()

    result = calc(content)
    print(result)


if __name__ == "__main__":
    main()
