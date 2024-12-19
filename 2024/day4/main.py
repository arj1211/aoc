import pathlib
from typing import Generator, List, Tuple

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.readlines()

data = [d.strip() for d in data]


def transpose(data):
    return [
        "".join([data[i][j] for i in range(len(data))]) for j in range(len(data[0]))
    ]


def countXMAS(r: str, str_len=len("XMAS")) -> int:
    n = 0
    ptr = str_len
    while ptr <= len(r):
        n += int(r[ptr - str_len : ptr] in ["XMAS", "SAMX"])
        ptr += 1
    return n


def generate_kernels(
    data: List[List[chr]], size: Tuple[int, int] = (4, 4)
) -> Generator[List[List[str]], None, None]:
    # Assuming `data` is a m by n matrix
    k_top_left_i, k_top_left_j = 0, 0
    while k_top_left_i <= len(data) - size[0]:
        M = [
            d[k_top_left_j : k_top_left_j + size[1]]
            for d in data[k_top_left_i : k_top_left_i + size[0]]
        ]
        M = ["".join(row) for row in M]
        yield M
        k_top_left_j += 1
        if k_top_left_j > len(data[0]) - size[1]:
            k_top_left_j = 0
            k_top_left_i += 1


def check_MAS(kernel):
    k_idxs = [0, 1, 2]
    s1 = "".join([kernel[i][i] for i in k_idxs])
    s2 = "".join([kernel[i][2 - i] for i in k_idxs])
    return int(all([s in ["MAS", "SAM"] for s in [s1, s2]]))


N = 0

# all horizontal
for row in data:
    N += countXMAS(row)

# all vertical
for col in transpose(data):
    N += countXMAS(col)

k_idxs = [0, 1, 2, 3]
for kernel in generate_kernels(data):
    s1 = "".join([kernel[i][i] for i in k_idxs])
    s2 = "".join([kernel[i][3 - i] for i in k_idxs])
    N += sum(int(s in ["XMAS", "SAMX"]) for s in [s1, s2])

print("XMAS appearances:", N)

M = 0
for kernel in generate_kernels(data, size=(3, 3)):
    M += check_MAS(kernel)

print("X-MAS appearances:", M)
