import unittest
from collections import deque

TEST_DIRECTORY = ''

class TestStepCounter(unittest.TestCase):
    def test_parse_map(self):
        test_input = (
            "...........\n"
            ".....###.#.\n"
            ".###.##..#.\n"
            "..#.#...#..\n"
            "....#.#....\n"
            ".##..S####.\n"
            ".##..#...#.\n"
            ".......##..\n"
            ".##.#.####.\n"
            ".##..##.##.\n"
            "..........."
        )
        expected = [
            list("..........."),
            list(".....###.#."),
            list(".###.##..#."),
            list("..#.#...#.."),
            list("....#.#...."),
            list(".##..S####."),
            list(".##..#...#."),
            list(".......##.."),
            list(".##.#.####."),
            list(".##..##.##."),
            list("...........")
        ]
        result = parse_map(test_input)
        self.assertEqual(result, expected)

    def test_valid_steps(self):
        garden_map_data = [
            list("..........."),
            list(".....###.#."),
            list(".###.##..#."),
            list("..#.#...#.."),
            list("....#.#...."),
            list(".##..S####."),
            list(".##..#...#."),
            list(".......##.."),
            list(".##.#.####."),
            list(".##..##.##."),
            list("...........")
        ]
        garden_map = GardenMap(garden_map_data)
        position = (5, 5)  # 'S' position
        expected_neighbors = [(4, 5), (5, 4)]  # Valid neighboring positions
        self.assertEqual(set(garden_map.valid_steps(position)), set(expected_neighbors))

    def test_count_reachable_tiles(self):
        garden_map_data = [
            list("..........."),
            list(".....###.#."),
            list(".###.##..#."),
            list("..#.#...#.."),
            list("....#.#...."),
            list(".##..S####."),
            list(".##..#...#."),
            list(".......##.."),
            list(".##.#.####."),
            list(".##..##.##."),
            list("...........")
        ]
        garden_map = GardenMap(garden_map_data)
        steps = 6  # Number of steps
        expected_count = 29
        self.assertEqual(len(garden_map.reachable_tiles(steps)), expected_count)

    def get_data(self, file_name):
        with open(TEST_DIRECTORY + file_name, 'r') as file:
            return file.read()


    def test_solve_part_one(self):
        data = self.get_data('input21.txt')
        garden_map = GardenMap(parse_map(data))
        result = garden_map.end_points_after(64)
        self.assertEqual(len(result), 3687)

    def get_endpoint_set(self):
        end_points_map = [
            list("..........."),
            list(".....###.#."),
            list(".###.##.O#."),
            list(".O#O#O.O#.."),
            list("O.O.#.#.O.."),
            list(".##O.O####."),
            list(".##.O#O..#."),
            list(".O.O.O.##.."),
            list(".##.#.####."),
            list(".##O.##.##."),
            list("..........."),
        ]
        s = set()
        for y, l in enumerate(end_points_map):
            for x, t in enumerate(l):
                if t == 'O':
                    s.add((y, x))
        return s

    def test_end_points_after(self):
        garden_map_data = [
            list("..........."),
            list(".....###.#."),
            list(".###.##..#."),
            list("..#.#...#.."),
            list("....#.#...."),
            list(".##..S####."),
            list(".##..#...#."),
            list(".......##.."),
            list(".##.#.####."),
            list(".##..##.##."),
            list("...........")
        ]
        garden_map = GardenMap(garden_map_data)
        steps = 6  # Number of steps
        expected_count = 16  # Expected count of reachable tiles in 6 steps

        result = garden_map.end_points_after(steps)
        self.assertEqual(result, self.get_endpoint_set())
        self.assertEqual(len(result), expected_count)

    def test_get_starting_position(self):
        garden_map_data = [
            list("..........."),
            list(".....###.#."),
            list(".###.##..#."),
            list("..#.#...#.."),
            list("....#.#...."),
            list(".##..S####."),
            list(".##..#...#."),
            list(".......##.."),
            list(".##.#.####."),
            list(".##..##.##."),
            list("...........")
        ]
        garden_map = GardenMap(garden_map_data)
        expected_position = (5, 5)  # Coordinates (row, column) of 'S'
        self.assertEqual(garden_map.get_starting_position(), expected_position)

    def test_solve_part_two(self):
        map = self.get_data('test21.txt')
        garden_map_data = parse_map(map)
        garden_map = InfiniteGardenMap(garden_map_data)
        self.assertEqual(len(garden_map.end_points_after(6)), 16)
        self.assertEqual(len(garden_map.end_points_after(10)), 50)
        self.assertEqual(len(garden_map.end_points_after(50)), 1594)
        self.assertEqual(len(garden_map.end_points_after(100)), 6536)

    @unittest.skip("")
    def test_solve_part_two_real(self):
        map = self.get_data('input21.txt')
        garden_map_data = parse_map(map)
        garden_map = InfiniteGardenMap(garden_map_data)
        print(len(garden_map.end_points_after(65)))
        print(len(garden_map.end_points_after(262+65)))
        print(len(garden_map.end_points_after(2*262+65)))
        print(len(garden_map.end_points_after(3*262+65)))

    def test_c(self):
        values = [3778, 93438, 302402, 630670, 1078242]
        diffs = [values[i+1] - values[i] for i in range(4)]
        diffs2 = [diffs[i+1] - diffs[i] for i in range(3)]
        print(values, diffs, diffs2)

class GardenMap:
    def __init__(self, map_data):
        self.map_data = map_data

    def get_starting_position(self):
        for row_index, row in enumerate(self.map_data):
            if 'S' in row:
                return row_index, row.index('S')

    def valid_steps(self, position):
        row, col = position
        steps = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(self.map_data) and 0 <= new_col < len(self.map_data[0]):
                if self.map_data[new_row][new_col] == '.' or self.map_data[new_row][new_col] == 'S':
                    steps.append((new_row, new_col))
        return steps

    def reachable_tiles(self, steps, start_override = None):

        start = self.get_starting_position()
        if start_override:
            start = start_override

        visited = set([start])
        queue = deque([(start, 0)])

        while queue:
            position, step_count = queue.popleft()

            if step_count < steps:
                for next_step in self.valid_steps(position):
                    if next_step not in visited:
                        visited.add(next_step)
                        queue.append((next_step, step_count + 1))

        return set(visited)

    def end_points_after(self, steps):
        reachable = self.reachable_tiles(steps)
        start = self.get_starting_position()
        parity = (start[0] + start[1] + steps) % 2
        return set([tile for tile in reachable if (tile[0] + tile[1]) % 2 == parity])


class InfiniteGardenMap(GardenMap):
    def is_rock(self, row, col):
        mod_row = (row + len(self.map_data)) % len(self.map_data)
        mod_col = (col + len(self.map_data[mod_row])) % len(self.map_data[mod_row])
        return self.map_data[mod_row][mod_col] == '#'

    def valid_steps(self, position):
        row, col = position
        steps = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if not self.is_rock(new_row, new_col):
                steps.append((new_row, new_col))
        return steps

def parse_map(map_str):
    return [list(row) for row in map_str.strip('\n').split('\n')]


if __name__ == '__main__':
    unittest.main()