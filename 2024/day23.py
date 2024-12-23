import os
import re
from itertools import product
from utils import data_files_for


class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, a, b):
        self.add_directed_edge(a, b)
        self.add_directed_edge(b, a)

    def add_directed_edge(self, a, b):
        if a not in self.edges:
            self.edges[a] = set()
        self.edges[a].add(b)

    def nodes(self):
        return self.edges.items()

    def is_connected(self, a, b):
        return b in self.edges[a]

    def search_nodes(self, regex):
        return [(node, edges) for node, edges in self.nodes() if regex.match(node)]


def parse_edge(line):
    return tuple(line.strip().split("-"))

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        edges = [parse_edge(line) for line in file]

        graph = Graph()
        for edge in edges:
            graph.add_edge(*edge)

        print("Number of nodes:", len(graph.edges))
        print("Number of edges:", sum(len(edges) for edges in graph.edges.values()))

        print("\n--- Part one ---")

        # Nodes starting with 't'
        t_matcher = re.compile(r"^t")
        t_nodes = graph.search_nodes(t_matcher)

        three_sets = set()
        for node, edges in t_nodes:
            # For each pair of neighbours
            for a, b in product(edges, repeat=2):
                if a == b:
                    continue
                if not graph.is_connected(a, b):
                    continue
                items = sorted([node, a, b])
                three_sets.add(tuple(items))

        print("Number of triangles:", len(three_sets))


        print("\n--- Part two ---")