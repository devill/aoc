import unittest
import heapq

TEST_DIRECTORY = ''

class TestCruciblePathfinder(unittest.TestCase):
    def test_parse_input(self):
        test_input = "321\n456\n987"
        expected = [[3, 2, 1], [4, 5, 6], [9, 8, 7]]
        result = parse_input(test_input)
        self.assertEqual(result, expected)

class TestLavaMapHelpers(unittest.TestCase):
    def test_turn_left(self):
        self.assertEqual(turn_left(HEADING_NORTH), HEADING_WEST)
        self.assertEqual(turn_left(HEADING_WEST), HEADING_SOUTH)
        self.assertEqual(turn_left(HEADING_SOUTH), HEADING_EAST)
        self.assertEqual(turn_left(HEADING_EAST), HEADING_NORTH)

    def test_turn_right(self):
        self.assertEqual(turn_right(HEADING_NORTH), HEADING_EAST)
        self.assertEqual(turn_right(HEADING_EAST), HEADING_SOUTH)
        self.assertEqual(turn_right(HEADING_SOUTH), HEADING_WEST)
        self.assertEqual(turn_right(HEADING_WEST), HEADING_NORTH)

class TestLavaMap(unittest.TestCase):
    def test_next_steps(self):
        lava_map_data = [[1, 1, 2], [2, 1, 2], [2, 1, 1]]
        lava_map = LavaMap(lava_map_data)
        current_step = ((1, 1), HEADING_SOUTH, 1) # Format: position, heading, number of straight steps
        expected_next_steps = [
            (2, ((2, 1), HEADING_EAST , 1)),  # turn left
            (1, ((1, 2), HEADING_SOUTH, 2)),  # continue straight
            (2, ((0, 1), HEADING_WEST , 1))   # turn right
        ]
        self.assertEqual(lava_map.next_steps(current_step), expected_next_steps)

    def test_next_steps_after_3_straight(self):
        lava_map_data = [[1, 1, 2], [2, 1, 2], [2, 1, 1]]
        lava_map = LavaMap(lava_map_data)
        current_step = ((1, 1), HEADING_SOUTH, 3) # Format: position, heading, number of straight steps
        expected_next_steps = [
            (2, ((2, 1), HEADING_EAST , 1)),  # turn left
            # straight missing, because it would be the 4th step in the same direction
            (2, ((0, 1), HEADING_WEST , 1))   # turn right
        ]
        self.assertEqual(lava_map.next_steps(current_step), expected_next_steps)

    def test_get_initial_moves(self):
        lava_map_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        lava_map = LavaMap(lava_map_data)
        expected_initial_moves = [
            (0, ((0, 0), HEADING_EAST, 0)),
            (0, ((0, 0), HEADING_SOUTH, 0))
        ]
        self.assertEqual(lava_map.get_initial_moves(), expected_initial_moves)

    def test_is_at_goal(self):
        lava_map_data = [[1, 2], [3, 4]]
        lava_map = LavaMap(lava_map_data)
        self.assertTrue(lava_map.is_at_goal(((1, 1), HEADING_EAST, 1)))
        self.assertFalse(lava_map.is_at_goal(((0, 1), HEADING_WEST, 1)))

class TestUltraCrucibleMap(unittest.TestCase):
    def test_next_steps_min_straight(self):
        # Test the minimum straight movement constraint
        map_data = [[1, 1, 2], [2, 1, 2], [2, 1, 1]]
        ultra_map = UltraCrucibleMap(map_data)
        current_step = ((1, 1), HEADING_SOUTH, 3)  # Less than MIN_STRAIGHT
        expected_next_steps = [
            # No turns should be available, only straight movement
            (1, ((1, 2), HEADING_SOUTH, 4)),
        ]
        self.assertEqual(ultra_map.next_steps(current_step), expected_next_steps)

    def test_next_steps_max_straight(self):
        # Test the maximum straight movement constraint
        map_data = [[1, 1, 2], [2, 1, 2], [2, 1, 1]]
        ultra_map = UltraCrucibleMap(map_data)
        current_step = ((1, 1), HEADING_SOUTH, 10)  # Equals MAX_STRAIGHT
        expected_next_steps = [
            # Only turns should be available, no straight movement
            (2, ((2, 1), HEADING_EAST, 1)),
            (2, ((0, 1), HEADING_WEST, 1)),
        ]
        self.assertEqual(ultra_map.next_steps(current_step), expected_next_steps)

    def test_next_steps_all_moves_available(self):
        # Test the maximum straight movement constraint
        map_data = [[1, 1, 2], [2, 1, 2], [2, 1, 1]]
        ultra_map = UltraCrucibleMap(map_data)
        current_step = ((1, 1), HEADING_SOUTH, 5)  # Equals MAX_STRAIGHT
        expected_next_steps = [
            (2, ((2, 1), HEADING_EAST, 1)),
            (2, ((0, 1), HEADING_WEST, 1)),
            (1, ((1, 2), HEADING_SOUTH, 6)),
        ]
        self.assertEqual(ultra_map.next_steps(current_step), expected_next_steps)

    def test_is_at_goal_straight_requirement(self):
        map_data = [[1, 1], [1, 1]]
        ultra_map = UltraCrucibleMap(map_data)
        # Position at goal but not enough straight steps
        self.assertFalse(ultra_map.is_at_goal(((1, 1), HEADING_EAST, 3)))
        # Position at goal with enough straight steps
        self.assertTrue(ultra_map.is_at_goal(((1, 1), HEADING_EAST, 4)))



