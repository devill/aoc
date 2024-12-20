import heapq
import os
from utils import data_files_for

START = 'S'
END = 'E'
WALL = '#'
EMPTY = '.'


class Maze:
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def find_start(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == START:
                    return x, y
        return None

    def find_end(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == END:
                    return x, y
        return None

    def is_valid_state(self, cell):
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height and not self.data[y][x] == WALL

    def neighbors(self, cell):
        for neighbor, _ in self.all_neighbours(cell):
            if self.is_valid_state(neighbor):
                yield neighbor, 1

    def all_neighbours(self, cell):
        x, y = cell
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height:
                yield neighbor, self.data[y + dy][x + dx]

    def wall_neighbours(self, cell):
        for neighbor, _ in self.all_neighbours(cell):
            if self.data[neighbor[1]][neighbor[0]] == WALL:
                yield neighbor

    def valid_states(self):
        for x, y in self.all_states():
            if self.is_valid_state((x, y)):
                yield x, y

    def walls(self):
        for x, y in self.all_states():
            if self.data[y][x] == WALL:
                yield x, y

    def all_states(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                yield x, y

def find_shortest_paths_to_all(graph, start):
    frontier = [(0, start)]
    cost_so_far = {start: 0}
    came_from = {}

    while frontier:
        current_cost, current_state = heapq.heappop(frontier)

        for neighbor, weight in graph.neighbors(current_state):
            new_cost = current_cost + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))
                came_from[neighbor] = current_state

    return cost_so_far


def cells_within_distance(cell, distance):
    x, y = cell
    for dx in range(-distance, distance + 1):
        remaining_distance = distance - abs(dx)
        for dy in range(-remaining_distance, remaining_distance + 1):
            if dx != 0 or dy != 0:
                yield x + dx, y + dy

def find_cheats_from(maze, start, max_length):
    frontier = [(1, wall_neighbour) for wall_neighbour in maze.wall_neighbours(start)]
    visited = set()

    while frontier:
        current_length, current_state = frontier.pop(0)
        if current_length > max_length:
            continue

        if current_state in visited:
            continue

        visited.add(current_state)

        if maze.data[current_state[1]][current_state[0]] == WALL:
            for neighbor, _ in maze.all_neighbours(current_state):
                if neighbor not in visited:
                    frontier.append((current_length + 1, neighbor))
        else:
            yield current_state, current_length


if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):
        limit = 100 if meta['type'] == 'real' else 10
        data = [list(line.strip()) for line in file]

        maze = Maze(data)
        start = maze.find_start()
        end = maze.find_end()

        shortest_paths_from_start = find_shortest_paths_to_all(maze, start)
        shortest_paths_from_end = find_shortest_paths_to_all(maze, end)

        shortest_path_length = shortest_paths_from_start[end]

        print(f"Shortest path length: {shortest_path_length}")

        print("\n--- Part one ---")

        cheat_count = 0
        saved_time_frequency = {}
        for cell1 in maze.valid_states():
            for cell2, distance in find_cheats_from(maze, cell1, 2):
                cheat_length = shortest_paths_from_start[cell1] + shortest_paths_from_end[cell2] + distance
                if cheat_length < shortest_path_length:
                    saved_time = shortest_path_length - cheat_length
                    saved_time_frequency[saved_time] = saved_time_frequency.get(saved_time, 0) + 1
                    if saved_time >= limit:
                        cheat_count += 1

        print(f"Cheats worth at least {limit} picoseconds:", cheat_count)


        print("\n--- Part two ---")

        cheat_count = 0
        for cell1 in maze.valid_states():
            for cell2, distance in find_cheats_from(maze, cell1, 20):
                cheat_length = shortest_paths_from_start[cell1] + shortest_paths_from_end[cell2] + distance
                if cheat_length < shortest_path_length:
                    saved_time = shortest_path_length - cheat_length
                    if saved_time >= limit:
                        cheat_count += 1

        print(f"Cheats worth at least {limit} picoseconds:", cheat_count)

        # too low 233268
        # too high 1061108

        # exit(0)