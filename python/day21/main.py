#! /usr/bin/env python3

import copy
import sys
import re


def parse(food):
    ingredients = re.sub(r' \(.*\)', '', food).split(" ")
    allergens = re.findall(r'\(contains (.*)\)', food)[0].split(", ")
    return set(ingredients), set(allergens)


def p1(content, p2=False):
    foods = list(map(parse, content))

    translation = {}

    all_allergens = set(sf for f in foods for sf in f[1])

    def find_translation():
        for fi in range(len(foods)):
            if len(foods[fi][0]) == 1 and len(foods[fi][1]) == 1:
                return foods[fi][0].pop(), foods[fi][1].pop()
            for oi in range(len(foods)):
                if fi != oi:
                    ingredients = foods[fi][0].intersection(foods[oi][0])
                    allergens = foods[fi][1].intersection(foods[oi][1])
                    if len(ingredients) == 1 and len(allergens) == 1:
                        return ingredients.pop(), allergens.pop()

        # much heavier computation-wise, save for last attempt
        for k in all_allergens:
            si = set()
            sa = set()
            for i, a in filter(lambda f: k in f[1], foods):
                # print('searching', k, a)
                if si and sa:
                    si &= i
                    sa &= a
                else:
                    si = copy.copy(i)
                    sa = copy.copy(a)

                if sa:
                    if len(sa) == 1:
                        if len(si) == 1:
                            return si.pop(), sa.pop()

        return None, None

    while True:
        # find the next translation
        ingredient, allergen = find_translation()
        if ingredient is None and allergen is None:
            break
        translation[ingredient] = allergen

        # update our list of foods
        to_delete = []
        for fi in range(len(foods)):
            i, a = foods[fi]
            if ingredient in i:
                i.remove(ingredient)
            if allergen in a:
                a.remove(allergen)

            if len(foods[fi][0]) == 0 and len(foods[fi][1]) == 0:
                to_delete.append(fi)

        for fi in to_delete:
            foods.pop(fi)

    if p2:
        return translation

    return sum(len(ingredients) for ingredients, _ in foods)


def p2(content):
    translation = p1(content, p2=True)
    return ",".join(p[0] for p in sorted(translation.items(), key=lambda p: p[1]))


def main():
    content = sys.stdin.read().rstrip().split("\n")

    # print(p1(content))
    print(p2(content))


if __name__ == "__main__":
    main()