class TestDijkstra(unittest.TestCase):
    def get_data(self, file_name):
        with open(TEST_DIRECTORY + file_name, 'r') as file:
            return file.read()

    # @unittest.skip("skip for now")
    def test_simple_case(self):
        test_input_data = "12\n93\n"

        map_data = parse_input(test_input_data)
        lava_map = LavaMap(map_data)
        shortest_path_cost = find_shortest_path_cost(lava_map)[0]
        self.assertEqual(shortest_path_cost, 5)

    # @unittest.skip("skip for now")
    def test_straight_step_limit(self):
        test_input_data = "11111\n99791\n11111"
        map_data = parse_input(test_input_data)
        lava_map = LavaMap(map_data)
        shortest_path_cost = find_shortest_path_cost(lava_map)[0]
        expected_cost = 12  # Expected after the implementation
        self.assertEqual(shortest_path_cost, expected_cost)

    # @unittest.skip("skip for now")
    def test_shortest_path_cost(self):
        test_input_data = self.get_data('test17.txt')

        map_data = parse_input(test_input_data)
        lava_map = LavaMap(map_data)
        shortest_path_cost = find_shortest_path_cost(lava_map)[0]
        expected_cost = 102
        self.assertEqual(shortest_path_cost, expected_cost)

    # @unittest.skip("skip for now")
    def test_shortest_path_cost_part_two(self):
        test_input_data = self.get_data('test17.txt')

        map_data = parse_input(test_input_data)
        lava_map = UltraCrucibleMap(map_data)
        shortest_path_cost, path = find_shortest_path_cost(lava_map)
        # self.display_path(path, lava_map)
        expected_cost = 94
        self.assertEqual(shortest_path_cost, expected_cost)

    # @unittest.skip("skip for now")
    def test_ultra_crucible_needs_to_arrive_straight(self):
        test_input_data = "\n".join([
            "111111111111",
            "999999999991",
            "999999999991",
            "999999999991",
            "999999999991"
        ])
        map_data = parse_input(test_input_data)
        lava_map = UltraCrucibleMap(map_data)
        shortest_path_cost, path = find_shortest_path_cost(lava_map)
        # self.display_path(path, lava_map)
        expected_cost = 71
        self.assertEqual(shortest_path_cost, expected_cost)

    # @unittest.skip("skip for now")
    def test_shortest_path_cost_real_data(self):
        test_input_data = self.get_data('input17.txt')

        map_data = parse_input(test_input_data)
        lava_map = LavaMap(map_data)
        shortest_path_cost, path = find_shortest_path_cost(lava_map)
        # self.display_path(path, lava_map)
        expected_cost = 684
        self.assertEqual(shortest_path_cost, expected_cost)

    # @unittest.skip("skip for now")
    def test_shortest_path_cost_real_data_part_two(self):
        test_input_data = self.get_data('input17.txt')

        map_data = parse_input(test_input_data)
        lava_map = UltraCrucibleMap(map_data)
        shortest_path_cost, path = find_shortest_path_cost(lava_map)
        # self.display_path(path, lava_map)
        # self.validate_path(path, lava_map)

        expected_cost = 822
        self.assertEqual(shortest_path_cost, expected_cost)

    def display_path(self, path, lava_map):

        print('')
        print("\n".join([f"Position: {position}, Heading: {heading}, Straigh steps: {straigh_steps}, Cost of getting here: {cost}" for cost, (position, heading, straigh_steps) in path]))
        print('')
        board = [ ['.' for _ in range(lava_map.cols)] for _ in range(lava_map.rows)]
        direction_chars = {
            HEADING_EAST : ">",
            HEADING_WEST : "<",
            HEADING_NORTH: "^",
            HEADING_SOUTH: "v",
        }
        for cost, ((x,y), heading, straigh_steps) in path:
            board[y][x] = direction_chars[heading]
        print("\n".join([''.join(l) for l in board]))

    def validate_path(self, path, lava_map):
        previous = None
        direction_names = {
            HEADING_EAST : "east",
            HEADING_WEST : "west",
            HEADING_NORTH: "north",
            HEADING_SOUTH: "south",
        }
        for cost, ((x,y), heading, straigh_steps) in path:
            if previous:
                pcost, ((px,py), pheading, pstraigh_steps) = previous
                if heading != pheading:
                    print('-- DIRECTION CHANGE -- previous direction: ' + direction_names[pheading])
                print(cost, ((x,y), direction_names[heading], straigh_steps))

            previous = cost, ((x,y), heading, straigh_steps)


