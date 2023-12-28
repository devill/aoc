import unittest

TEST_DIRECTORY = ''

class TestSandSlabs(unittest.TestCase):
    def get_data(self, file_name):
        with open(TEST_DIRECTORY + file_name, 'r') as file:
            return file.read()

    def test_parse_input(self):
        test_input = (
            "1,0,1~1,2,1\n"
            "0,0,2~2,0,2\n"
            "0,2,3~2,2,3\n"
            "0,0,4~0,2,4\n"
            "2,0,5~2,2,5\n"
            "0,1,6~2,1,6\n"
            "1,1,8~1,1,9\n"
        )
        expected = [
            ((1, 0, 1), (1, 2, 1)),
            ((0, 0, 2), (2, 0, 2)),
            ((0, 2, 3), (2, 2, 3)),
            ((0, 0, 4), (0, 2, 4)),
            ((2, 0, 5), (2, 2, 5)),
            ((0, 1, 6), (2, 1, 6)),
            ((1, 1, 8), (1, 1, 9))
        ]
        result = parse_input(test_input)
        self.assertEqual(result, expected)

    def test_dependency_distance(self):
        test_cases = [
            { 'name': 'non_overlapping', 'lower': ((1, 1, 1), (1, 2, 2)), 'upper': ((2, 1, 2), (2, 2, 4)), 'expected': None },
            { 'name': 'laying_on_top', 'lower': ((1, 1, 1), (1, 2, 2)), 'upper': ((1, 1, 3), (2, 2, 4)), 'expected': 0 },
            { 'name': 'above', 'lower': ((1, 1, 1), (1, 2, 2)), 'upper': ((1, 1, 5), (2, 2, 6)), 'expected': 2 }
        ]

        for case in test_cases:
            with self.subTest(name=case['name']):
                result = dependency_distance(case['lower'], case['upper'])
                self.assertEqual(result, case['expected'])

    def test_brick_dependencies(self):
        test_input = [
            ((1, 1, 1), (1, 2, 2)),
            ((2, 1, 2), (2, 2, 4)),
            ((1, 1, 10), (2, 2, 12))
        ]
        expected = [
            {-1: 0},  # Brick 0 depends on the ground with a distance of 0
            {-1: 1},  # Brick 1 depends on the ground with a distance of 1
            {-1: 9, 0: 7, 1: 5}  # Brick 2 depends on the ground (9), on brick 0 (8), and on brick 1 (6)
        ]
        result = calculate_dependencies(test_input)
        self.assertEqual(result, expected)

    def test_update_z_coordinates(self):
        bricks = [
            ((1, 1, 1), (1, 2, 2)),
            ((2, 1, 2), (2, 2, 4)),
            ((1, 1, 10), (2, 2, 12))
        ]
        expected = [
            ((1, 1, 1), (1, 2, 2)),
            ((2, 1, 1), (2, 2, 3)),
            ((1, 1, 4), (2, 2, 6))
        ]
        result = update_z_coordinates(bricks)
        self.assertEqual(result, expected)

    def test_update_z_coordinates_complex_case(self):
        bricks = [
            ((1, 0, 1), (1, 2, 1)),
            ((0, 0, 2), (2, 0, 2)),
            ((0, 2, 3), (2, 2, 3)),
            ((0, 0, 4), (0, 2, 4)),
            ((2, 0, 5), (2, 2, 5)),
            ((0, 1, 6), (2, 1, 6)),
            ((1, 1, 8), (1, 1, 9))
        ]
        sorted_bricks = sorted(bricks, key=lambda brick: brick[0][2])
        fallen_bricks = update_z_coordinates(sorted_bricks)
        expected = [
            ((1, 0, 1), (1, 2, 1)),
            ((0, 0, 2), (2, 0, 2)),
            ((0, 2, 2), (2, 2, 2)),
            ((0, 0, 3), (0, 2, 3)),
            ((2, 0, 3), (2, 2, 3)),
            ((0, 1, 4), (2, 1, 4)),
            ((1, 1, 5), (1, 1, 6))
        ]
        self.assertEqual(fallen_bricks, expected)

    def test_invert_dependencies(self):
        input_dependencies = [
            {-1: 0},  # Brick 0 depends on the ground with a distance of 0
            {-1: 1},  # Brick 1 depends on the ground with a distance of 1
            {-1: 9, 0: 7, 1: 5}  # Brick 2 depends on the ground (9), on brick 0 (8), and on brick 1 (6)
        ]
        expected_output = [
            {2: 7},  # The only brick depending on 0 is 2 with distance 7
            {2: 5},  # The only brick depending on 1 is 2 with distance 5
            {}  # No one depends on 2
        ]
        result = invert_dependencies(input_dependencies)
        self.assertEqual(result, expected_output)

    def test_find_safe_to_disintegrate(self):
        fallen_bricks = [
            ((1, 0, 1), (1, 2, 1)),
            ((0, 0, 2), (2, 0, 2)),
            ((0, 2, 2), (2, 2, 2)),
            ((0, 0, 3), (0, 2, 3)),
            ((2, 0, 3), (2, 2, 3)),
            ((0, 1, 4), (2, 1, 4)),
            ((1, 1, 5), (1, 1, 6))
        ]
        number_of_disintegratable = len(find_safe_to_disintegrate(fallen_bricks))
        self.assertEqual(number_of_disintegratable, 5)

    def test_end_to_end(self):
        data = self.get_data('test22.txt')
        bricks = parse_input(data)
        sorted_bricks = sorted(bricks, key=lambda brick: brick[0][2])
        fallen_bricks = update_z_coordinates(sorted_bricks)
        number_of_disintegratable = len(find_safe_to_disintegrate(fallen_bricks))
        self.assertEqual(number_of_disintegratable, 5)

        total_chains = sum([len(c) for c in find_chains(fallen_bricks)])
        self.assertEqual(total_chains, 7)

    # @unittest.skip("runs slow")
    def test_solve_puzzles(self):
        data = self.get_data('input22.txt')
        bricks = parse_input(data)
        sorted_bricks = sorted(bricks, key=lambda brick: brick[0][2])
        fallen_bricks = update_z_coordinates(sorted_bricks)

        # part one
        # original_disigrentable = find_safe_to_disintegrate(fallen_bricks)
        # number_of_disintegratable = len(original_disigrentable)
        # self.assertEqual(number_of_disintegratable, 482)

        chains = find_chains(fallen_bricks)

        # part one alternative solution
        disintegratable = [i for i, c in enumerate(chains) if len(c) == 0]
        self.assertEqual(len(disintegratable), 482)

        # part two
        total_chains = sum([len(c) for c in chains])
        self.assertEqual(total_chains, 103010)

    def test_find_direct_supported(self):
        fallen_bricks = [
            ((1, 0, 1), (1, 2, 1)),
            ((0, 0, 2), (2, 0, 2)),
            ((0, 2, 2), (2, 2, 2)),
            ((0, 0, 3), (0, 2, 3)),
            ((2, 0, 3), (2, 2, 3)),
            ((0, 1, 4), (2, 1, 4)),
            ((1, 1, 5), (1, 1, 6))
        ]
        result = find_direct_supported(fallen_bricks)
        self.assertEqual(result, [{1, 2}, {3, 4}, {3, 4}, {5}, {5}, {6}, set()])

    def test_find_direct_supporter(self):
        fallen_bricks = [
            ((1, 0, 1), (1, 2, 1)),
            ((0, 0, 2), (2, 0, 2)),
            ((0, 2, 2), (2, 2, 2)),
            ((0, 0, 3), (0, 2, 3)),
            ((2, 0, 3), (2, 2, 3)),
            ((0, 1, 4), (2, 1, 4)),
            ((1, 1, 5), (1, 1, 6))
        ]
        result = find_direct_supporter(fallen_bricks)
        self.assertEqual(result, [set(), {0}, {0}, {1, 2}, {1, 2}, {3, 4}, {5}])


    def test_find_chains(self):
        fallen_bricks = [
            ((1, 0, 1), (1, 2, 1)),
            ((0, 0, 2), (2, 0, 2)),
            ((0, 2, 2), (2, 2, 2)),
            ((0, 0, 3), (0, 2, 3)),
            ((2, 0, 3), (2, 2, 3)),
            ((0, 1, 4), (2, 1, 4)),
            ((1, 1, 5), (1, 1, 6))
        ]
        chains = find_chains(fallen_bricks)
        total_chains = sum([len(c) for c in chains])
        self.assertEqual(total_chains, 7)

