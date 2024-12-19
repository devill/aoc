import os
from utils import data_files_for


def select_patterns_for_design(patterns, design):
    if design == '':
        return []
    for pattern in patterns:
        if design[:len(pattern)] == pattern:
            patterns_for_rest_of_design = select_patterns_for_design(patterns, design[len(pattern):])
            if patterns_for_rest_of_design is not None:
                return [pattern] + patterns_for_rest_of_design
    return None



if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        data = [line.strip() for line in file]
        patterns = [pattern.strip() for pattern in data[0].split(', ')]
        designs = [design.strip() for design in data[2:]]


        print("\n--- Part one ---")

        count = 0
        for design in designs:
            patterns_for_design = select_patterns_for_design(patterns, design)
            if patterns_for_design is not None:
                count += 1
        print(count)


        print("\n--- Part two ---")