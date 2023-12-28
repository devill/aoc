import unittest

TEST_DIRECTORY = ''

def get_data(file_name):
    with open(TEST_DIRECTORY + file_name, 'r') as file:
        return file.read()

class TestEdgeParser(unittest.TestCase):

    def test_single_edge_parsing(self):
        input_str = "(1, 0) --(5)--> (2, 1)\n"
        expected_output = { "1,0": [("2,1", 5)] }
        self.assertEqual(parse_edges(input_str), expected_output)

    def test_multiple_edge_parsing(self):
        input_str = "(1, 0) --(5)--> (2, 1)\n(2, 1) --(10)--> (3, 2)\n"
        expected_output = {
            "1,0": [("2,1", 5)],
            "2,1": [("3,2", 10)]
        }
        self.assertEqual(parse_edges(input_str), expected_output)


def parse_edges(input_str):
    nodes = {}
    lines = input_str.strip().split("\n")
    for line in lines:
        source, rest = line.split(" --(")
        weight, target = rest.split(")--> ")
        weight = int(weight)
        # Removing parentheses and spaces for consistent node name format
        source = source.strip("()").replace(" ", "")
        target = target.strip("()").replace(" ", "")
        if source not in nodes:
            nodes[source] = []
        nodes[source].append((target, weight))
    for node in nodes:
        nodes[node].sort(key=lambda x: x[1], reverse=True)
    return nodes

class TestMaxPossiblePathLength(unittest.TestCase):

    def test_max_possible_path_length(self):
        nodes = {
            "1,0": [("139,0", 10), ("1,140", 3)],
            "1,140": [("139,140", 130)],
            "139,0": [("139,140", 5)],
            "139,140": []
        }
        expected_max_length = 10 + 130 + 5  # Sum of the longest edges from each node
        self.assertEqual(find_max_possible_path_length(nodes), expected_max_length)

def find_max_possible_path_length(nodes):
    max_length = 0
    for neighbors in nodes.values():
        if neighbors:
            max_length += neighbors[0][1]  # Adding the weight of the longest edge
    return max_length


class TestLongestPathFinder(unittest.TestCase):

    def test_simple_graph(self):
        nodes = {
            "1,0": [("139,0", 10), ("1,140", 3)],
            "1,140": [("139,140", 130)],
            "139,0": [("139,140", 5)]
        }
        start_node = "1,0"
        end_node = "139,140"
        expected_length = 133
        self.assertEqual(find_longest_path_length(nodes, start_node, end_node), expected_length)


def find_longest_path_length(nodes, start_node, end_node):
    def backtrack(current_node, visited, current_length):
        if current_node == end_node:
            return current_length
        max_length = 0
        for neighbor, weight in nodes.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                length = backtrack(neighbor, visited, current_length + weight)
                max_length = max(max_length, length)
                visited.remove(neighbor)
        return max_length

    return backtrack(start_node, set([start_node]), 0)

class TestLongestPathFinderWithPruning(unittest.TestCase):

    def test_longest_path_with_pruning(self):
        nodes = {
            "1,0": [("139,0", 10), ("1,140", 3)],
            "1,140": [("139,140", 130)],
            "139,0": [("139,140", 5)]
        }
        start_node = "1,0"
        end_node = "139,140"
        expected_length = 133  # The path (1,0) -> (139,0) -> (139,140) should be pruned
        self.assertEqual(find_longest_path_length_with_pruning(nodes, start_node, end_node), expected_length)

    def test_longest_path_with_nodes(self):
        nodes = {
            "1,0": [("139,0", 10), ("1,140", 3)],
            "1,140": [("139,140", 130)],
            "139,0": [("139,140", 5)]
        }
        start_node = "1,0"
        end_node = "139,140"
        expected_length = 133
        expected_path = ["1,0", "1,140", "139,140"]
        result_length, result_path = find_longest_path_with_nodes(nodes, start_node, end_node)
        self.assertEqual(result_length, expected_length)
        self.assertEqual(result_path, expected_path)

def find_longest_path_length_with_pruning(nodes, start_node, end_node):
    theoretical_maximum = find_max_possible_path_length(nodes)

    def backtrack(current_node, visited, current_length, theoretical_remaining):
        if current_node == end_node:
            return current_length
        max_length = 0
        for neighbor, weight in nodes.get(current_node, []):
            if neighbor not in visited:
                updated_theoretical_remaining = theoretical_remaining
                if nodes[current_node]:
                    updated_theoretical_remaining -= nodes[current_node][0][1]  # Subtract the longest edge
                if current_length + updated_theoretical_remaining <= max_length:
                    continue  # Early pruning
                visited.add(neighbor)
                length = backtrack(neighbor, visited, current_length + weight, updated_theoretical_remaining)
                max_length = max(max_length, length)
                visited.remove(neighbor)
        return max_length

    return backtrack(start_node, set([start_node]), 0, theoretical_maximum)

def find_longest_path_with_nodes(nodes, start_node, end_node):
    theoretical_maximum = find_max_possible_path_length(nodes)

    def backtrack(current_node, visited, current_length, path, theoretical_remaining):
        if current_node == end_node:
            return current_length, path
        max_length, max_path = 0, []
        for neighbor, weight in nodes.get(current_node, []):
            if neighbor not in visited:
                updated_theoretical_remaining = theoretical_remaining
                if nodes[current_node]:
                    updated_theoretical_remaining -= nodes[current_node][0][1]
                if current_length + updated_theoretical_remaining <= max_length:
                    continue  # Early pruning
                visited.add(neighbor)
                length, temp_path = backtrack(neighbor, visited, current_length + weight, path + [neighbor], updated_theoretical_remaining)
                if length > max_length:
                    max_length, max_path = length, temp_path
                visited.remove(neighbor)
        return max_length, max_path

    return backtrack(start_node, set([start_node]), 0, [start_node], theoretical_maximum)


class TestSolvePartTwo(unittest.TestCase):
    #@unittest.skip('slow')
    def test_solve_part_two(self):
        data = get_data('simplified23.txt')
        nodes = parse_edges(data)
        start_node = "1,0"
        end_node = "139,140"
        result_length, result_path = find_longest_path_with_nodes(nodes, start_node, end_node)
        print(result_length)
        print(result_path)

if __name__ == '__main__':
    unittest.main()
