from random import choice, randint, shuffle
from time import sleep
from typing import Dict, Generator, List, Optional, Sequence, Set, Tuple


def generate_cycling_pairs(
    cycle_length: int = 5,
    num_cycles: int = -1,
    padding_length: int = 5,
) -> Generator[Tuple[Tuple[int, int], int], None, None]:
    """
    Generate a sequence of cycling pairs of coordinates.

    Args:
        cycle_length (int): The number of unique coordinate pairs to generate for the cycle. Default is 5.
        num_cycles (int): The number of cycles to generate. If -1, the generator will cycle indefinitely. Default is -1.
        padding_length (int): The number of unique coordinate pairs to generate for padding. Default is 5.

    Yields:
        Tuple[Tuple[int, int], int]: A tuple containing a coordinate pair and an index. The index is -1 for padding pairs and
        ranges from 0 to cycle_length-1 for cycling pairs.
    """
    max_cycle_pair_value = 10
    pairs = set()
    while len(pairs) < cycle_length:
        pairs.add((randint(0, max_cycle_pair_value), randint(0, max_cycle_pair_value)))
    padding = set()
    while len(padding) < padding_length:
        padding.add(
            (
                randint(max_cycle_pair_value + 1, max_cycle_pair_value + 10),
                randint(max_cycle_pair_value + 1, max_cycle_pair_value + 10),
            )
        )

    padding = list(padding)
    pairs = list(pairs)
    for coord in padding:
        yield coord, -1

    if num_cycles == -1:
        while True:
            for i, coord in enumerate(pairs):
                yield coord, i
    else:
        for _ in range(num_cycles):
            for i, coord in enumerate(pairs):
                yield coord, i


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


if __name__ == "__main__":

    original_data = [
        list(d.strip())
        for d in [
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
    ]

    for obstacle_coordinate in [(9, 2), (7, 0), (7, 2)]:
        data = [row.copy() for row in original_data]
        data[obstacle_coordinate[0]][obstacle_coordinate[1]] = "#"
        print("=" * 50)
        print("the obstacle is at:", obstacle_coordinate)
        for row in data:
            print("".join(row))
        print()

        x, y, direction = locate_starting_pos(grid=data)
        start_location = (x, y, direction)
        pos = (x, y, direction)
        traversal_coords = []

        is_loop = False
        loop_seq = []
        loop_len = 0
        display_grid = [data[i].copy() for i in range(len(data))]

        max_iterations = 10_000  # Set a maximum iteration limit
        iteration_count = 0
        while direction and iteration_count < max_iterations:
            iteration_count += 1
            pos = (x, y, direction)
            display_grid[x][y] = direction

            traversal_coords.append(pos)
            x, y, direction = step(grid=data, curr_pos=pos)

            display_grid[x][y] = "@"
            for row in display_grid:
                print("".join(row))
            print()
            sleep(0.25)

            is_loop, loop_seq, loop_len = detect_in_loop(traversal_coords)
            if is_loop:
                break

        print(f"Loop detected: {is_loop}")
        print(f"Loop sequence: {loop_seq}")
        print(f"Loop length: {loop_len}")
        print()

        display_grid = [data[i].copy() for i in range(len(data))]
        for coord in loop_seq:
            x, y, _ = coord
            display_grid[x][y] = "O"
        display_grid[start_location[0]][start_location[1]] = start_location[2]
        for row in display_grid:
            print("".join(row))

        print("=" * 50)
