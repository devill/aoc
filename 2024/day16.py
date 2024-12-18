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
                    return ((x, y), (1, 0))

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

    def get_move_backward_state(self, state):
        (x, y), (dx, dy) = state
        return ((x - dx, y - dy), (dx, dy))

    def can_move_backward(self, state):
        (x, y), (dx, dy) = state
        return 0 <= x - dx < self.width and 0 <= y - dy < self.height and self.data[y - dy][x - dx] != "#"

    def get_turn_states(self, state):
        (x, y), (dx, dy) = state
        return [
            ((x, y), (dy, -dx)),
            ((x, y), (-dy, dx))
        ]

    def get_next_states_with_weights(self, state):
        states = [(s, 1000) for s in self.get_turn_states(state)]
        if self.can_move_forward(state):
            states.append((self.get_move_forward_state(state), 1))
        return states

    def get_previous_states_with_weights(self, state):
        states = [(s, 1000) for s in self.get_turn_states(state)]
        if self.can_move_backward(state):
            states.append((self.get_move_backward_state(state), 1))
        return states

def maze_dijsktra(maze):
    start_state = maze.find_start_state()

    visited = {}
    queue = [(0, start_state)]
    heapq.heapify(queue)

    while queue:
        weight, state = heapq.heappop(queue)

        if state in visited:
            continue
        visited[state] = weight

        for next_state, next_weight in maze.get_next_states_with_weights(state):
            if next_state not in visited:
                heapq.heappush(queue, ((weight + next_weight), next_state))


    return visited


def find_states_on_shortest_paths(visited, end_position):
    stack = end_states_with_lowest_weight(end_position, visited)
    states_on_shortest_paths = set()

    visited_states = set()
    while stack:
        state = stack.pop()
        if state in visited_states:
            continue
        visited_states.add(state)
        states_on_shortest_paths.add(state)
        for prev_state, expected_weight in maze.get_previous_states_with_weights(state):
            if visited[prev_state] + expected_weight == visited[state]:
                stack.append(prev_state)

    return states_on_shortest_paths

def shortest_path_weight(end_position, visited):
    return min(visited[(end_position, direction)] for direction in DIRECTIONS if
               (end_position, direction) in visited)


def end_states_with_lowest_weight(end_position, visited):
    spw = shortest_path_weight(end_position, visited)
    return [(end_position, direction) for direction in DIRECTIONS if visited[(end_position, direction)] == spw]

def draw_map(data, positions_on_shortest_paths):
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if (x, y) in positions_on_shortest_paths:
                print('\033[91mO\033[0m', end="")
            elif cell == '.':
                print('\033[90m.\033[0m', end="")  # Darker color for '.'
            elif cell == '#':
                print('\033[90m#\033[0m', end="")  # White color for '#'
            else:
                print(cell, end="")
        print()

def draw_map_with_graph(data, graph, positions_on_shortest_paths):
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if (x, y) in positions_on_shortest_paths:
                print('\033[91mO\033[0m', end="")
            elif cell == '.':
                print('\033[90m.\033[0m', end="")  # Darker color for '.'
            elif cell == '#':
                print('\033[90m#\033[0m', end="")  # White color for '#'
            else:
                print(cell, end="")
            if (x, y) in graph and (x + 1, y) in graph[(x, y)] and (x + 1, y) in graph and (x, y) in graph[(x + 1, y)]:
                print('\033[93mX\033[0m', end="")
            elif (x, y) in graph and (x + 1, y) in graph[(x, y)]:
                print('\033[93m<\033[0m', end="")
            elif (x + 1, y) in graph and (x, y) in graph[(x + 1, y)]:
                print('\033[93m>\033[0m', end="")
            elif cell == '#' or data[y][x + 1] == '#':
                print('\033[90m#\033[0m', end="")  # White color for '#'
            else:
                print(' ', end="")
        print()
        for x, cell in enumerate(row):
            if (x, y) in graph and (x, y + 1) in graph[(x, y)] and (x, y + 1) in graph and (x, y) in graph[(x, y + 1)]:
                print('\033[93mX\033[0m', end="")
            elif (x, y) in graph and (x, y + 1) in graph[(x, y)]:
                print('\033[93m^\033[0m', end="")
            elif (x, y + 1) in graph and (x, y) in graph[(x, y + 1)]:
                print('\033[93mv\033[0m', end="")
            elif cell == '#' or data[y + 1][x] == '#':
                print('\033[90m#\033[0m', end="")
            else:
                print('  ', end="")
            print('\033[90m#\033[0m', end="")
        print()


def flatten_graph(graph):
    flat_graph = {}
    for state, prev_states in graph.items():
        if state[0] not in flat_graph:
            flat_graph[state[0]] = []
        flat_graph[state[0]].extend([prev_state[0] for prev_state in prev_states if prev_state in graph])
    return flat_graph


if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):
        # if meta['type'] == 'real':
        #     continue
        data = [list(line.strip()) for line in file.readlines()]

        print("\n--- Part one ---")

        maze = Maze(data)
        visited = maze_dijsktra(maze)
        end_position = maze.find_end_position()

        weight = shortest_path_weight(end_position, visited)
        print(f"Weight of the shortest path: {weight}")

        print("\n--- Part two ---")

        states_on_shortest_paths = find_states_on_shortest_paths(visited, end_position)
        positions_on_shortest_paths = set([ state[0] for state in states_on_shortest_paths])
        print(f"Number of positions on any of the shortest paths: {len(positions_on_shortest_paths)} ({len(states_on_shortest_paths)} states)")

        draw_map(data, positions_on_shortest_paths)
