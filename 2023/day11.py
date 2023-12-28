from itertools import combinations
import unittest

# Parser function
def parse_universe(universe_str):
    lines = universe_str.strip().split('\n')
    galaxies = []
    empty_rows = set()
    empty_cols = set(range(len(lines[0])))

    for row_idx, line in enumerate(lines):
        row_has_galaxy = False
        for col_idx, char in enumerate(line):
            if char == '#':
                galaxies.append((row_idx, col_idx))
                row_has_galaxy = True
                empty_cols.discard(col_idx)

        if not row_has_galaxy:
            empty_rows.add(row_idx)

    return galaxies, empty_rows, empty_cols

# Function to calculate expanded distance
def calculate_expanded_distance(galaxy1, galaxy2, empty_rows, empty_cols, expansion_coefficient=2):
    row_distance = abs(galaxy1[0] - galaxy2[0])
    col_distance = abs(galaxy1[1] - galaxy2[1])

    # Adjust distances for cosmic expansion with scaling
    row_distance += sum((expansion_coefficient - 1) for r in range(min(galaxy1[0], galaxy2[0]), max(galaxy1[0], galaxy2[0])) if r in empty_rows)
    col_distance += sum((expansion_coefficient - 1) for c in range(min(galaxy1[1], galaxy2[1]), max(galaxy1[1], galaxy2[1])) if c in empty_cols)

    return row_distance + col_distance

# Function to calculate the sum of shortest paths
def sum_of_shortest_paths(galaxies, empty_rows, empty_cols, expansion_coefficient=2):
    total_sum = 0
    for galaxy1, galaxy2 in combinations(galaxies, 2):
        distance = calculate_expanded_distance(galaxy1, galaxy2, empty_rows, empty_cols, expansion_coefficient)
        total_sum += distance
    return total_sum

# Updated calculate_distance function
def calculate_distance(galaxy1, galaxy2, empty_rows, empty_cols):
    return calculate_expanded_distance(galaxy1, galaxy2, empty_rows, empty_cols, expansion_coefficient=1)

# Test class for Cosmic Expansion
class TestCosmicExpansion(unittest.TestCase):
    def test_parse_universe(self):
        input_str = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
        expected_galaxies = [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
        expected_empty_rows = {3, 7}
        expected_empty_cols = {2, 5, 8}
        result = parse_universe(input_str)
        self.assertEqual(result, (expected_galaxies, expected_empty_rows, expected_empty_cols))

    def test_calculate_distance(self):
        galaxy1 = (0, 3)
        galaxy2 = (4, 6)
        empty_rows = {3, 7}
        empty_cols = {2, 5, 8}
        expected_distance = 7  # |0 - 4| + |3 - 6|
        result = calculate_distance(galaxy1, galaxy2, empty_rows, empty_cols)
        self.assertEqual(result, expected_distance)

    def test_sum_of_shortest_paths(self):
        galaxies = [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
        empty_rows = {3, 7}
        empty_cols = {2, 5, 8}
        expected_sum = 374
        result = sum_of_shortest_paths(galaxies, empty_rows, empty_cols)
        self.assertEqual(result, expected_sum)

    def test_sum_of_shortest_paths_with_coefficient_10(self):
        galaxies = [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
        empty_rows = {3, 7}
        empty_cols = {2, 5, 8}
        expected_sum = 1030
        result = sum_of_shortest_paths(galaxies, empty_rows, empty_cols, expansion_coefficient=10)
        self.assertEqual(result, expected_sum)

    def test_real_input(self):
        file_path = 'input11.txt'

        with open(file_path, 'r') as file:
            puzzle_input = file.read()

        # Parsing the input and calculating the sum of shortest paths
        galaxies, empty_rows, empty_cols = parse_universe(puzzle_input)

        sum_paths = sum_of_shortest_paths(galaxies, empty_rows, empty_cols)
        self.assertEqual(sum_paths, 9521776) # Part One

        sum_paths = sum_of_shortest_paths(galaxies, empty_rows, empty_cols, 1000000)
        self.assertEqual(sum_paths, 553224415344) # Part Two

unittest.main()
