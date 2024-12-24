import pathlib
from typing import Dict, Generator, List, Optional, Sequence, Set, Tuple

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


next_direction_map = {"^": ">", ">": "v", "v": "<", "<": "^"}


def get_next_turn_pos(grid, curr_pos):
    x, y, d = curr_pos
    if d == "^":
        while x >= 1 and grid[x - 1][y] != "#":
            x -= 1
    if d == "v":
        # walk in this dir until obstacle or oob
        while x < len(grid) - 1 and grid[x + 1][y] != "#":
            x += 1
    if d == "<":
        # walk in this dir until obstacle or oob
        while y >= 1 and grid[x][y - 1] != "#":
            y -= 1
    if d == ">":
        # walk in this dir until obstacle or oob
        while y < len(grid[0]) - 1 and grid[x][y + 1] != "#":
            y += 1
    if (1 <= x < len(grid) - 1) and (1 <= y < len(grid[0]) - 1):
        return x, y, next_direction_map[d]
    return x, y, ""


def detect_loop(grid, curr_pos):
    x, y, d = curr_pos
    turns = set()
    while d:
        x, y, d = get_next_turn_pos(grid, (x, y, d))
        if (x, y, d) in turns:
            return True
        turns.add((x, y, d))
    return False


def detect_loop_if_obstacle(grid, curr_pos, obstacle_pos):
    x, y, d = curr_pos
    reset_val = grid[obstacle_pos[0]][obstacle_pos[1]]
    grid[obstacle_pos[0]][obstacle_pos[1]] = "#"
    loop_detected = detect_loop(grid, curr_pos)
    grid[obstacle_pos[0]][obstacle_pos[1]] = reset_val
    return loop_detected


def locate_starting_pos(
    grid: List[List[chr]], start_symbols: Set[chr] = {"^", "v", "<", ">"}
) -> Tuple[int, int, chr]:
    """
    Locate the starting position in a grid based on specified start symbols.

    Args:
        grid (List[List[chr]]): A 2D list representing the grid.
        start_symbols (Set[chr], optional): A set of characters representing the start symbols. Defaults to {"^", "v", "<", ">"}.

    Returns:
        Tuple[int, int, chr]: A tuple containing the row index, column index, and the start symbol found.
                              Returns (-1, -1, "") if no start symbol is found.
    """
    for i in range(len(grid)):
        j = [idx for idx in range(len(grid[i])) if grid[i][idx] in start_symbols]
        if len(j) == 1:
            j = j[0]
            return i, j, grid[i][j]
    return -1, -1, ""


def step(
    grid: List[List[chr]],
    curr_pos: Tuple[int, int, chr],
    next_direction_map: Dict[chr, chr] = {"^": ">", ">": "v", "v": "<", "<": "^"},
) -> Tuple[int, int, chr]:
    """
    Move a position in a grid based on the current direction and handle obstacles.

    Args:
        grid (List[List[chr]]): A 2D list representing the grid where each cell can be a character.
        curr_pos (Tuple[int, int, chr]): A tuple containing the current x and y coordinates and the direction.
        next_direction_map (Dict[chr, chr], optional): A dictionary mapping the current direction to the next direction
            when an obstacle is encountered. Defaults to {"^": ">", ">": "v", "v": "<", "<": "^"}.

    Returns:
        Tuple[int, int, chr]: A tuple containing the new x and y coordinates and the new direction.
    """

    def _get_dx_dy(direction):
        dx = 1 if direction == "v" else -1 if direction == "^" else 0
        dy = 1 if direction == ">" else -1 if direction == "<" else 0
        return dx, dy

    x, y, direction = curr_pos
    dx, dy = _get_dx_dy(direction)
    height, width = len(grid), len(grid[0])

    new_x, new_y = x + dx, y + dy

    if not (0 <= new_x < height and 0 <= new_y < width):
        return new_x, new_y, ""

    if grid[new_x][new_y] == "#":
        direction = next_direction_map[direction]

        dx, dy = _get_dx_dy(direction=direction)
        new_x, new_y = x + dx, y + dy

    return new_x, new_y, direction


def detect_in_loop(
    coords_sequence: Sequence[Tuple[int, int, chr]]
) -> Tuple[bool, Optional[List[Tuple[int, int]]], int]:
    """
    Detect if sequence contains a loop and return loop information.

    Returns:
        Tuple containing:
        - bool: Whether loop was detected
        - List: Loop sequence if found, None otherwise
        - int: Length of the loop (0 if no loop)
    """
    position_history: Dict[Tuple[int, int, chr], int] = {}

    for i, pos in enumerate(coords_sequence):
        if pos in position_history:
            # Loop found - calculate loop sequence
            loop_start = position_history[pos]
            loop_sequence = list(coords_sequence[loop_start:i])
            return True, loop_sequence, len(loop_sequence)
        position_history[pos] = i

    return False, None, 0


def count_visited_positions(
    grid: List[List[chr]], start_pos: Tuple[int, int, chr]
) -> Tuple[int, Set[Tuple[int, int]]]:

    visited = []
    distinct_positions = set()
    x, y, direction = start_pos

    while direction:
        visited.append((x, y, direction))
        distinct_positions.add((x, y))
        x, y, direction = step(grid=grid, curr_pos=(x, y, direction))
        is_loop, loop_seq, loop_len = detect_in_loop(visited)
        if is_loop:
            break

    return len(distinct_positions), distinct_positions


if __name__ == "__main__":

    x, y, direction = locate_starting_pos(grid=data)
    result, path = count_visited_positions(grid=data, start_pos=(x, y, direction))
    print("Number of distinct positions the guard will visit:", result)

    N = 0
    for obstacle_pos in path:
        if detect_loop_if_obstacle(data, (x, y, direction), obstacle_pos):
            N += 1

    print("Number of obstacles that will cause the guard to loop:", N)

    # turns = set()
    # while d:
    #     x, y, d = get_next_turn_pos(data, (x, y, d))
    #     if (x, y, d) in turns:
    #         print("Loop detected!")
    #         break
    #     turns.add((x, y, d))
    # data[x][y] = d
    # for row in data:
    #     print("".join(row))
    # data[x][y] = "."
    # print()
    # sleep(0.25)
