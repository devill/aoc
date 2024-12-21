import os
from utils import data_files_for

class Keypad:
    def __init__(self, layout):
        self.layout = layout
        self.positions = {key: (x, y) for y, row in enumerate(layout) for x, key in enumerate(row) if key}

    def shortest_paths_between_keys(self, start_key, end_key):
        start = self.positions[start_key]
        end = self.positions[end_key]

        vertical_distance = abs(start[1] - end[1])
        vertical_direction = '^' if start[1] > end[1] else 'v'
        horizontal_distance = abs(start[0] - end[0])
        horizontal_direction = '<' if start[0] > end[0] else '>'

        if vertical_distance == 0 or horizontal_distance == 0:
            yield ''.join([vertical_direction] * vertical_distance + [horizontal_direction] * horizontal_distance)
            return

        if self.layout[end[1]][start[0]] != '':
            yield ''.join([vertical_direction] * vertical_distance + [horizontal_direction] * horizontal_distance)

        if self.layout[start[1]][end[0]] != '':
            yield ''.join([horizontal_direction] * horizontal_distance + [vertical_direction] * vertical_distance)

    def paths_for(self):
        return {
            (start, end): [path for path in self.shortest_paths_between_keys(start, end)]
            for start in self.positions for end in self.positions
        }

def add_indirection(path, min_path_length):
    return sum(min_path_length[(start, end)] for start, end in zip('A' + path, path + 'A'))

def calculate_complexity(data, indirections, numeric_keypad, directional_keypad):
    directional_keypad_paths = directional_keypad.paths_for()
    numeric_keypad_paths = numeric_keypad.paths_for()

    min_path_length = {
        (start, end): min(len(path) for path in paths) + 1
        for (start, end), paths in directional_keypad_paths.items()
    }

    for _ in range(indirections - 1):
        min_indirect_path_length = {
            (start, end): min([add_indirection(path, min_path_length) for path in paths])
            for (start, end), paths in directional_keypad_paths.items()
        }
        min_path_length = min_indirect_path_length

    min_indirect_numeric_path_length = {
        (start, end): min([add_indirection(path, min_path_length) for path in paths])
        for (start, end), paths in numeric_keypad_paths.items()
    }

    complexity = 0
    for numeric_sequence in data:
        min_length = sum([min_indirect_numeric_path_length[(start, end)] for start, end in zip('A' + numeric_sequence[:-1], numeric_sequence)])
        value = int(''.join(numeric_sequence[:-1]))
        complexity += min_length * value
    print(f"Complexity: {complexity}")

if __name__ == "__main__":
    numeric_keypad = Keypad([
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['', '0', 'A']
    ])

    directional_keypad = Keypad([
        ['', '^', 'A'],
        ['<', 'v', '>']
    ])

    for file, _ in data_files_for(os.path.basename(__file__)):
        data = [line.strip() for line in file.readlines()]

        print("\n--- Part one ---")
        calculate_complexity(data, 2, numeric_keypad, directional_keypad)

        print("\n--- Part two ---")
        calculate_complexity(data, 25, numeric_keypad, directional_keypad)