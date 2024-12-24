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


def place_obstacle(grid: List[List[chr]], pos: Tuple[int, int]) -> List[List[chr]]:
    x, y = pos
    if grid[x][y] == "#":
        return grid
    grid_copy = [[grid[i][j] for j in range(len(grid[i]))] for i in range(len(grid))]
    grid_copy[x][y] = "#"
    return grid_copy


def obstacle_in_direction(
    grid: List[List[chr]], curr_pos: Tuple[int, int, chr]
) -> bool:
    x, y, direction = curr_pos

    if direction == "^":
        return any(grid[i][y] == "#" for i in range(x - 1, -1, -1))
    if direction == "v":
        return any(grid[i][y] == "#" for i in range(x + 1, len(grid)))
    if direction == "<":
        return any(grid[x][j] == "#" for j in range(y - 1, -1, -1))
    if direction == ">":
        return any(grid[x][j] == "#" for j in range(y + 1, len(grid[0])))
    return False


def simulate_obstacle_placements(
    grid: List[List[chr]],
    start_pos: Tuple[int, int, chr],
    possible_obstacle_placements: Optional[Set[Tuple[int, int]]] = None,
) -> int:

    start_direction = start_pos[2]
    start_pos = (start_pos[0], start_pos[1])

    N = 0

    if not possible_obstacle_placements:
        possible_obstacle_placements = [
            (i, j)
            for i in range(len(grid))
            for j in range(len(grid[i]))
            if grid[i][j] == "." and (i, j) != start_pos
        ]

    list_of_loop_seq = []
    for idx, obstacle_placement in enumerate(possible_obstacle_placements):

        traveled_coords = []
        sim_grid = place_obstacle(grid, obstacle_placement)

        direction = start_direction
        x, y = start_pos

        while direction:
            traveled_coords.append((x, y, direction))
            x, y, direction = step(grid=sim_grid, curr_pos=(x, y, direction))
            # if there isn't an obstacle in the current direction, break
            if not obstacle_in_direction(grid=sim_grid, curr_pos=(x, y, direction)):
                break
            # if we've visited this position in the past, check if we're in a loop
            if (x, y, direction) in traveled_coords[:-1]:
                is_loop, loop_seq, loop_len = detect_in_loop(traveled_coords)
                if is_loop:
                    list_of_loop_seq.append(
                        {
                            "obstacle_placement": obstacle_placement,
                            "loop_sequence": loop_seq,
                            "loop_length": loop_len,
                        }
                    )
                    print(
                        f"{idx+1}/{len(possible_obstacle_placements)} - Loop detected for obstacle placement {obstacle_placement}"
                    )
                    N += 1
                    break

    return N, list_of_loop_seq


if __name__ == "__main__":

    x, y, direction = locate_starting_pos(grid=data)
    result, path = count_visited_positions(grid=data, start_pos=(x, y, direction))
    print("Number of distinct positions the guard will visit:", result)

    result, coords_lists = simulate_obstacle_placements(
        grid=data, start_pos=(x, y, direction), possible_obstacle_placements=path
    )
    print("Number of potential obstacle positions:", result)
