import unittest

TEST_DIRECTORY = '' # You may have to modify this line depending on where input18.txt is on your system

class TestLavaductLagoon(unittest.TestCase):
    _TEST_INPUT = "\n".join([
        "R 6 (#70c710)",
        "D 5 (#0dc571)",
        "L 2 (#5713f0)",
        "D 2 (#d2c081)",
        "R 2 (#59c680)",
        "D 2 (#411b91)",
        "L 5 (#8ceee2)",
        "U 2 (#caa173)",
        "L 1 (#1b58a2)",
        "U 2 (#caa171)",
        "R 2 (#7807d2)",
        "U 3 (#a77fa3)",
        "L 2 (#015232)",
        "U 2 (#7a21e3)",
        ""
    ])

    def get_data(self, file_name='input18.txt'):
        with open(TEST_DIRECTORY + file_name, 'r') as file:
            return file.read()

    def test_parse_input(self):
        expected_output = [
            ('R', 6),
            ('D', 5),
            ('L', 2),
            ('D', 2),
            ('R', 2),
            ('D', 2),
            ('L', 5),
            ('U', 2),
            ('L', 1),
            ('U', 2),
            ('R', 2),
            ('U', 3),
            ('L', 2),
            ('U', 2),
        ]
        result = parse_input(self._TEST_INPUT)
        self.assertEqual(result, expected_output)

    # @unittest.skip("refactoring first")
    def test_parse_hex_input(self):
        expected_output = [
            ('R', 0x70c71),
            ('D', 0x0dc57),
            ('R', 0x5713f),
            ('D', 0xd2c08),
            ('R', 0x59c68),
            ('D', 0x411b9),
            ('L', 0x8ceee),
            ('U', 0xcaa17),
            ('L', 0x1b58a),
            ('D', 0xcaa17),
            ('L', 0x7807d),
            ('U', 0xa77fa),
            ('L', 0x01523),
            ('U', 0x7a21e),
        ]
        result = parse_hex_input(self._TEST_INPUT)
        self.assertEqual(result, expected_output)

    def test_find_bounds(self):
        parsed_data = parse_input(self._TEST_INPUT)
        bounds = find_bounds(parsed_data)
        self.assertEqual(bounds, ((0, 6), (-9, 0)))

    def test_find_bounds_hex(self):
        parsed_data = parse_hex_input(self._TEST_INPUT)
        bounds = find_bounds(parsed_data)
        self.assertEqual(bounds, ((0, 1186328), (-1186328, 0)))

    def test_find_bounds_real_data(self):
        parsed_data = parse_input(self.get_data())
        bounds = find_bounds(parsed_data)
        self.assertEqual(bounds, ((0, 372), (-202, 144)))

    def test_calculate_winding_number(self):
        parsed_data = parse_input(self._TEST_INPUT)
        test_cases = [
            ((0,0), None),
            ((2,-2), None),
            ((1, -1), 1),
            ((1, -3), 0)
        ]
        for point, expected_winding_number in test_cases:
            with self.subTest(name=point):
                self.assertEqual(calculate_winding_number(parsed_data, point), expected_winding_number)

    def test_count_lava_containment_points(self):
        # print("test_count_lava_containment_points")
        parsed_data = parse_input(self._TEST_INPUT)
        count = count_lava_containment_points(parsed_data)
        expected_count = 62  # Based on the example from the puzzle description
        self.assertEqual(count, expected_count)

    def test_count_lava_containment_points_hex(self):
        # print("test_count_lava_containment_points_hex")
        parsed_data = parse_hex_input(self._TEST_INPUT)
        count = count_lava_containment_points(parsed_data)
        expected_count = 952408144115  # Based on the example from the puzzle description
        self.assertEqual(count, expected_count)

    def test_extract_vertex_coordinates(self):
        parsed_data = parse_input(self._TEST_INPUT)
        x_coords, y_coords = extract_vertex_coordinates(parsed_data)
        expected_x_coords = [0, 1, 2, 4, 6]
        expected_y_coords = [-9, -7, -5, -2, 0]
        self.assertEqual(x_coords, expected_x_coords)
        self.assertEqual(y_coords, expected_y_coords)

    def test_extract_vertex_coordinates_real_data(self):
        parsed_data = parse_input(self.get_data())
        x_coords, y_coords = extract_vertex_coordinates(parsed_data)
        self.assertEqual(len(x_coords), 221)
        self.assertEqual(len(y_coords), 214)

    def test_extract_vertex_coordinates_real_data_hex(self):
        parsed_data = parse_hex_input(self.get_data())
        x_coords, y_coords = extract_vertex_coordinates(parsed_data)
        self.assertEqual(len(x_coords), 324)
        self.assertEqual(len(y_coords), 313)

    # @unittest.skip("Slow, only run if necessary")
    def test_count_lava_containment_points_real_data(self):
        # print("test_count_lava_containment_points_real_data")
        parsed_data = parse_input(self.get_data())
        count = count_lava_containment_points(parsed_data)
        expected_count = 40761  # Solution to part one
        self.assertEqual(count, expected_count)

    # @unittest.skip("Slow for now, only run if necessary")
    def test_count_lava_containment_points_real_data_hex(self):
        # print("test_count_lava_containment_points_real_data_hex")
        parsed_data = parse_hex_input(self.get_data())
        count = count_lava_containment_points(parsed_data)
        expected_count = 106920098354636  # Solution to part two
        self.assertEqual(count, expected_count)


    def test_count_lava_containment_points_empty_steps(self):
        # print("test_count_lava_containment_points_empty_steps")
        parsed_data = []
        expected_area = 1  # The initial 0,0 point
        calculated_area = count_lava_containment_points(parsed_data)
        self.assertEqual(calculated_area, expected_area)

    def test_count_lava_containment_points_simple_rectangle(self):
        # print("test_count_lava_containment_points_simple_rectangle")
        parsed_data = [
            ('R', 6),
            ('D', 2),
            ('L', 6),
            ('U', 2)
        ]
        expected_area = 21  # 7x3 rectangle
        calculated_area = count_lava_containment_points(parsed_data)
        self.assertEqual(calculated_area, expected_area)

    def test_count_lava_containment_points_irregular_shape(self):
        # print("test_count_lava_containment_points_irregular_shape")
        parsed_data = [
            ('R', 2),
            ('D', 2),
            ('R', 2),
            ('U', 2),
            ('R', 2),
            ('D', 6),
            ('L', 2),
            ('D', 2),
            ('L', 2),
            ('U', 2),
            ('L', 2),
            ('U', 6)
        ]
        expected_area = 53  # 7x7 square with two removed and 6 added
        calculated_area = count_lava_containment_points(parsed_data)
        self.assertEqual(calculated_area, expected_area)

