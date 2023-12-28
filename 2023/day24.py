import unittest


TEST_DIRECTORY = ''

def get_data(file_name):
    with open(TEST_DIRECTORY + file_name, 'r') as file:
        return file.read()

class TestHailstoneParser(unittest.TestCase):

    def test_parse_hailstone_data(self):
        test_input = (
            "19, 13, 30 @ -2,  1, -2\n"
            "18, 19, 22 @ -1, -1, -2\n"
            "20, 25, 34 @ -2, -2, -4\n"
            "12, 31, 28 @ -1, -2, -1\n"
            "20, 19, 15 @  1, -5, -3\n"
        )
        expected_output = [
            {'p': (19, 13, 30), 'v': (-2,  1, -2)},
            {'p': (18, 19, 22), 'v': (-1, -1, -2)},
            {'p': (20, 25, 34), 'v': (-2, -2, -4)},
            {'p': (12, 31, 28), 'v': (-1, -2, -1)},
            {'p': (20, 19, 15), 'v': ( 1, -5, -3)},
        ]
        self.assertEqual(parse_hailstone_data(test_input), expected_output)

def parse_hailstone_data(data):
    hailstones = []
    for line in data.strip().split('\n'):
        parts = line.split('@')
        position = tuple(map(int, parts[0].strip().split(', ')))
        velocity = tuple(map(int, parts[1].strip().split(', ')))
        hailstones.append({'p': position, 'v': velocity})
    return hailstones


class TestHailstoneIntersection(unittest.TestCase):

    def test_hailstone_intersection(self):
        hailstone1 = {'p': (18, 19, 22), 'v': (-1, -1, -2)}
        hailstone2 = {'p': (12, 31, 28), 'v': (-1, -2, -1)}
        expected_output = (-6, -5)
        self.assertEqual(find_hailstone_intersection(hailstone1, hailstone2), expected_output)


def find_hailstone_intersection(hailstone1, hailstone2):
    p_a, v_a = hailstone1['p'], hailstone1['v']
    p_b, v_b = hailstone2['p'], hailstone2['v']

    # Solving the system of linear equations
    a = v_a[0]
    b = -v_b[0]
    e = v_a[1]
    f = -v_b[1]
    c = p_b[0] - p_a[0]
    d = p_b[1] - p_a[1]

    denominator = a * f - e * b
    if denominator == 0:
        return None  # Parallel paths or identical paths, no unique intersection point

    ta = (c * f - d * b) / denominator
    intersection_x = p_a[0] + v_a[0] * ta
    intersection_y = p_a[1] + v_a[1] * ta

    return (intersection_x, intersection_y)


class TestIntersectionCount(unittest.TestCase):

    def test_count_intersections_in_box(self):
        hailstones = [
            {'p': (19, 13, 30), 'v': (-2,  1, -2)},
            {'p': (18, 19, 22), 'v': (-1, -1, -2)},
            {'p': (20, 25, 34), 'v': (-2, -2, -4)},
            {'p': (12, 31, 28), 'v': (-1, -2, -1)},
            {'p': (20, 19, 15), 'v': ( 1, -5, -3)}
        ]
        min_coords = (7, 7)
        max_coords = (27, 27)
        expected_count = 2  # Based on the example provided
        self.assertEqual(count_intersections_in_box(hailstones, min_coords, max_coords), expected_count)

def count_intersections_in_box(hailstones, min_coords, max_coords):
    def is_within_box(point, min_coords, max_coords):
        return min_coords[0] <= point[0] <= max_coords[0] and min_coords[1] <= point[1] <= max_coords[1]

    def is_valid_intersection(hailstone1, hailstone2, intersection):
        # Ensure the paths do not intersect in the past
        t_a = (intersection[0] - hailstone1['p'][0]) / hailstone1['v'][0] if hailstone1['v'][0] != 0 else float('inf')
        t_b = (intersection[0] - hailstone2['p'][0]) / hailstone2['v'][0] if hailstone2['v'][0] != 0 else float('inf')
        return t_a >= 0 and t_b >= 0

    count = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            intersection = find_hailstone_intersection(hailstones[i], hailstones[j])
            if intersection and is_within_box(intersection, min_coords, max_coords) and is_valid_intersection(hailstones[i], hailstones[j], intersection):
                count += 1
    return count

class TestSolvePartOne(unittest.TestCase):

    def test_end_to_end(self):
        hailstones = parse_hailstone_data(get_data('test24.txt'))
        min_coords = (7, 7)
        max_coords = (27, 27)
        # Based on the example provided
        self.assertEqual(count_intersections_in_box(hailstones, min_coords, max_coords), 2)


    def test_solve(self):
        hailstones = parse_hailstone_data(get_data('input24.txt'))
        min_coords = (200000000000000, 200000000000000)
        max_coords = (400000000000000, 400000000000000)
        self.assertEqual(count_intersections_in_box(hailstones, min_coords, max_coords), 14046)