def parse_input(data):
    bricks = []
    for line in data.strip().split('\n'):
        parts = line.split('~')
        brick = tuple(tuple(int(n) for n in part.split(',')) for part in parts)
        bricks.append(brick)
    return bricks

def dependency_distance(lower, upper):
    # Unpack the coordinates of the lower and upper bricks
    (lower_x1, lower_y1, lower_z1), (lower_x2, lower_y2, lower_z2) = lower
    (upper_x1, upper_y1, upper_z1), (upper_x2, upper_y2, upper_z2) = upper

    # Check if the bricks are aligned vertically
    if (upper_x1 <= lower_x2 and lower_x1 <= upper_x2) and (upper_y1 <= lower_y2 and lower_y1 <= upper_y2):
        return upper_z1 - lower_z2 - 1  # Distance between the two bricks
    return None  # No dependency if the bricks are not vertically aligned

def calculate_dependencies(bricks):
    dependencies = []
    for i, upper_brick in enumerate(bricks):
        # Initialize dependency map for each brick
        dependency_map = {-1: upper_brick[0][2] - 1}  # Dependency on the ground
        for j, lower_brick in enumerate(bricks):
            if i == j:
                continue  # Skip self-dependency
            distance = dependency_distance(lower_brick, upper_brick)
            if distance is not None and distance >= 0:
                dependency_map[j] = distance
        dependencies.append(dependency_map)
    return dependencies


