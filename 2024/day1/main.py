import pathlib

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.readlines()

data = list(map(lambda x: tuple(int(y) for y in x.strip().split("  ")), data))

l1 = [x[0] for x in data]
l2 = [x[1] for x in data]

l1 = sorted(l1)
l2 = sorted(l2)

s = 0

for n1, n2 in zip(l1, l2):
    s += abs(n1 - n2)

print("List distance:", s)

freq = {}
for n in l2:
    if n not in freq:
        freq[n] = 0
    freq[n] += 1

s = 0
for n in l1:
    s += n * (0 if n not in freq else freq[n])

print("Similarity score:", s)
