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

class PatternCounter:
    def __init__(self, patterns):
        self.patterns = patterns
        self.cache = {}

    def count_variations_for_design(self, design):
        if design == '':
            return 1
        if design in self.cache:
            return self.cache[design]
        count = 0
        for pattern in self.patterns:
            if design[:len(pattern)] == pattern:
                count += self.count_variations_for_design(design[len(pattern):])
        self.cache[design] = count
        return count


if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        data = [line.strip() for line in file]
        patterns = [pattern.strip() for pattern in data[0].split(', ')]
        designs = [design.strip() for design in data[2:]]

        counter = PatternCounter(patterns)
        count_possible_designs = 0
        count_total_variations = 0
        for design in designs:
            pattern_variations = counter.count_variations_for_design(design)
            count_possible_designs += 1 if pattern_variations > 0 else 0
            count_total_variations += pattern_variations

        print("\n--- Part one ---")

        print(f"Possible designs: {count_possible_designs}")

        print("\n--- Part two ---")


        print(f"Total variations: {count_total_variations}")