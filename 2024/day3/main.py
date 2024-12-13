import pathlib
import re

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.read()


def compute(data_str: str):
    muls = re.findall("mul\(\d{1,3},\d{1,3}\)", data_str)
    muls = list(map(lambda x: tuple(int(y) for y in x[4:-1].split(",")), muls))
    return sum(x[0] * x[1] for x in muls)


print("Sum:", compute(data))

s = 0
while data:
    if data.find("don't()") == -1:
        s += compute(data)
        break
    to_proc = data[: data.find("don't()")]
    s += compute(to_proc)
    data = data[data.find("don't()") :]
    data = data[data.find("do()") :]

print("Enabled sum:", s)
