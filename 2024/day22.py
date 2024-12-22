import os
from utils import data_files_for

class MonkeyRandom:

    def __init__(self):
        self.value = None

    def advance(self):
        self.value = (self.value ^ (self.value << 6) % 16777216)
        self.value = (self.value ^ (self.value >> 5) % 16777216)
        self.value = (self.value ^ (self.value << 11) % 16777216)
        return self

    def advance_many(self, times):
        for _ in range(times):
            self.advance()
        return self

    def get_many(self, times):
        return [self.advance().get() for _ in range(times)]

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        return self

class SequenceMapper:
    def __init__(self):
        self.randomizer = MonkeyRandom()

    def get_future_value(self, value):
        return self.randomizer.set(value).advance_many(2000).get()

    def get_values_for_first_pattern_occurances(self, value):

        initial_values = self.randomizer.set(value).get_many(2000)
        initial_digits = [v % 10 for v in [value] + initial_values]
        diffs = [initial_digits[i + 1] - initial_digits[i] for i in range(len(initial_digits) - 1)]

        patterns = {}
        for i in range(4, len(diffs)):
            pattern = tuple(diffs[i-4:i])
            if pattern not in patterns:
                patterns[pattern] = initial_digits[i]

        return patterns

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        values = [int(line.strip()) for line in file]

        print("\n--- Part one ---")

        future_values = [SequenceMapper().get_future_value(value) for value in values]
        print(sum(future_values))

        print("\n--- Part two ---")
        mapper = SequenceMapper()
        pattern_sums = {}
        for value in values:
            patters_for_value = mapper.get_values_for_first_pattern_occurances(value)
            for pattern, pattern_value in patters_for_value.items():
                if pattern not in pattern_sums:
                    pattern_sums[pattern] = 0
                pattern_sums[pattern] += pattern_value

        print(max(pattern_sums.values()))

        # 10155 too high