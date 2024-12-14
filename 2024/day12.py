import os
from utils import data_files_for

from collections import defaultdict, deque

def generate_graph(array_of_arrays):
    graph = defaultdict(list)
    rows, cols = len(array_of_arrays), len(array_of_arrays[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(rows):
        for c in range(cols):
            current_char = array_of_arrays[r][c]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and array_of_arrays[nr][nc] == current_char:
                    graph[(r, c)].append((nr, nc))

    # Add isolated nodes (nodes with no neighbors)
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in graph:
                graph[(r, c)] = []

    return graph

def find_connected_subgraphs(data, graph):
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            queue = deque([node])
            visited.add(node)
            x, y = node
            name = data[x][y]
            component_nodes = set()
            component_edges = set()

            while queue:
                current = queue.popleft()
                component_nodes.add(current)
                for neighbor in graph[current]:
                    edge = tuple(sorted([current, neighbor]))
                    component_edges.add(edge)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append((
                name,
                len(component_nodes),
                len(component_edges),
                component_nodes,
                component_edges
            ))

    return components

def generate_outer_edges(nodes, edges):
    outer_edges = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r, c in nodes:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if ((r, c), (nr, nc)) not in edges and ((nr, nc), (r, c)) not in edges:
                outer_edges.add(((r, c), (nr, nc)))

    return outer_edges

def count_outer_edge_sides(outer_edges):
    side_count = len(outer_edges)
    for edge in outer_edges:
        if edge[0][0] != edge[1][0]:
            left_edge = ((edge[0][0], edge[0][1] - 1),(edge[1][0], edge[1][1]- 1))
            if left_edge in outer_edges:
                side_count -= 1
        if edge[0][1] != edge[1][1]:
            edge_above = ((edge[0][0]-1, edge[0][1]),(edge[1][0]-1, edge[1][1]))
            if edge_above in outer_edges:
                side_count -= 1
    return side_count

def calculate_mapped_values(components):
    results = []
    for name, node_count, edge_count, nodes, edges in components:
        perimeter = 4 * node_count - 2 * edge_count
        outer_edges = generate_outer_edges(nodes, edges)
        if len(outer_edges) != perimeter:
            print(f"Error: ({name} - {len(outer_edges)} != {perimeter}", )
        sides = count_outer_edge_sides(outer_edges)
        results.append((name, node_count, edge_count, len(outer_edges), sides, node_count * perimeter, node_count * sides))
    return results


if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):

        data = [list(line.strip()) for line in file]

        graph = generate_graph(data)

        components = find_connected_subgraphs(data, graph)

        mapped_values = calculate_mapped_values(components)
        #print("Mapped Values:", mapped_values)
        #print('\n'.join([f"{name} - #node: {node_count}, #edge: {edge_count}, perimeter: {perimeter}, sides: {sides}, price: {price}, discounted: {discounted}" for name, node_count, edge_count, perimeter, sides, price, discounted in mapped_values]))

        final_result = (sum([v[-2] for v in mapped_values]), sum([v[-1] for v in mapped_values]))


        print("\n--- Part one ---")
        print("Final Result:", final_result[0])

        print("\n--- Part two ---")
        print("Final Result:", final_result[1])
