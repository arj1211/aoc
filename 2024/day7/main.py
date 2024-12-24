import pathlib

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.readlines()

_data = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20",
]

data = [d.strip() for d in data]


def parse_rule(rule):
    rule = rule.split(": ")
    return int(rule[0]), [int(r) for r in rule[1].split(" ")]


def rule_possibly_true(true_result, current_value, args, arg_i):
    if arg_i == len(args):
        return current_value == true_result
    return rule_possibly_true(
        true_result, current_value + args[arg_i], args, arg_i + 1
    ) or rule_possibly_true(true_result, current_value * args[arg_i], args, arg_i + 1)


def solve_rule(rule):
    result, args = rule
    if rule_possibly_true(result, args[0], args, 1):
        return result
    return 0


S = 0
for rule in data:
    rule = parse_rule(rule)
    S += solve_rule(rule)

print(S)
