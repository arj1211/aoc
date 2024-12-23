import pathlib
from typing import List, Set, Tuple

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.readlines()


_data = [
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

_data = [
    "...#.......",
    ".........#.",
    "...........",
    "...........",
    "...........",
    ".#.........",
    "...^...#...",
    "...........",
    "......#....",
    "#..........",
    "........#..",
]

data = [list(d.strip()) for d in data]

start_symbols = {"^", "v", "<", ">"}
next_direction = {"^": ">", ">": "v", "v": "<", "<": "^"}


def locate_starting_pos(
    grid: List[List[chr]], start_symbols: Set[chr] = start_symbols
) -> Tuple[int, int, chr]:
    for i in range(len(grid)):
        j = [idx for idx in range(len(grid[i])) if grid[i][idx] in start_symbols]
        if len(j) == 1:
            j = j[0]
            return i, j, grid[i][j]
    return -1, -1, ""


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


# this gets stuck in loops
def count_visited_positions(
    grid: List[List[chr]],
    start_pos: Tuple[int, int],
    start_direction: chr,
    return_visited: bool = False,
) -> int | Set[Tuple[int, int]]:
    visited = set()
    x, y = start_pos
    direction = start_direction
    while direction:
        pos = (x, y)
        if pos not in visited:
            visited.add(pos)
        x, y, direction = step(grid=grid, curr_pos=pos, direction=direction)

    if return_visited:
        return visited
    return len(visited)


def detect_in_loop(
    grid: List[List[chr]],
    curr_pos: Tuple[int, int],
    direction: chr,
    return_loop_path: bool = False,
) -> bool | Tuple[bool, Set[Tuple[int, int]]]:
    visited = set()
    revisited = set()
    x, y = curr_pos

    while direction:
        pos = (x, y)
        if pos not in visited:
            visited.add(pos)
            revisited.clear()
        else:
            if pos in revisited:
                print(f"Entered a loop at {pos} heading {direction}")
                if return_loop_path:
                    return True, revisited
                return True
            revisited.add(pos)
        x, y, direction = step(grid=grid, curr_pos=pos, direction=direction)

    return False, set()


def place_obstacle(grid: List[List[chr]], pos: Tuple[int, int]) -> List[List[chr]]:
    x, y = pos
    if grid[x][y] == "#":
        return grid
    grid_copy = [[grid[i][j] for j in range(len(grid[i]))] for i in range(len(grid))]
    grid_copy[x][y] = "#"
    return grid_copy


def simulate_obstacle_placements(
    grid: List[List[chr]],
    start_pos: Tuple[int, int],
    start_direction: chr,
    obstacle_placements: List[Tuple[int, int]] = [],
) -> int:

    N = 0
    if not obstacle_placements:
        obstacle_placements = [
            (i, j)
            for i in range(len(grid))
            for j in range(len(grid[i]))
            if grid[i][j] == "." and (i, j) != start_pos
        ]
    loop_coords = []
    for idx, obstacle_placement in enumerate(obstacle_placements):
        sim_grid = place_obstacle(grid, obstacle_placement)
        is_loop, coords = detect_in_loop(
            sim_grid, start_pos, start_direction, return_loop_path=True
        )
        if is_loop:
            loop_coords.append((obstacle_placement, coords))
            N += 1

    return N, loop_coords


if __name__ == "__main__":

    x, y, direction = locate_starting_pos(grid=data)
    result = count_visited_positions(data, (x, y), direction)
    print("Number of distinct positions the guard will visit:", result)

    result, coords_lists = simulate_obstacle_placements(data, (x, y), direction)
    print("Number of potential obstacle positions:", result)
