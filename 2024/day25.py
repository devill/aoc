import os
from utils import data_files_for

def parse_schematic(schematic):
    as_matirx = [list(row) for row in schematic.split("\n")]
    type = 'lock' if as_matirx[0] == ['#'] * 5 else 'key'
    column_counts = [sum(1 for row in as_matirx if row[i] == '#') - 1 for i in range(5)]
    return type, column_counts

def test_lock_key_pair(lock, key):
    for l, k in zip(lock, key):
        if l + k > 5:
            return False
    return True

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        raw_data = [parse_schematic(schematic) for schematic in file.read().strip().split("\n\n")]
        keys = [schematic for type, schematic in raw_data if type == 'key']
        locks = [schematic for type, schematic in raw_data if type == 'lock']

        print("\n--- Part one ---")

        all_lock_key_pairs = [test_lock_key_pair(lock, key) for lock in locks for key in keys]
        fits = sum([1 for pair in all_lock_key_pairs if pair])
        print(fits)

        print("\n--- Part two ---")