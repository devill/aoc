import os
import heapq
from utils import data_files_for

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Maze:
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def find_start_state(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == "S":
                    return ((x, y), (-1, 0))

    def find_end_position(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == "E":
                    return (x, y)

    def get_move_forward_state(self, state):
        (x, y), (dx, dy) = state
        return ((x + dx, y + dy), (dx, dy))

    def can_move_forward(self, state):
        (x, y), (dx, dy) = state
        return 0 <= x + dx < self.width and 0 <= y + dy < self.height and self.data[y + dy][x + dx] != "#"

    def get_turn_states(self, state):
        (x, y), (dx, dy) = state
        return [
            ((x, y), (dy, -dx)),
            ((x, y), (-dy, dx))
        ]

    def get_next_states_with_weights(self, state):
        states = [(state, 1000) for state in self.get_turn_states(state)]
        if self.can_move_forward(state):
            states.append((self.get_move_forward_state(state), 1))
        return states


def maze_dijsktra_with_paths(maze):
    start_state = maze.find_start_state()

    visited = {}
    queue = [(0, start_state)]
    heapq.heapify(queue)
    graph = {}

    while queue:
        weight, state = heapq.heappop(queue)

        if state in visited:
            if visited[state] < weight:
                continue
        visited[state] = weight

        if state not in graph:
            graph[state] = []

        for next_state, next_weight in maze.get_next_states_with_weights(state):
            total_weight = weight + next_weight
            if next_state not in visited or visited[next_state] >= total_weight:
                heapq.heappush(queue, (total_weight, next_state))
                if next_state not in graph:
                    graph[next_state] = []
                graph[next_state].append(state)

    return visited, graph


def find_positions_on_shortest_paths(visited, graph, end_position):
    stack = end_states_with_lowest_weight(end_position, visited)
    positions_on_shortest_paths = set()

    visited_states = set()
    while stack:
        state = stack.pop()
        if state in visited_states:
            continue
        visited_states.add(state)
        positions_on_shortest_paths.add(state[0])
        for prev_state in graph.get(state, []):
            stack.append(prev_state)

    return positions_on_shortest_paths


def shortest_path_weight(end_position, visited):
    return min(visited[(end_position, direction)] for direction in DIRECTIONS if
               (end_position, direction) in visited)


def end_states_with_lowest_weight(end_position, visited):
    spw = shortest_path_weight(end_position, visited)
    return [(end_position, direction) for direction in DIRECTIONS if
               (end_position, direction) in visited and visited[(end_position, direction)] == spw]

def draw_map(data, positions_on_shortest_paths):
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if (x, y) in positions_on_shortest_paths:
                print('\033[91mO\033[0m', end="")
            elif cell == '.':
                print('\033[90m.\033[0m', end="")  # Darker color for '.'
            elif cell == '#':
                print('\033[97m#\033[0m', end="")  # White color for '#'
            else:
                print(cell, end="")
        print()

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        data = [list(line.strip()) for line in file.readlines()]

        print("\n--- Part one ---")

        maze = Maze(data)
        visited, graph = maze_dijsktra_with_paths(maze)
        end_position = maze.find_end_position()

        weight = shortest_path_weight(end_position, visited)
        print(f"Weight of the shortest path: {weight}")

        print("\n--- Part two ---")

        positions_on_shortest_paths = find_positions_on_shortest_paths(visited, graph, end_position)
        print(f"Number of positions on any of the shortest paths: {len(positions_on_shortest_paths)}")
        # 572 too low
        # 586 too high

        draw_map(data, positions_on_shortest_paths)