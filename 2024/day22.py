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




if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        values = [int(line.strip()) for line in file]

        print("\n--- Part one ---")

        future_values = [SequenceMapper().get_future_value(value) for value in values]
        print(sum(future_values))

        print("\n--- Part two ---")