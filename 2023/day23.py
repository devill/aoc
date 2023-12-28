import unittest
import sys

TEST_DIRECTORY = ''

def get_data(file_name):
    with open(TEST_DIRECTORY + file_name, 'r') as file:
        return file.read()

@unittest.skip('Don\'t disturb')
class TestHikingTrailsParser(unittest.TestCase):
    def test_parse_trails(self):
        test_input = (
            "#.##\n"
            "#.##\n"
            "#..#\n"
            "##.#\n"
        )

        expected = [
            list('#.##'),
            list('#.##'),
            list('#..#'),
            list('##.#'),
        ]

        self.assertEqual(parse_trails(test_input), expected)

    def test_parse_for_test_case(self):
        test_input = (
            "#O#########\n"
            "#OOO##....#\n"
            "#.#O##.##.#\n"
            "#OOO##.##.#\n"
            "#O####.##.#\n"
            "#O.OOOO##.#\n"
            "#O#O##O##.#\n"
            "#OOO##O...#\n"
            "######O##.#\n"
            "######OOOO#\n"
            "#########O#\n"
        )

        expected_trails = [
            list("#.#########"),
            list("#...##....#"),
            list("#.#.##.##.#"),
            list("#...##.##.#"),
            list("#.####.##.#"),
            list("#......##.#"),
            list("#.#.##.##.#"),
            list("#...##....#"),
            list("######.##.#"),
            list("######....#"),
            list("#########.#"),
        ]

        expected_hike = set([(1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3),
                         (1, 4), (1, 5), (1, 6), (1, 7), (2, 7), (3, 7), (3, 6), (3, 5),
                         (4, 5), (5, 5), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 9),
                         (8, 9), (9, 9), (9, 10)])

        trails, hike = parse_for_test_case(test_input)
        self.assertEqual(trails, expected_trails)
        self.assertEqual(hike, expected_hike)

    def test_parse_for_test_case_with_slopes(self):
        test_input = (
            "#O######\n"
            "#▶▼<OOO#\n"
            "#>OO▲^O#\n"
            "###v#O◀#\n"
        )
        expected_trails = [
            list("#.######"),
            list("#>v<...#"),
            list("#>..^^.#"),
            list("###v#.<#")
        ]

        expected_hike = set([
            (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 1), (5, 1), (6, 1),
            (6, 2), (6, 3), (5, 3)
        ])

        trails, hike = parse_for_test_case(test_input)
        self.assertEqual(trails, expected_trails)
        self.assertEqual(hike, expected_hike)

def parse_trails(trails_map):
    return [list(line) for line in trails_map.strip('\n').split('\n')]

def parse_for_test_case(test_input):
    lines = test_input.strip().split('\n')
    hike = {(x, y) for y, line in enumerate(lines) for x, cell in enumerate(line) if cell in {'O', '▲','▶', '▼', '◀'}}
    regular_input = test_input\
        .replace('O','.')\
        .replace('▲', '^')\
        .replace('▶', '>')\
        .replace('▼', 'v')\
        .replace('◀', '<')
    return (parse_trails(regular_input), hike)


