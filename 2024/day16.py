import os
from utils import data_files_for

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


def maze_dijsktra(maze):
    start_state = maze.find_start_state()
    end_position = maze.find_end_position()

    visited = set()
    queue = [(0, start_state)]
    while queue:
        weight, state = queue.pop(0)

        if state in visited:
            continue
        visited.add(state)
        if state[0] == end_position:
            return weight
        for next_state, next_weight in maze.get_next_states_with_weights(state):
            queue.append((weight + next_weight, next_state))
        queue.sort(key=lambda x: x[0])

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        data = [list(line.strip()) for line in file.readlines()]

        print("\n--- Part one ---")

        maze = Maze(data)
        print(maze_dijsktra(maze))


        print("\n--- Part two ---")