import unittest

class TestParabolicReflectorDish(unittest.TestCase):
    def test_parse_input(self):
        test_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
        expected = [
            ['O', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
            ['O', '.', 'O', 'O', '#', '.', '.', '.', '.', '#'],
            ['.', '.', '.', '.', '.', '#', '#', '.', '.', '.'],
            ['O', 'O', '.', '#', 'O', '.', '.', '.', '.', 'O'],
            ['.', 'O', '.', '.', '.', '.', '.', 'O', '#', '.'],
            ['O', '.', '#', '.', '.', 'O', '.', '#', '.', '#'],
            ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O'],
            ['.', '.', '.', '.', '.', '.', '.', 'O', '.', '.'],
            ['#', '.', '.', '.', '.', '#', '#', '#', '.', '.'],
            ['#', 'O', 'O', '.', '.', '#', '.', '.', '.', '.']
        ]
        result = parse_input(test_input)
        self.assertEqual(result, expected)

    def test_transpose(self):
        grid = [
            ['O', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
            ['O', '.', 'O', 'O', '#', '.', '.', '.', '.', '#'],
            ['.', '.', '.', '.', '.', '#', '#', '.', '.', '.'],
            ['O', 'O', '.', '#', 'O', '.', '.', '.', '.', 'O'],
            ['.', 'O', '.', '.', '.', '.', '.', 'O', '#', '.'],
            ['O', '.', '#', '.', '.', 'O', '.', '#', '.', '#'],
            ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O'],
            ['.', '.', '.', '.', '.', '.', '.', '.', 'O', '.'],
            ['#', '.', '.', '.', '.', '#', '#', '#', '.', '.'],
            ['#', 'O', 'O', '.', '.', '#', '.', '.', '.', '.']
        ]
        expected = [
            ['O', 'O', '.', 'O', '.', 'O', '.', '.', '#', '#'],
            ['.', '.', '.', 'O', 'O', '.', '.', '.', '.', 'O'],
            ['.', 'O', '.', '.', '.', '#', 'O', '.', '.', 'O'],
            ['.', 'O', '.', '#', '.', '.', '.', '.', '.', '.'],
            ['.', '#', '.', 'O', '.', '.', '.', '.', '.', '.'],
            ['#', '.', '#', '.', '.', 'O', '#', '.', '#', '#'],
            ['.', '.', '#', '.', '.', '.', 'O', '.', '#', '.'],
            ['.', '.', '.', '.', 'O', '#', '.', '.', '#', '.'],
            ['.', '.', '.', '.', '#', '.', '.', 'O', '.', '.'],
            ['.', '#', '.', 'O', '.', '#', 'O', '.', '.', '.']
        ]
        result = transpose(grid)
        self.assertEqual(result, expected)

    def test_shift_line_left(self):
        test_cases = [
            ("OO..", "OO.."),
            (".O.O", "OO.."),
            ("..O.", "O..."),
            (".O#.O", "O.#O."),
            ("O.O.#.#..O.O", "OO..#.#OO...")
        ]

        for input_line, expected in test_cases:
            with self.subTest():
                result = ''.join(shift_line_left(list(input_line)))
                self.assertEqual(result, expected)

    def test_calculate_load(self):
        test_cases = [
            ("O.", 2),
            ("O..", 3),
            ("OO.", 5),
            (".#O", 1),
            ("O#O", 4),
            ("OO..#.#OO...", 32)
        ]

        for line, expected_load in test_cases:
            with self.subTest(line=line):
                result = calculate_load(list(line))
                self.assertEqual(result, expected_load)

    def test_shift_and_calculate(self):
        test_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
        expected_output = 136

        total_load = shift_and_calculate(test_input)

        self.assertEqual(total_load, expected_output)

    def test_rotate_and_calculate(self):
        test_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
        expected_output = 64

        total_load = rotate_and_calculate(test_input,1000000000)

        self.assertEqual(total_load, expected_output)

    def test_turn_clockwise(self):
        input_matrix = [
            ['O', 'O', '#'],
            ['#', '.', 'O'],
            ['.', '#', '.']
        ]
        expected = [
            ['.', '#', 'O'],
            ['#', '.', 'O'],
            ['.', 'O', '#']
        ]
        result = turn_clockwise(input_matrix)
        self.assertEqual(result, expected)

    def test_turn_counterclockwise(self):
        input_matrix = [
            ['O', 'O', '#'],
            ['#', '.', 'O'],
            ['.', '#', '.']
        ]
        expected = [
            ['#', 'O', '.'],
            ['O', '.', '#'],
            ['O', '#', '.']
        ]
        result = turn_counterclockwise(input_matrix)
        self.assertEqual(result, expected)

    def test_puzzle_results(self):
        with open('input14.txt', 'r') as file:
            input_data = file.read()

            total_load_1 = shift_and_calculate(input_data)
            self.assertEqual(total_load_1, 110779)

            total_load_2 = rotate_and_calculate(input_data, 1000000000)
            self.assertEqual(total_load_2, 86069)

def reverse(matrix):
    return [row[::-1] for row in matrix]

def turn_clockwise(matrix):
    return reverse(transpose(matrix))

def turn_counterclockwise(matrix):
    return transpose(reverse(matrix))


def shift_and_calculate(input):
    # Parsing the input
    grid = parse_input(input)

    # Transposing the grid to handle columns as rows
    transposed_grid = transpose(grid)

    # Shifting all lines to the left
    shifted_grid = [shift_line_left(row) for row in transposed_grid]

    # Calculating the total load
    total_load = sum(calculate_load(row) for row in shifted_grid)

    return total_load

def rotate_and_calculate(input,count):
    platform = turn_counterclockwise(parse_input(input))
    cache = {}
    loads = [sum(calculate_load(row) for row in platform)]
    i = 0
    while True:
        for _ in range(4):
            platform = [shift_line_left(row) for row in platform]
            platform = turn_clockwise(platform)
        platform_text = "\n".join([ ''.join(l) for l in platform])
        total_load = sum(calculate_load(row) for row in platform)
        loads.append(total_load)

        if platform_text in cache:
            first = cache[platform_text]
            loop_length = i - first
            return loads[(count - first) % loop_length + first]

        cache[platform_text] = i
        i += 1


def calculate_load(line):
    load = 0
    length = len(line)
    for i, char in enumerate(line):
        if char == 'O':
            # Load is calculated based on the distance from the end of the line
            load += length - i
    return load



def shift_line_left(line):
    # Split the line at '#' as rocks will not pass these
    segments = ''.join(line).split('#')
    shifted_segments = []

    for segment in segments:
        # Count the number of 'O' and create a new segment with 'O's shifted to the left
        count_o = segment.count('O')
        new_segment = 'O' * count_o + '.' * (len(segment) - count_o)
        shifted_segments.append(new_segment)

    # Join the segments back together with '#'
    return list('#'.join(shifted_segments))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def parse_input(input_str):
    return [list(line) for line in input_str.strip().split('\n')]

if __name__ == '__main__':
    unittest.main()