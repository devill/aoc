import unittest

class TestLavaProduction(unittest.TestCase):
    def test_parse_input(self):
        test_string = """..\/.
./-|.
\../.
/..\.
.-.|.
"""
        expected_output = [
            list("..\/."),
            list("./-|."),
            list("\../."),
            list("/..\."),
            list(".-.|.")
        ]
        result = parse_input(test_string)
        self.assertEqual(result, expected_output)

    def test_find_energized(self):
        test_input = [
            list(".|...\\...."),
            list("|.-.\\....."),
            list(".....|-..."),
            list("........|."),
            list(".........."),
            list(".........\\"),
            list("..../.\\\\.."),
            list(".-.-/..|.."),
            list(".|....-|.\\"),
            list("..//.|....")
        ]
        energized = find_energized(test_input)
        expected = [
            list("######...."),
            list(".#...#...."),
            list(".#...#####"),
            list(".#...##..."),
            list(".#...##..."),
            list(".#...##..."),
            list(".#..####.."),
            list("########.."),
            list(".#######.."),
            list(".#...#.#..")
        ]
        self.assertEqual(energized, expected)

    def test_part_one(self):
        test_input = [
            list(".|...\\...."),
            list("|.-.\\....."),
            list(".....|-..."),
            list("........|."),
            list(".........."),
            list(".........\\"),
            list("..../.\\\\.."),
            list(".-.-/..|.."),
            list(".|....-|.\\"),
            list("..//.|....")
        ]
        count = get_energized_count(test_input)
        self.assertEqual(count, 46)

    def test_part_two(self):
        test_input = [
            list(".|...\\...."),
            list("|.-.\\....."),
            list(".....|-..."),
            list("........|."),
            list(".........."),
            list(".........\\"),
            list("..../.\\\\.."),
            list(".-.-/..|.."),
            list(".|....-|.\\"),
            list("..//.|....")
        ]
        count = get_maximum_energized_count(test_input)
        self.assertEqual(count, 51)

    def test_part_one_real_data(self):
        with open('input16.txt', 'r') as file:
            content = parse_input(file.read().strip())
            count = get_energized_count(content)
            self.assertEqual(count, 7496)

    # @unittest.skip("skip for now")
    def test_part_two_real_data(self):
        with open('input16.txt', 'r') as file:
            content = parse_input(file.read().strip())
            count = get_maximum_energized_count(content)
            self.assertEqual(count, 7932)

def parse_input(input_string):
    return [list(row) for row in input_string.split('\n') if row]

# Updating constants with direction values
HEADING_EAST = (1, 0)
HEADING_WEST = (-1, 0)
HEADING_NORTH = (0, -1)
HEADING_SOUTH = (0, 1)

tile_mapping = {
    (HEADING_EAST, '/'): [HEADING_NORTH],
    (HEADING_EAST, '\\'): [HEADING_SOUTH],
    (HEADING_EAST, '|'): [HEADING_NORTH, HEADING_SOUTH],

    (HEADING_WEST, '/'): [HEADING_SOUTH],
    (HEADING_WEST, '\\'): [HEADING_NORTH],
    (HEADING_WEST, '|'): [HEADING_NORTH, HEADING_SOUTH],

    (HEADING_SOUTH, '/'): [HEADING_WEST],
    (HEADING_SOUTH, '\\'): [HEADING_EAST],
    (HEADING_SOUTH, '-'): [HEADING_EAST, HEADING_WEST],

    (HEADING_NORTH, '/'): [HEADING_EAST],
    (HEADING_NORTH, '\\'): [HEADING_WEST],
    (HEADING_NORTH, '-'): [HEADING_EAST, HEADING_WEST],

}

def find_energized(grid, initial = ((0, 0), HEADING_EAST)):
    explorable = [initial]
    seen = {initial}

    while explorable:
        (x, y), heading = explorable.pop(0)
        current_tile = grid[y][x]
        next_headings = [heading]
        if (heading, current_tile) in tile_mapping:
            next_headings = tile_mapping[(heading, current_tile)]

        for next_heading in next_headings:
            new_x, new_y = x + next_heading[0], y + next_heading[1]
            next_pos = (new_x, new_y)
            if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[new_y]) and (next_pos, next_heading) not in seen:
                explorable.append((next_pos, next_heading))
                seen.add((next_pos, next_heading))

    # Create a result array of the same size as the grid, initialized with '.'
    result = [['.' for _ in row] for row in grid]
    for (x, y), _ in seen:
        result[y][x] = '#'

    return result

def get_energized_count(grid, initial = ((0, 0), HEADING_EAST)):
    energized_tiles = find_energized(grid, initial)
    # print("\n".join([''.join(l) for l in energized_tiles]))
    return sum(row.count('#') for row in energized_tiles)

def get_maximum_energized_count(grid):
    # Define the possible starting positions and corresponding headings
    rows, cols = len(grid), len(grid[0])
    start_positions = [
                          ((col, 0), HEADING_SOUTH) for col in range(cols)  # Top row, heading downward
                      ] + [
                          ((col, rows - 1), HEADING_NORTH) for col in range(cols)  # Bottom row, heading upward
                      ] + [
                          ((0, row), HEADING_EAST) for row in range(1, rows - 1)  # Left column, heading right
                      ] + [
                          ((cols - 1, row), HEADING_WEST) for row in range(1, rows - 1)  # Right column, heading left
                      ]

    # Iterate over each starting position and heading
    max_count = 0
    for initial in start_positions:
        energized_count = get_energized_count(grid, initial)
        # print(initial, energized_count)
        max_count = max(max_count, energized_count)

    return max_count


if __name__ == '__main__':
    unittest.main()
