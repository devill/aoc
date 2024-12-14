import os
from utils import data_files_for

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        for line in file:
            print(line)

        print("\n--- Part one ---")

        print("\n--- Part two ---")