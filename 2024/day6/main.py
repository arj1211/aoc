import pathlib
from typing import Generator, List, Set, Tuple

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.readlines()


data = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#...",
]

data = [list(d.strip()) for d in data]

start_symbols = {"^", "v", "<", ">"}
next_direction = {"^": ">", ">": "v", "v": "<", "<": "^"}


def locate_starting_pos(
    grid: List[List[chr]], start_symbols: Set[chr] = start_symbols
) -> Tuple[int, int]:
    for i in range(len(grid)):
        j = [idx for idx in range(len(grid[i])) if grid[i][idx] in start_symbols]
        if len(j) == 1:
            j = j[0]
            return i, j, grid[i][j]
    return -1, -1


def step(
    grid: List[List[chr]], curr_pos: Tuple[int, int], direction: chr
) -> Tuple[int, int, chr]:

    def _get_dx_dy(direction):
        dx = 1 if direction == "v" else -1 if direction == "^" else 0
        dy = 1 if direction == ">" else -1 if direction == "<" else 0
        return dx, dy

    x, y = curr_pos
    dx, dy = _get_dx_dy(direction=direction)

    assert (dx * dy == 0) and (dx != dy)

    new_x, new_y = x + dx, y + dy

    if ((new_x < 0) or (new_x >= len(grid))) or (
        (new_y < 0) or (new_y >= len(grid[new_x]))
    ):
        return new_x, new_y, ""

    if grid[new_x][new_y] == "#":
        direction = next_direction[direction]
        dx, dy = _get_dx_dy(direction=direction)
        new_x, new_y = x + dx, y + dy

    return new_x, new_y, direction


x, y, direction = locate_starting_pos(grid=data)
n = 0
while direction:
    n += 1 if data[x][y] != "X" else 0
    data[x][y] = "X"
    x, y, direction = step(grid=data, curr_pos=(x, y), direction=direction)

print("Number of distinct positions the guard will visit:", n)