HEADING_EAST = (1, 0)
HEADING_WEST = (-1, 0)
HEADING_NORTH = (0, -1)
HEADING_SOUTH = (0, 1)

def turn_left(heading):
    return (heading[1], -heading[0])

def turn_right(heading):
    return (-heading[1], heading[0])


def parse_input(input_str):
    return [[int(char) for char in line] for line in input_str.strip('\n').split('\n')]


class LavaMap:
    def __init__(self, map_data):
        self.map_data = map_data
        self.rows = len(map_data)
        self.cols = len(map_data[0])

    def next_steps(self, current_step):
        position, heading, straight_steps = current_step
        next_steps = []

        # Turn left resets the straight step count
        next_steps.append((self.step(position, turn_left(heading)), turn_left(heading), 1))

        # Continue straight only if straight steps are less than 3
        if straight_steps < 3:
            next_steps.append((self.step(position, heading), heading, straight_steps + 1))

        # Turn right resets the straight step count
        next_steps.append((self.step(position, turn_right(heading)), turn_right(heading), 1))

        # Filter valid positions and calculate costs
        valid_next_steps = [(p, h, s) for p, h, s in next_steps if self.is_valid_position(p)]
        result = [(self.position_cost(p), (p, h, s)) for p, h, s in valid_next_steps]

        return result

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.cols and 0 <= y < self.rows

    def step(self, position, heading):
        return (position[0] + heading[0], position[1] + heading[1])

    def position_cost(self, position):
        x, y = position
        return self.map_data[y][x]

    def get_initial_moves(self):
        return [
            (0, ((0, 0), HEADING_EAST, 0)),
            (0, ((0, 0), HEADING_SOUTH, 0))
        ]

    def is_at_goal(self, current_step):
        position, _, _ = current_step
        return position == (self.cols - 1, self.rows - 1)

class UltraCrucibleMap(LavaMap):
    MIN_STRAIGHT = 4
    MAX_STRAIGHT = 10

    def next_steps(self, current_step):
        position, heading, straight_steps = current_step
        next_steps = []

        # Add turning only if straight steps are at least MIN_STRAIGHT
        if straight_steps >= self.MIN_STRAIGHT:
            next_steps.append((self.step(position, turn_left(heading)), turn_left(heading), 1))
            next_steps.append((self.step(position, turn_right(heading)), turn_right(heading), 1))

        # Continue straight only if straight steps are less than MAX_STRAIGHT
        if straight_steps < self.MAX_STRAIGHT:
            next_steps.append((self.step(position, heading), heading, straight_steps + 1))

        # Filter valid positions and calculate costs
        valid_next_steps = [(p, h, s) for p, h, s in next_steps if self.is_valid_position(p)]
        result = [(self.position_cost(p), (p, h, s)) for p, h, s in valid_next_steps]

        return result

    def is_at_goal(self, current_step):
        position, _, straight_steps = current_step

        if straight_steps < 4:
            return False

        return position == (self.cols - 1, self.rows - 1)


def find_shortest_path_cost(lava_map):
    # Priority queue to hold the nodes to visit, format: (cost, node)
    to_visit = []
    for move in lava_map.get_initial_moves():
        heapq.heappush(to_visit, move)

    visited = set()
    predecessor = {}

    while to_visit:
        cost, node = heapq.heappop(to_visit)

        if node in visited:
            continue

        visited.add(node)

        # Check if goal is reached
        if lava_map.is_at_goal(node):
            path = [(cost, node)]
            total_cost = cost
            while (cost, node) in predecessor:
                cost, node = predecessor[(cost, node)]
                path.append((cost,node))
            return (total_cost, path[::-1])

        next_moves = lava_map.next_steps(node)

        # Add next steps to the priority queue
        for next_cost, next_node in next_moves:
            if next_node not in visited:
                heapq.heappush(to_visit, (cost + next_cost, next_node))
                predecessor[(cost + next_cost, next_node)] = (cost, node)

    return float('inf')  # Return infinity if no path is found

unittest.main()

