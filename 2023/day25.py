import unittest
import sys
import itertools
import time

sys.setrecursionlimit(10000)

TEST_DIRECTORY = ''

def get_data(file_name):
    with open(TEST_DIRECTORY + file_name, 'r') as file:
        return file.read()


class TestSnowerloadParser(unittest.TestCase):
    def test_parse(self):
        test_input = (
            "jqt: rhn xhk nvd\n"
            "rsh: frs pzl lsr\n"
            "xhk: hfx\n"
            "cmg: qnr nvd lhk bvb\n"
            "rhn: xhk bvb hfx\n"
            "bvb: xhk hfx\n"
            "pzl: lsr hfx nvd\n"
            "qnr: nvd\n"
            "ntq: jqt hfx bvb xhk\n"
            "nvd: lhk\n"
            "lsr: lhk\n"
            "rzs: qnr cmg lsr rsh\n"
            "frs: qnr lhk lsr\n"
        )
        expected_output = {
            'bvb': {'name': 'bvb', 'connections': ['cmg', 'rhn', 'xhk', 'hfx', 'ntq']},
            'cmg': {'name': 'cmg', 'connections': ['qnr', 'nvd', 'lhk', 'bvb', 'rzs']},
            'frs': {'name': 'frs', 'connections': ['rsh', 'qnr', 'lhk', 'lsr']},
            'hfx': {'name': 'hfx', 'connections': ['xhk', 'rhn', 'bvb', 'pzl', 'ntq']},
            'jqt': {'name': 'jqt', 'connections': ['rhn', 'xhk', 'nvd', 'ntq']},
            'lhk': {'name': 'lhk', 'connections': ['cmg', 'nvd', 'lsr', 'frs']},
            'lsr': {'name': 'lsr', 'connections': ['rsh', 'pzl', 'lhk', 'rzs', 'frs']},
            'ntq': {'name': 'ntq', 'connections': ['jqt', 'hfx', 'bvb', 'xhk']},
            'nvd': {'name': 'nvd', 'connections': ['jqt', 'cmg', 'pzl', 'qnr', 'lhk']},
            'pzl': {'name': 'pzl', 'connections': ['rsh', 'lsr', 'hfx', 'nvd']},
            'qnr': {'name': 'qnr', 'connections': ['cmg', 'nvd', 'rzs', 'frs']},
            'rhn': {'name': 'rhn', 'connections': ['jqt', 'xhk', 'bvb', 'hfx']},
            'rsh': {'name': 'rsh', 'connections': ['frs', 'pzl', 'lsr', 'rzs']},
            'rzs': {'name': 'rzs', 'connections': ['qnr', 'cmg', 'lsr', 'rsh']},
            'xhk': {'name': 'xhk', 'connections': ['jqt', 'hfx', 'rhn', 'bvb', 'ntq']}
        }
        self.assertEqual(parse(test_input), expected_output)



def parse(string_input):
    nodes = {}
    for line in string_input.strip().split("\n"):
        node, connections_string = line.split(": ")
        connections = connections_string.split(' ')
        if node not in nodes:
            nodes[node] = {"name": node, "connections": []}
        for connection in connections:
            nodes[node]["connections"].append(connection)
            if connection not in nodes:
                nodes[connection] = {"name": connection, "connections": []}
            nodes[connection]["connections"].append(node)
    return nodes

class TestGenerateEdges(unittest.TestCase):
    def test_generate_edges(self):
        nodes = {
            "a": {"name": "a", "connections": ["b"]},
            "b": {"name": "b", "connections": ["a", "c"]},
            "c": {"name": "c", "connections": ["b"]}
        }
        expected_edges = {("a", "b"), ("b", "c")}
        self.assertEqual(generate_edges(nodes), expected_edges)

def generate_edges(nodes):
    edges = set()
    for node, data in nodes.items():
        for connection in data['connections']:
            if (connection, node) not in edges:
                edges.add((node, connection))
    return edges


class TestSolvePartOne(unittest.TestCase):
    def test_end_to_end(self):
        nodes = parse(get_data('input25.txt'))
        print(find_solution(nodes))

def dfs_tree(nodes, start):
    time = 0
    discovered = {}
    low = {}
    bridges = set()
    parents = {}

    def visit(node, parent=None):
        nonlocal nodes, time, discovered, low, bridges, parents
        parents[node] = parent
        discovered[node] = low[node] = time
        time += 1

        for connected_node in nodes[node]['connections']:
            if connected_node not in discovered:
                visit(connected_node, node)
                low[node] = min(low[node], low[connected_node])
                if low[connected_node] > discovered[node]:
                    bridges.add((node, connected_node))
            elif connected_node != parent:
                low[node] = min(low[node], discovered[connected_node])

    visit(start)
    return (bridges, parents)


def remove_edges(nodes, edge1, edge2):
    # Helper function to remove edges from the graph
    nodes[edge1[0]]["connections"].remove(edge1[1])
    nodes[edge1[1]]["connections"].remove(edge1[0])
    nodes[edge2[0]]["connections"].remove(edge2[1])
    nodes[edge2[1]]["connections"].remove(edge2[0])

def restore_edges(nodes, edge1, edge2):
    # Helper function to restore edges in the graph
    nodes[edge1[0]]["connections"].append(edge1[1])
    nodes[edge1[1]]["connections"].append(edge1[0])
    nodes[edge2[0]]["connections"].append(edge2[1])
    nodes[edge2[1]]["connections"].append(edge2[0])

def find_solution(nodes):
    all_edges = generate_edges(nodes)
    total_steps = len(all_edges) * (len(all_edges) - 1) / 2
    steps = 0
    start_time = time.time()

    for edge1, edge2 in itertools.combinations(all_edges, 2):
        steps += 1
        if steps % 1000 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            progress_percentage = (steps / total_steps) * 100
            estimated_total_time = elapsed_time / progress_percentage * 100
            estimated_time_left = estimated_total_time - elapsed_time
            estimated_finish_time = current_time + estimated_time_left
            estimated_finish_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(estimated_finish_time))

            print(f"{steps} / {total_steps} ({round(progress_percentage)}%) - {edge1} - {edge2}")
            print(f"Time so far: {round(elapsed_time, 2)}s, Estimated time left: {round(estimated_time_left, 2)}s")
            print(f"Estimated finish time: {estimated_finish_time_str}")

        remove_edges(nodes, edge1, edge2)
        bridges, _ = dfs_tree(nodes, next(iter(nodes)))
        restore_edges(nodes, edge1, edge2)

        if len(bridges) > 0:
            return edge1, edge2, bridges

    return None


if __name__ == '__main__':
    unittest.main()