def update_z_coordinates(bricks):
    dependencies = calculate_dependencies(bricks)
    updated_bricks = []

    for i, brick in enumerate(bricks):
        (x1, y1, z1), (x2, y2, z2) = brick
        # Calculate the maximum z2 of all dependencies
        max_z2 = max([updated_bricks[j][1][2] for j in dependencies[i] if j != -1], default=0)
        # Update the z-coordinates based on the maximum z2 found
        new_z1 = max_z2 + 1
        new_z2 = new_z1 + (z2 - z1)
        updated_bricks.append(((x1, y1, new_z1), (x2, y2, new_z2)))

    return updated_bricks

def invert_dependencies(dependencies):
    inverted = [{} for _ in range(len(dependencies))]
    for brick, deps in enumerate(dependencies):
        for dep, distance in deps.items():
            if dep != -1 :
                inverted[dep][brick] = distance
    return inverted

# def find_safe_to_disintegrate(fallen_bricks):
#     supported = find_direct_supported(fallen_bricks)
#     supporter = find_direct_supporter(fallen_bricks)
#
#     safe_to_disintegrate = []
#
#     for i, supporters in enumerate(supporter):
#         # Check if all bricks depending on this one with distance 0 have at least one other brick to depend on with distance 0
#         if all(len(supported[j]) >= 2 for j in supporters):
#             safe_to_disintegrate.append(i)
#
#     return safe_to_disintegrate

def find_safe_to_disintegrate(fallen_bricks):
    supporter = find_direct_supporter(fallen_bricks)
    supported = find_direct_supported(fallen_bricks)

    safe_to_disintegrate = []

    for i, _ in enumerate(fallen_bricks):
        if all(len(supporter[j]) >= 2 for j in supported[i]):
            safe_to_disintegrate.append(i)

    return safe_to_disintegrate


def find_direct_supporter(fallen_bricks):
    dependencies = calculate_dependencies(fallen_bricks)

    return [
        set([ k for k, v in b.items() if k != -1 and v == 0]) for b in dependencies
    ]


def find_direct_supported(fallen_bricks):
    dependencies = calculate_dependencies(fallen_bricks)
    inverted_dependencies = invert_dependencies(dependencies)

    return [
        set([ k for k, v in b.items() if v == 0]) for b in inverted_dependencies
    ]

def find_chains(fallen_bricks):
    supporter = find_direct_supporter(fallen_bricks)
    chains = []

    for i, disintegrated in enumerate(fallen_bricks):
        fallen = [i == j for j,_ in enumerate(fallen_bricks)]
        for bi in range(i + 1, len(fallen_bricks)):
            fallen[bi] = len(supporter[bi]) != 0 and all(fallen[s] for s in supporter[bi])

        fallen_set = set([index for index, f in enumerate(fallen) if f and index != i])
        chains.append(fallen_set)

    return chains


if __name__ == '__main__':
    unittest.main()
