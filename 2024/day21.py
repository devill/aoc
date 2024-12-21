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

    def initial_min_path_length(self):
        return { (start, end): 1 for start, end in self.paths_for().keys() }

    def add_indirection(self, path, min_path_length):
        return sum(min_path_length[(start, end)] for start, end in zip('A' + path, path + 'A'))

    def add_indirections(self, min_path_length):
        return {
            (start, end): min([self.add_indirection(path, min_path_length) for path in paths])
            for (start, end), paths in self.paths_for().items()
        }


def generate_indirect_paths(indirections):
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
    min_path_length = directional_keypad.initial_min_path_length()

    for _ in range(indirections):
        min_path_length = directional_keypad.add_indirections(min_path_length)

    min_indirect_numeric_path_length = numeric_keypad.add_indirections(min_path_length)

    return min_indirect_numeric_path_length

def find_min_length(numeric_sequence, min_indirect_numeric_path_length):
    return sum([min_indirect_numeric_path_length[(start, end)] for start, end in zip('A' + numeric_sequence[:-1], numeric_sequence)])

def calculate_complexity(data, indirections):
    min_indirect_numeric_path_length = generate_indirect_paths(indirections)
    calculated_values = [{ "min_length": find_min_length(numeric_sequence, min_indirect_numeric_path_length), "value": int(''.join(numeric_sequence[:-1])) } for numeric_sequence in data]
    complexity = sum([value["min_length"] * value["value"] for value in calculated_values])
    return complexity

if __name__ == "__main__":


    for file, _ in data_files_for(os.path.basename(__file__)):
        data = [line.strip() for line in file.readlines()]

        print("\n--- Part one ---")
        complexity = calculate_complexity(data, 2)
        print(f"Complexity: {complexity}")

        print("\n--- Part two ---")
        complexity = calculate_complexity(data, 25)
        print(f"Complexity: {complexity}")