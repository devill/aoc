import os
import re
from itertools import product
from utils import data_files_for


def empty(clique):
    return not clique


class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, a, b):
        self.add_directed_edge(a, b)
        self.add_directed_edge(b, a)

    def add_edges(self, edges):
        for a, b in edges:
            self.add_edge(a, b)

    def add_directed_edge(self, a, b):
        if a not in self.edges:
            self.edges[a] = set()
        self.edges[a].add(b)

    def nodes(self):
        return self.edges.items()

    def node_set(self):
        return set(self.edges.keys())

    def is_connected(self, a, b):
        return b in self.edges[a]

    def search_nodes(self, regex):
        return [(node, edges) for node, edges in self.nodes() if regex.match(node)]

    def neighbors(self, node):
        return self.edges[node]

    def find_three_cliques_with_matching_nodes(self, regex):
        t_nodes = self.search_nodes(regex)

        three_sets = set()
        for node, edges in t_nodes:
            # For each pair of neighbours
            for a, b in product(edges, repeat=2):
                if not self.is_connected(a, b):
                    continue
                items = sorted([node, a, b])
                three_sets.add(tuple(items))
        return three_sets

    def find_all_cliques(self):
        for clique in self.find_all_cliques_recursion(set(), self.node_set(), set()):
            yield sorted(clique)

    def find_all_cliques_recursion(self, current_clique, clicque_candidates, not_connected_to_clique):
        """Bron–Kerbosch algorithm with pivoting for finding cliques."""
        if empty(clicque_candidates) and empty(not_connected_to_clique):
            yield current_clique
        else:
            # Choose a pivot to minimize the size of P ∩ N(pivot)
            pivot = next(iter(clicque_candidates.union(not_connected_to_clique)))
            pivot_neighbors = self.neighbors(pivot)
            for v in clicque_candidates - pivot_neighbors:
                yield from self.find_all_cliques_recursion(
                    current_clique.union({v}),
                    clicque_candidates.intersection(self.neighbors(v)),
                    not_connected_to_clique.intersection(self.neighbors(v))
                )
                clicque_candidates.remove(v)
                not_connected_to_clique.add(v)

    def find_largest_clique(self):
        return max(self.find_all_cliques(), key=len, default=set())


def parse_edge(line):
    return tuple(line.strip().split("-"))


if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        edges = [parse_edge(line) for line in file]

        graph = Graph()
        graph.add_edges(edges)

        print("Number of nodes:", len(graph.edges))
        print("Number of edges:", sum(len(edges) for edges in graph.edges.values()) //2)

        print("\n--- Part one ---")
        three_sets = graph.find_three_cliques_with_matching_nodes(re.compile(r"^t"))
        print("Number of triangles:", len(three_sets))

        print("\n--- Part two ---")
        largest_clique = graph.find_largest_clique()
        print("Largest Clique:", ','.join(largest_clique))
        print("Size of Largest Clique:", len(largest_clique))