def extract_vertex_coordinates(parsed_data):
    x_coords, y_coords = set(), set()
    x = y = 0

    # Adding initial point
    x_coords.add(x)
    y_coords.add(y)

    for direction, distance in parsed_data:
        if direction == 'R':
            x += distance
        elif direction == 'L':
            x -= distance
        elif direction == 'U':
            y += distance
        elif direction == 'D':
            y -= distance

        # Adding vertex coordinates
        x_coords.add(x)
        y_coords.add(y)

    # Returning sorted lists
    return sorted(x_coords), sorted(y_coords)

opposing = {
    'R': 'L',
    'L': 'R',
    'D': 'U',
    'U': 'D',
}

def count_lava_containment_points(parsed_data):
    if len(parsed_data) == 0:
        return 1

    (min_x, max_x), (min_y, max_y) = find_bounds(parsed_data)
    x = -min_x
    y = -min_y
    area = 0
    # print('')

    for i, (direction, distance) in enumerate(parsed_data):
        next_move = parsed_data[(i+1) % len(parsed_data)][0]
        previous_move = parsed_data[i - 1][0]

        if direction == next_move or opposing[direction] == next_move:
            print("Unexpceted move")
            return None

        # print(f"{direction}, {distance}; ({x},{y})")
        if direction == 'R':
            x += distance
            area += (distance - 1) * (y + 1)

        elif direction == 'L':
            x -= distance
            area -= (distance - 1) * y

        elif direction == 'U':
            y += distance
            if previous_move == 'R':
                if next_move == 'R':
                    area += y + 1
                else:
                    area += 0
            else:
                if next_move == 'R':
                    area += distance + 1
                else:
                    area += -(y - distance)

        elif direction == 'D':
            y -= distance
            if previous_move == 'R':
                if next_move == 'R':
                    area += y + distance + 1
                else:
                    area += distance + 1
            else:
                if next_move == 'R':
                    area += 0
                else:
                    area += -y

        #print(area)

    # print('---')
    return area


def sign(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0

def calculate_winding_number(parsed_data, point):
    if point == (0, 0):
        return None # We start here, so it is always on the boundary

    x, y = point

    path_x, path_y = 0, 0

    winding_number = 0

    last_side = None
    if x < path_x:
        if y < path_y:
            last_side = 'above'
        if y > path_y:
            last_side = 'below'

    for direction, distance in parsed_data:
        previous_x, previous_y = path_x, path_y
        if direction == 'R':
            path_x += distance
        elif direction == 'L':
            path_x -= distance
        elif direction == 'U':
            path_y += distance
        elif direction == 'D':
            path_y -= distance

        if x == path_x == previous_x and sign(path_y - y) != sign(previous_y - y):
            return None # point on vertical boundary

        if y == path_y == previous_y and sign(path_x - x) != sign(previous_x - x):
            return None # point on horizontal boundary

        new_side = None
        if x < path_x:
            if y < path_y:
                new_side = 'above'
            if y > path_y:
                new_side = 'below'

        if last_side != None and new_side != None and last_side != new_side:
            winding_number += 1

        if y != path_y:
            last_side = new_side

    return winding_number % 2

def find_bounds(parsed_data):
    min_x = min_y = max_x = max_y = 0
    x = y = 0
    for direction, distance in parsed_data:
        if direction == 'R':
            x += distance
        elif direction == 'L':
            x -= distance
        elif direction == 'U':
            y += distance
        elif direction == 'D':
            y -= distance
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    return (min_x, max_x), (min_y, max_y)


def parse_input(input_str):
    lines = input_str.strip('\n').split('\n')
    parsed_data = []
    for line in lines:
        parts = line.split(' ')
        direction = parts[0]
        distance = int(parts[1])
        parsed_data.append((direction, distance))
    return parsed_data

def parse_hex_input(input_str):
    lines = input_str.strip('\n').split('\n')
    parsed_data = []
    dir_mapping = ['R','D','L','U']
    for line in lines:
        parts = line.split(' ')
        direction = dir_mapping[int(parts[2][-2])]
        distance = int(parts[2][2:-2], 16)
        parsed_data.append((direction, distance))
    return parsed_data


unittest.main()
