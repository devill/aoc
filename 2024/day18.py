import os
import heapq
from utils import data_files_for

class GridWithBlocks:
    def __init__(self, size, blocked_locations):
        self.size = size
        self.blocked_locations = blocked_locations

    def initial_state(self):
        return (0, 0)

    def target_state(self):
        return (self.size - 1, self.size - 1)

    def is_valid_state(self, state):
        x, y = state
        return 0 <= x < self.size and 0 <= y < self.size and state not in self.blocked_locations

    def neighbors(self, state):
        x, y = state
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            neighbor = (x + dx, y + dy)
            if self.is_valid_state(neighbor):
                yield neighbor, 1

def dijsktra(graph):
    start = graph.initial_state()
    target = graph.target_state()
    frontier = [(0, start)]
    cost_so_far = {start: 0}
    came_from = {}

    while frontier:
        current_cost, current_state = heapq.heappop(frontier)
        if current_state == target:
            path = []
            while current_state != start:
                path.append(current_state)
                current_state = came_from[current_state]
            path.append(start)
            path.reverse()
            return path

        for neighbor, weight in graph.neighbors(current_state):
            new_cost = current_cost + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))
                came_from[neighbor] = current_state

    return None

def draw_grid(size, blocked_locations):
    for y in range(size):
        for x in range(size):
            if (x, y) in blocked_locations:
                print('#', end='')
            else:
                print('.', end='')
        print()

if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):
        raw_data = [line.strip().split(',') for line in file]
        data = [(int(x), int(y)) for x, y in raw_data]
        size = 71 if meta['type'] == 'real' else 7
        head_length = 1024 if meta['type'] == 'real' else 12
        #print(data)

        print("\n--- Part one ---")

        blocked_locations = set(data[:head_length])

        graph = GridWithBlocks(size, blocked_locations)
        path = dijsktra(graph)

        if path:
            print("Path found:", len(path) - 1)
        else:
            print("No path found")

        print("\n--- Part two ---")

        low = 0
        high = len(data)

        while low < high:
            mid = (low + high) // 2
            blocked_locations = set(data[:mid])
            graph = GridWithBlocks(size, blocked_locations)
            path = dijsktra(graph)
            if path:
                low = mid + 1
            else:
                high = mid

        print(f"Path is blocked at {low - 1} nanoseconds by {data[low-1]}")