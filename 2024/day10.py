import os
from utils import data_files_for

def print_touched(data, touched):
    for i, line in enumerate(data):
        for j, num in enumerate(line):
            if (i, j) in touched:
                print(num, end="")
            else:
                print(".", end="")
        print()

if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        data = [[int(i) for i in list(line.strip())] for line in file]


        print("\n--- Part one ---")

        trailheads = []
        for i, line in enumerate(data):
            for j, num in enumerate(line):
                if num == 0:
                    trailheads.append((i, j))

        current_steps = [{trailhead} for trailhead in trailheads]
        all_touched = [{trailhead} for trailhead in trailheads]
        next_steps = [set() for _ in range(len(trailheads))]
        next_elevation = 1

        while next_elevation < 10:
            for i, trailhead_steps in enumerate(current_steps):
                for current_step in trailhead_steps:
                    if current_step[0] - 1 >= 0 and data[current_step[0] - 1][current_step[1]] == next_elevation:
                        next_steps[i].add((current_step[0] - 1, current_step[1]))
                    if current_step[0] + 1 < len(data) and data[current_step[0] + 1][current_step[1]] == next_elevation:
                        next_steps[i].add((current_step[0] + 1, current_step[1]))
                    if current_step[1] - 1 >= 0 and data[current_step[0]][current_step[1] - 1] == next_elevation:
                        next_steps[i].add((current_step[0], current_step[1] - 1))
                    if current_step[1] + 1 < len(data[0]) and data[current_step[0]][current_step[1] + 1] == next_elevation:
                        next_steps[i].add((current_step[0], current_step[1] + 1))
                all_touched[i] = all_touched[i].union(next_steps[i])

            current_steps = next_steps
            next_steps = [set() for _ in range(len(trailheads))]
            next_elevation += 1

        head_scores = [len(trailhead) for trailhead in current_steps]
        print(f"Total score: {sum(head_scores)}")

        print("\n--- Part two ---")

        # exit(0)