class TestHikingTrails(unittest.TestCase):
    def display_hike(self, map, hike):
        h = '\n' + '\n'.join([''.join(['O' if (x,y) in hike else cell for x, cell in enumerate(line)]) for y, line in enumerate(map)])
        print(h)

    @unittest.skip('Don\'t disturb')
    def longest_hike_on_map(self, test_input):
        hike_map, expected_hike = parse_for_test_case(test_input)
        hike = Hike(hike_map)
        longest_hike = set(hike.find_longest_hike())
        self.assertEqual(longest_hike, expected_hike)

    @unittest.skip('Don\'t disturb')
    def test_longest_hike_single_option(self):
        self.longest_hike_on_map(
            "#O###\n"
            "#O###\n"
            "#O###\n"
            "#OOO#\n"
            "###O#\n"
        )

    @unittest.skip('Don\'t disturb')
    def test_longest_hike_with_dead_end(self):
        self.longest_hike_on_map((
            "#O###\n"
            "#OOO#\n"
            "#.#O#\n"
            "#.#O#\n"
            "###O#\n"
        ))

    @unittest.skip('Don\'t disturb')
    def test_longest_hike_among_multiple(self):
        self.longest_hike_on_map(
            "#O#########\n"
            "#OOO##OOOO#\n"
            "#.#O##O##O#\n"
            "#OOO##O##O#\n"
            "#O####O##O#\n"
            "#O.OOOO##O#\n"
            "#O#O##.##O#\n"
            "#OOO##OOOO#\n"
            "######O##.#\n"
            "######OOOO#\n"
            "#########O#\n"
        )

    @unittest.skip('Don\'t disturb')
    def test_longest_hike_with_slopes(self):
        self.longest_hike_on_map(
            "#O#########\n"
            "#O▶O##..<.#\n"
            "#.#▼##.##.#\n"
            "#O◀O##OOOO#\n"
            "#O####▲##O#\n"
            "#O.OOOO##O#\n"
            "#O#O##.##O#\n"
            "#OOO##...O#\n"
            "#^#v##.##O#\n"
            "#...##..<O#\n"
            "#########O#\n"
        )

    @unittest.skip('Don\'t disturb')
    def test_end_to_end_part_one(self):
        data = get_data('test23.txt')
        map = parse_trails(data)
        hike = Hike(map)
        longest_hike = hike.find_longest_hike()
        length = len(longest_hike) - 1
        self.assertEqual(length, 94)

    @unittest.skip('Don\'t disturb')
    def test_end_to_end_part_two(self):
        data = get_data('test23.txt')\
            .replace('^', '.')\
            .replace('>', '.')\
            .replace('v', '.')\
            .replace('<', '.')
        map = parse_trails(data)
        hike = Hike(map)
        longest_hike = len(hike.find_longest_hike()) - 1
        self.assertEqual(longest_hike, 154)

    @unittest.skip('Runs slow')
    @unittest.skip('Don\'t disturb')
    def test_solve_part_one(self):
        sys.setrecursionlimit(10000)
        data = get_data('input23.txt')
        map = parse_trails(data)
        hike = Hike(map)
        longest_hike = len(hike.find_longest_hike()) - 1
        self.assertEqual(longest_hike, 2154)

    @unittest.skip('Don\'t disturb')
    def test_dfs_tree(self):
        map = [
            list("#.###"),
            list("#...#"),
            list("#.#.#"),
            list("#...#"),
            list("###.#"),
            list("#...#"),
            list("#.#.#"),
            list("#...#"),
            list("###.#"),
        ]
        hike = Hike(map)
        bridges, parents = hike.dfs_tree()
        expected_bridges = set([
            ((3, 7), (3, 8)),
            ((3, 3), (3, 4)),
            ((1, 0), (1, 1)),
            ((3, 4), (3, 5)),
        ])
        self.assertEqual(bridges, expected_bridges)

    @unittest.skip('Runs incredibly slow')
    def test_solve_part_two(self):
        print("")
        print("")
        print("STARTS HERE")
        print("")
        sys. setrecursionlimit(10000)
        data = get_data('input23.txt') \
            .replace('^', '.') \
            .replace('>', '.') \
            .replace('v', '.') \
            .replace('<', '.')
        map = parse_trails(data)
        hike = Hike(map)
        longest_hike = len(hike.find_longest_hike()) - 1
        print(longest_hike)
        # self.assertEqual(longest_hike, 2154)

    def test_simplified_graph(self):
        data = get_data('input23.txt')\
            .replace('^', '.') \
            .replace('>', '.') \
            .replace('v', '.') \
            .replace('<', '.')
        hike = Hike(parse_trails(data))
        nodes = hike.get_nodes()
        edge_count = 0
        for cell, data in nodes.items():
            for n in data["neighbours"]:
                c, w = n
                print(f"{cell} --({w})--> {c}")
                edge_count += 1
        print(edge_count)
        print(len(nodes))

