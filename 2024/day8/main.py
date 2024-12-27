import pathlib
from typing import Dict, List, Set, Tuple

current_dir = pathlib.Path(__file__).parent.resolve()
input_data_path = current_dir.joinpath("input.txt")

with open(input_data_path, "r") as input_file:
    data = input_file.readlines()


def setup_test_cases():

    test_cases = [
        (
            [
                "..........",
                "..........",
                "..........",
                "....a.....",
                "..........",
                ".....a....",
                "..........",
                "..........",
                "..........",
                "..........",
            ],
            [
                "..........",
                "...#......",
                "..........",
                "....a.....",
                "..........",
                ".....a....",
                "..........",
                "......#...",
                "..........",
                "..........",
            ],
        ),
        (
            [
                "..........",
                "..........",
                "..........",
                "....a.....",
                "........a.",
                ".....a....",
                "..........",
                "..........",
                "..........",
                "..........",
            ],
            [
                "..........",
                "...#......",
                "#.........",
                "....a.....",
                "........a.",
                ".....a....",
                "..#.......",
                "......#...",
                "..........",
                "..........",
            ],
        ),
        (
            [
                "............",
                "........0...",
                ".....0......",
                ".......0....",
                "....0.......",
                "......A.....",
                "............",
                "............",
                "........A...",
                ".........A..",
                "............",
                "............",
            ],
            [
                "......#....#",
                "...#....0...",
                "....#0....#.",
                "..#....0....",
                "....0....#..",
                ".#....A.....",
                "...#........",
                "#......#....",
                "........A...",
                ".........A..",
                "..........#.",
                "..........#.",
            ],
        ),
    ]

    _test_cases = []
    for data, result in test_cases:
        _data = [list(r) for r in data]
        _result = [list(r) for r in result]
        _test_cases.append((_data, _result))
    test_cases = _test_cases

    return test_cases


def _get_antenna_positions(data) -> Dict[chr, Set[Tuple[int, int]]]:
    antenna_positions = {}
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell.isalnum():
                if cell not in antenna_positions:
                    antenna_positions[cell] = set()
                antenna_positions[cell].add((i, j))
    return antenna_positions


def _get_antenna_pairs(
    antenna_positions,
) -> List[Tuple[chr, Tuple[int, int], Tuple[int, int]]]:
    antenna_position_pairs = []
    for antenna, positions in antenna_positions.items():
        positions = list(positions)
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                antenna_position_pairs.append((antenna, positions[i], positions[j]))
    return antenna_position_pairs


def _get_antinode_positions(antenna_position_pairs) -> Dict[chr, Set[Tuple[int, int]]]:

    def _get_points_info_and_distance(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return dx, dy

    antinode_positions = {}
    for antenna, p1, p2 in antenna_position_pairs:
        dx, dy = _get_points_info_and_distance(p1, p2)
        antinode1 = (p1[0] - dx, p1[1] - dy)
        antinode2 = (p2[0] + dx, p2[1] + dy)
        if antenna not in antinode_positions:
            antinode_positions[antenna] = set()
        antinode_positions[antenna].add(antinode1)
        antinode_positions[antenna].add(antinode2)

    return antinode_positions


def _filter_antinode_positions_within_map(
    antinode_positions, max_x, max_y
) -> Dict[chr, Set[Tuple[int, int]]]:

    def point_is_within_bounds(point, max_x, max_y):
        return 0 <= point[0] < max_x and 0 <= point[1] < max_y

    filtered_antinode_positions = {}
    for antenna, antinodes in antinode_positions.items():
        if antenna not in filtered_antinode_positions:
            filtered_antinode_positions[antenna] = set()
        for antinode in antinodes:
            if point_is_within_bounds(antinode, max_x, max_y):
                filtered_antinode_positions[antenna].add(antinode)
    return filtered_antinode_positions


def get_antinode_positions_within_map(data):
    antenna_positions = _get_antenna_positions(data)
    antenna_position_pairs = _get_antenna_pairs(antenna_positions)
    antinode_positions = _get_antinode_positions(antenna_position_pairs)
    max_x, max_y = len(data), len(data[0])
    antinode_positions = _filter_antinode_positions_within_map(
        antinode_positions, max_x, max_y
    )
    return antinode_positions


def _convert_antinode_positions_to_map(antinode_positions, data):
    for antenna, antinodes in antinode_positions.items():
        for antinode in antinodes:
            if data[antinode[0]][antinode[1]] == ".":
                data[antinode[0]][antinode[1]] = "#"
    return data


def run_tests(test_cases):
    for data, solution in test_cases:
        antinode_positions = get_antinode_positions_within_map(data)
        result = _convert_antinode_positions_to_map(antinode_positions, data)
        success = True
        print(
            "solution",
            " " * (len(solution[0]) // 2 + (len(solution[0]) - len("solution"))),
            "result",
        )
        for row1, row2 in zip(solution, result):
            success = success and (row1 == row2)
            print("".join(row1), " " * (len(row1) // 2), "".join(row2))
        print(success)
        print()


if __name__ == "__main__":
    test_cases = setup_test_cases()
    run_tests(test_cases)

    data = [list(r.strip()) for r in data]

    antinode_positions = get_antinode_positions_within_map(data)

    s = 0
    for antenna, antinodes in antinode_positions.items():
        print(f"Antenna {antenna}: {len(antinodes)} antinodes")
        s += len(antinodes)
    print(f"Total antinodes: {s}")
