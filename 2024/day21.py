import os
from utils import data_files_for

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
        yield ''.join([vertical_direction] * vertical_distance + [horizontal_direction] * horizontal_distance)
        return

    # Unless we hit a gap
    # we can go vertical first
    if keypad_values[end[1]][start[0]] != '':
        yield ''.join([vertical_direction] * vertical_distance + [horizontal_direction] * horizontal_distance)

    # Unless we start on the last row and end on the first colum,
    # we can go horizontal first
    if keypad_values[start[1]][end[0]] != '':
        yield ''.join([horizontal_direction] * horizontal_distance + [vertical_direction] * vertical_distance)

class KeypadController:
    def __init__(self, keypad_paths):
        self.keypad_paths = keypad_paths

    def shortest_paths_on_directional_keypad(self, sequence):
        if len(sequence) == 0:
            return

        if len(sequence) == 1:
            for path_end in self.keypad_paths[('A', sequence[0])]:
                yield path_end + 'A'
            return

        for path_start in self.shortest_paths_on_directional_keypad(sequence[:-1]):
            for path_end in self.keypad_paths[(sequence[-2], sequence[-1])]:
                yield path_start + path_end + 'A'

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

def generate_table(dictionary):
    keys = sorted(set(k[0] for k in dictionary.keys()))
    rows = sorted(set(k[1] for k in dictionary.keys()))

    # Print the header
    print("   ", end="")
    for key in keys:
        print(f"{key:>3}", end="")
    print()

    # Print each row
    for row in rows:
        print(f"{row:>3}", end="")
        for key in keys:
            value = dictionary.get((key, row), "")
            print(f"{value:>3}", end="")
        print()


if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):

        data = [line.strip() for line in file.readlines()]

        print("\n--- Part one ---")

        indirection_controller = IndirectionController()

        complexity = indirection_controller.get_complexity(data, 2)
        print(f"Complexity: {complexity}")

        print("\n--- Part two ---")

        directional_keypad_paths = paths_for(directional_keypad)
        numeric_keypad_paths = paths_for(numeric_keypad)

        def add_indirection(path, min_path_length):
            length = 0
            total_path = 'A' + path + 'A'
            for start, end in zip(total_path[:-1], total_path[1:]):
                length += min_path_length[(start, end)]
            return length


        min_path_length = {
            (start, end): min(len(path) for path in paths) + 1
            for (start, end), paths in directional_keypad_paths.items()
        }

        for _ in range(24):
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
            print(numeric_sequence, min_length)
        print(f"Complexity: {complexity}")