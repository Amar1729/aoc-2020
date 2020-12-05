#! /usr/bin/env python3

import sys
import re


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
        if not all(
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
        ):
            return False

        def try_int(s: str, low: int, high: int) -> bool:
            try:
                if low <= int(s) <= high:
                    return True
                else:
                    return False
            except ValueError:
                return False

        if not try_int(self.byr, 1920, 2002):
            return False

        if not try_int(self.iyr, 2010, 2020):
            return False

        if not try_int(self.eyr, 2020, 2030):
            return False

        if self.hgt.endswith("cm"):
            if not try_int(self.hgt.rstrip("cm"), 150, 193):
                return False
        elif self.hgt.endswith("in"):
            if not try_int(self.hgt.rstrip("in"), 59, 76):
                return False
        else:
            return False

        if not re.match(r"#[0-9a-f]{6}$", self.hcl):
            return False

        if self.ecl not in [
            "amb", "blu", "brn", "gry", "grn", "hzl", "oth",
        ]:
            return False

        if not re.match(r"[0-9]{9}$", self.pid):
            return False

        return True


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
