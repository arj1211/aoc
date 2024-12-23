import argparse
import logging
import os
import pathlib
from datetime import datetime
from functools import wraps
from typing import Callable, Generator, List, Set, Tuple

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


# Configure logging
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/guard_simulation_{timestamp}.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def log_function(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logging.debug(f"Entering {func_name} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.debug(f"Exiting {func_name} with result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in {func_name}: {str(e)}", exc_info=True)
            raise

    return wrapper


def show_grid(grid: List[List[chr]]) -> None:
    for row in grid:
        logging.debug("".join(row))


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
        logging.debug(
            f"Hit obstacle at {new_x}, {new_y} during step from {x}, {y} heading {direction}"
        )
        direction = next_direction[direction]
        logging.debug(f"Changing direction to {direction}")
        dx, dy = _get_dx_dy(direction=direction)
        new_x, new_y = x + dx, y + dy
        logging.debug(f"New position: {new_x}, {new_y}")

    return new_x, new_y, direction


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
    grid: List[List[chr]], curr_pos: Tuple[int, int], direction: chr
) -> bool:
    visited = set()
    revisited = set()
    x, y = curr_pos

    while direction:
        pos = (x, y)
        if pos not in visited:
            logging.debug(f"Visiting position {pos} heading {direction}")
            visited.add(pos)
            revisited.clear()
        else:
            if pos in revisited:
                logging.debug(f"Entered a loop at {pos} heading {direction}")
                return True
            logging.debug(f"Revisiting position {pos} heading {direction}")
            revisited.add(pos)
        x, y, direction = step(grid=grid, curr_pos=pos, direction=direction)

    logging.debug("No loop detected")
    return False


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
            (i, j) for i in range(len(grid)) for j in range(len(grid[i]))
        ]
    for obstacle_placement in obstacle_placements:
        sim_grid = place_obstacle(grid, obstacle_placement)
        if detect_in_loop(sim_grid, start_pos, start_direction):
            N += 1
            logging.debug(
                f"Detected loop in path when obstacle placed at {obstacle_placement}"
            )
        else:
            logging.debug(
                f"No loop detected in path when obstacle placed at {obstacle_placement}"
            )
    return N


def get_neighbouring_positions_of_visited(
    visited: Set[Tuple[int, int]], grid: List[List[chr]]
) -> Set[Tuple[int, int]]:
    logging.debug(
        f"Finding neighbors for {len(visited)} visited positions in {len(grid)}x{len(grid[0])} grid"
    )

    neighbouring_positions = set()
    for pos in visited:
        x, y = pos
        logging.debug(f"Checking neighbors for position ({x}, {y})")

        for dx, dy in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < len(grid)
                and 0 <= new_y < len(grid[0])
                and grid[new_x][new_y] == "."
            ):
                logging.debug(f"Found valid neighbor at ({new_x}, {new_y})")
                neighbouring_positions.add((new_x, new_y))

    logging.debug(f"Found {len(neighbouring_positions)} valid neighboring positions")
    return neighbouring_positions


x, y, direction = locate_starting_pos(grid=data)
result = count_visited_positions(data, (x, y), direction)
print("Number of distinct positions the guard will visit:", result)

visited = count_visited_positions(data, (x, y), direction, return_visited=True)
visited |= get_neighbouring_positions_of_visited(visited, data)
result = simulate_obstacle_placements(data, (x, y), direction, visited)
print("Number of potential obstacle positions:", result)
