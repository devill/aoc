import os
import math
from utils import data_files_for

if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        data = [list(line.strip()) for line in file]

        frequencies = {}

        for i, line in enumerate(data):
            for j, frequency in enumerate(line):
                if frequency != '.':
                    if frequency not in frequencies:
                        frequencies[frequency] = []
                    frequencies[frequency].append((i, j))

        print("\n--- Part one ---")

        nodes = set()
        for frequency, antenna_locations in frequencies.items():
            for al1 in antenna_locations:
                for al2 in antenna_locations:
                    if al1 != al2:
                        d = (al2[0] - al1[0], al2[1] - al1[1])
                        node = (al1[0] - d[0], al1[1] - d[1])

                        if 0 <= node[0] < len(data) and 0 <= node[1] < len(data[0]):
                            nodes.add(node)

        result = len(nodes)
        print(f"Result is {result}")

        print("\n--- Part two ---")

        nodes = set()
        for frequency, antenna_locations in frequencies.items():
            for al1 in antenna_locations:
                for al2 in antenna_locations:
                    if al1[0] < al2[0] or (al1[0] == al2[0] and al1[1] < al2[1]):
                        d = (al2[0] - al1[0], al2[1] - al1[1])
                        gcd = math.gcd(d[0], d[1])
                        ds = (d[0] // gcd, d[1] // gcd)

                        size = max(len(data) // ds[0], len(data[0]) // ds[1])
                        for i in range(-2*size, 2*size):
                            node = (al1[0] + i * ds[0], al1[1] + i * ds[1])
                            if 0 <= node[0] < len(data) and 0 <= node[1] < len(data[0]):
                                nodes.add(node)

        result = len(nodes)
        print(f"Result is {result}")

        # exit(0)