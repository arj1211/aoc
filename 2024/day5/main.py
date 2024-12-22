import json
import pathlib
from typing import List, Tuple

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.read()

ordering_rules, pages = data.split("\n\n")
ordering_rules = ordering_rules.strip().split("\n")
pages = pages.strip().split("\n")


def get_anti_relation(relation: List[Tuple[str, str]]):
    return [(b, a) for a, b in relation]


def get_rules_relation(ordering_rules: List[str] = ordering_rules):
    ordering = []
    for rule in ordering_rules:
        a, b = rule.split("|")
        ordering.append((a, b))
    return ordering


def get_page_relation(page: List[str]):
    relation = []
    for i in range(len(page)):
        for j in range(i + 1, len(page)):
            relation.append((page[i], page[j]))
    return relation


def page_violates_rules(
    anti_rules_relation: List[Tuple[str, str]], page_relation: List[Tuple[str, str]]
):
    return set(anti_rules_relation).intersection(page_relation)


def swap_elements(l, elemA, elemB):
    i, j = 0, 0
    for idx, value in enumerate(l):
        if value == elemA:
            i = idx
        if value == elemB:
            j = idx
    l[i], l[j] = l[j], l[i]
    return l


def correct_violations(page, anti_rules_relation, page_relation):
    violation = page_violates_rules(anti_rules_relation, page_relation)
    if violation:
        violation = violation.pop()
    while violation:
        page = swap_elements(page, *violation)
        page_relation = get_page_relation(page)
        violation = page_violates_rules(anti_rules_relation, page_relation)
        if violation:
            violation = violation.pop()
    return page


rules_relation = get_rules_relation(ordering_rules)
anti_rules_relation = get_anti_relation(rules_relation)

s1 = 0
s2 = 0
for page in pages:
    page = page.split(",")
    page_relation = get_page_relation(page)
    violations = page_violates_rules(anti_rules_relation, page_relation)
    if not violations:
        s1 += int(page[len(page) // 2])
    else:
        corrected_page = correct_violations(page, anti_rules_relation, page_relation)
        s2 += int(corrected_page[len(corrected_page) // 2])


print("Middle number sum of correctly-ordered updates:", s1)
print("Middle number sum of corrected updates:", s2)
