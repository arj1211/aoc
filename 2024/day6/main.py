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
    dx, dy = _get_dx_dy(direction)
    height, width = len(grid), len(grid[0])

    new_x, new_y = x + dx, y + dy

    if not (0 <= new_x < height and 0 <= new_y < width):
        return new_x, new_y, ""

    if grid[new_x][new_y] == "#":
        direction = next_direction[direction]
        dx, dy = _get_dx_dy(direction=direction)
        new_x, new_y = x + dx, y + dy

    return new_x, new_y, direction


def count_visited_positions(grid, start_pos, start_direction):
    visited = set()
    x, y = start_pos
    direction = start_direction

    while direction:
        pos = (x, y)
        if pos not in visited:
            visited.add(pos)
        x, y, direction = step(grid=grid, curr_pos=pos, direction=direction)

    return len(visited)


x, y, direction = locate_starting_pos(grid=data)
result = count_visited_positions(data, (x, y), direction)
print("Number of distinct positions the guard will visit:", result)
