import os
from utils import data_files_for
from collections import deque

# Define the keypads
numeric_keypad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['', '0', 'A']
]

directional_keypad = [
    ['', '^', 'A'],
    ['<', 'v', '>']
]


def shortest_paths_between_keys(keypad_positions, keypad_values, start_key, end_key):
    start = keypad_positions[start_key]
    end = keypad_positions[end_key]

    vertical_distance = abs(start[1] - end[1])
    vertical_direction = '^' if start[1] > end[1] else 'v'
    horizontal_distance = abs(start[0] - end[0])
    horizontal_direction = '<' if start[0] > end[0] else '>'

    # If distance is 0 in one direction, we can only go in the other direction
    if vertical_distance == 0 or horizontal_distance == 0:
        yield [vertical_direction] * vertical_distance + [horizontal_direction] * horizontal_distance
        return

    # Unless we hit a gap
    # we can go vertical first
    if keypad_values[end[1]][start[0]] != '':
        yield [vertical_direction] * vertical_distance + [horizontal_direction] * horizontal_distance

    # Unless we start on the last row and end on the first colum,
    # we can go horizontal first
    if keypad_values[start[1]][end[0]] != '':
        yield [horizontal_direction] * horizontal_distance + [vertical_direction] * vertical_distance

class KeypadController:
    def __init__(self, keypad_paths):
        self.keypad_paths = keypad_paths

    def shortest_paths_on_directional_keypad(self, sequence):
        if len(sequence) == 0:
            return

        if len(sequence) == 1:
            for path_end in self.keypad_paths[('A', sequence[0])]:
                yield path_end + ['A']
            return

        for path_start in self.shortest_paths_on_directional_keypad(sequence[:-1]):
            for path_end in self.keypad_paths[(sequence[-2], sequence[-1])]:
                yield path_start + path_end + ['A']


def display_sequence(sequence):
    print("".join(sequence))

def paths_for(keypad):
    keypad_positions = { key: (x, y) for y, row in enumerate(keypad) for x, key in enumerate(row) if key }
    keypad_paths = {
        (start, end): [path for path in shortest_paths_between_keys(keypad_positions, keypad, start, end)]
        for start in keypad_positions for end in keypad_positions
    }
    return keypad_paths

class IndirectionController:
    def __init__(self):
        numeric_keypad_paths = paths_for(numeric_keypad)
        self.numeric_keypad_controller = KeypadController(numeric_keypad_paths)

        directional_keypad_paths = paths_for(directional_keypad)
        self.directional_keypad_controller = KeypadController(directional_keypad_paths)

    def shortest_paths_with_indirection(self, sequence, indirections):
        if indirections == 0:
            for path in self.numeric_keypad_controller.shortest_paths_on_directional_keypad(sequence):
                yield path
        else:
            for path in self.shortest_paths_with_indirection(sequence, indirections - 1):
                for indirect_path in self.directional_keypad_controller.shortest_paths_on_directional_keypad(path):
                    yield indirect_path

    def length_of_shortest_path_with_indirection(self, sequence, indirections):
        return min(len(path) for path in self.shortest_paths_with_indirection(sequence, indirections))

    def get_complexity(self, data, indirections):
        complexity = 0
        for number_sequence in data:
            min_length = self.length_of_shortest_path_with_indirection(number_sequence, indirections)
            value = int(''.join(number_sequence[:-1]))
            complexity += min_length * value
        return complexity

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):

        data = [list(line.strip()) for line in file.readlines()]

        print("\n--- Part one ---")

        indirection_controller = IndirectionController()

        complexity = indirection_controller.get_complexity(data, 2)
        print(f"Complexity: {complexity}")

        print("\n--- Part two ---")

        # complexity = indirection_controller.get_complexity(data, 25)
        # print(f"Complexity: {complexity}")


        # exit(0)