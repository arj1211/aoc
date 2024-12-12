import pathlib

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.readlines()


data = list(map(lambda x: list(int(y) for y in x.strip().split(" ")), data))


def is_safe_1(levels):
    if levels != sorted(levels) and levels != sorted(levels, reverse=True):
        return 0
    shifted_levels = levels[1:]
    for i in range(len(shifted_levels)):
        if abs(levels[i] - shifted_levels[i]) not in {1, 2, 3}:
            return 0
    return 1


s = 0
for levels in data:
    s += is_safe_1(levels)

print("Safe reports:", s)


def is_safe_2(levels):
    if is_safe_1(levels):
        return 1
    for i in range(len(levels)):
        single_fault_levels = levels[:i] + levels[i + 1 :]
        if is_safe_1(single_fault_levels):
            return 1
    return 0


s = 0
for levels in data:
    s += is_safe_2(levels)

print("Single-fault safe reports:", s)
