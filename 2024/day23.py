import os
import re
from itertools import product
from utils import data_files_for
import networkx as nx

def bron_kerbosch_with_pivoting(graph, r, p, x):
    """Bron–Kerbosch algorithm with pivoting for finding cliques."""
    if not p and not x:
        yield r
    else:
        # Choose a pivot to minimize the size of P ∩ N(pivot)
        pivot = next(iter(p.union(x)))
        pivot_neighbors = set(graph.neighbors(pivot))  # Convert neighbors to a set
        for v in p - pivot_neighbors:
            yield from bron_kerbosch_with_pivoting(
                graph,
                r.union({v}),
                p.intersection(graph.neighbors(v)),
                x.intersection(graph.neighbors(v))
            )
            p.remove(v)
            x.add(v)

def find_largest_clique(graph):
    """Find the largest clique in the graph using Bron-Kerbosch with pivoting."""
    max_clique = set()
    for clique in bron_kerbosch_with_pivoting(graph, set(), set(graph.nodes()), set()):
        if len(clique) > len(max_clique):
            max_clique = clique
    return max_clique

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

    def get_networkx_graph(self):
        G = nx.Graph()
        for node, edges in self.nodes():
            for edge in edges:
                G.add_edge(node, edge)
        return G


def parse_edge(line):
    return tuple(line.strip().split("-"))

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        edges = [parse_edge(line) for line in file]

        graph = Graph()
        for edge in edges:
            graph.add_edge(*edge)

        print("Number of nodes:", len(graph.edges))
        print("Number of edges:", sum(len(edges) for edges in graph.edges.values()) //2)

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

        G = graph.get_networkx_graph()
        largest_clique = sorted(find_largest_clique(G))
        print("Largest Clique:", ','.join(largest_clique))
        print("Size of Largest Clique:", len(largest_clique))