class Hike:

    def __init__(self, map):
        self.map = map
        self.slopes = {
            '^': [(0, -1)],
            '>': [(1, 0)],
            'v': [(0, 1)],
            '<': [(-1, 0)],
        }

    def get_cell(self, cell):
        x, y = cell
        return self.map[y][x]

    def find_start(self):
        for j, cell in enumerate(self.map[0]):
            if cell == '.':
                return (j, 0)

    def find_end(self):
        for j, cell in enumerate(self.map[-1]):
            if cell == '.':
                return (j, len(self.map) - 1)

    def valid_cell(self, cell):
        x, y = cell
        if y < 0 or y >= len(self.map):
            return False
        if x < 0 or x >= len(self.map[y]):
            return False
        return self.get_cell(cell) != '#'

    def next_valid(self, cell):
        deltas = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1)
        ]
        x, y = cell
        if self.get_cell((x,y)) in self.slopes:
            deltas = self.slopes[self.get_cell((x,y))]

        return [(x + dx, y + dy) for dx, dy in deltas if self.valid_cell((x + dx, y + dy))]

    def neighbours(self, cell):
        deltas = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1)
        ]
        x, y = cell

        return [(x + dx, y + dy) for dx, dy in deltas if self.valid_cell((x + dx, y + dy))]

    def find_all_hikes(self):
        return self.find_hikes(self.find_start(), self.find_end(), set())

    def find_hikes(self, start, end, banned):
        hike = []
        visited = set()
        hikes = []

        def step_to(cell):
            hike.append(cell)
            visited.add(cell)

        def backtrack():
            last_step = hike.pop()
            visited.remove(last_step)

        def explore(cell):
            step_to(cell)
            if cell == end:
                hikes.append(hike[:])
            else:
                for next_cell in self.next_valid(cell):
                    if next_cell not in visited and next_cell not in banned:
                        explore(next_cell)
            backtrack()

        explore(start)

        return hikes

    def find_longest_hike(self):
        all_hikes = self.find_all_hikes()
        # Find the longest hike by length
        longest_hike = max(all_hikes, key=len)
        return longest_hike

    def find_longest_hike_speed_up_with_connected_components(self):
        bridges, parents = self.dfs_tree()
        start = self.find_start()
        block_end = self.find_end()
        block_start = parents[block_end]
        longest_hike = set([start, self.find_end()])
        while True:
            l = 0
            while (parents[block_start], block_start) not in bridges:
                block_start = parents[block_start]
                l+=1

            if block_start == parents[block_end]:
                longest_hike.add(block_start)
            else:

                banned = set([parents[block_start], block_end])
                print(l, block_start, parents[block_end], banned)
                hikes = self.find_hikes(block_start, parents[block_end], banned)

                longest_sub_hike = max(hikes, key=len)
                longest_hike.update(longest_sub_hike)
                longest_hike.update(banned)

            if parents[block_start] == start:
                break
            block_end = block_start
            block_start = parents[block_start]

        return longest_hike

    def dfs_tree(self):
        time = 0
        discovered = {}
        low = {}
        bridges = set()
        parents = {}

        def dfs(cell, parent=None):
            nonlocal time, discovered, low, bridges, parents
            parents[cell] = parent
            discovered[cell] = low[cell] = time
            time += 1

            for next_cell in self.neighbours(cell):
                if next_cell not in discovered:
                    dfs(next_cell, cell)
                    low[cell] = min(low[cell], low[next_cell])
                    if low[next_cell] > discovered[cell]:
                        bridges.add((cell, next_cell))
                elif next_cell != parent:
                    low[cell] = min(low[cell], discovered[next_cell])

        start = self.find_start()
        dfs(start)
        return (bridges, parents)

    def find_edge_end(self, p1, p2):
        c = 1
        start, end = self.find_start(), self.find_end()
        while True:
            if p2 == start or p2 == end:
                return (p2, c)
            nn = [n for n in self.next_valid(p2) if n != p1]
            if len(nn) == 0:
                return (None, None)
            elif len(nn) == 1:
                p1 = p2
                p2 = nn[0]
                c += 1
            else:
                return (p2, c)

    def get_nodes(self):
        nodes = {}
        start, end = self.find_start(), self.find_end()
        for y, line in enumerate(self.map):
            for x, cell in enumerate(self.map[y]):
                if cell != "#" and (len(self.next_valid((x,y))) > 2 or (x,y) == start or (x,y) == end):
                    nn = [self.find_edge_end((x, y), n) for n in self.next_valid((x, y))]
                    nodes[(x,y)] = { "cell": (x,y), "neighbours": [n for n in nn if n[0] != None]}
        return nodes


if __name__ == '__main__':
    unittest.main()