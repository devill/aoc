import os
import re
import math
import time
from utils import data_files_for

def parse_line(line):
    match = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
    if match:
        p = (int(match.group(1)), int(match.group(2)))
        v = (int(match.group(3)), int(match.group(4)))
        return  { "position": p, "velocity": v }
    return None

def display_positions(positions, size):
    robot_map = [[0 for _ in range(size[0])] for _ in range(size[1])]
    for x,y in positions:
        robot_map[y][x] += 1
    return '\n'.join([''.join([str(c) if c > 0 else '.' for c in line]) for line in robot_map])


def future_positions(robots, seconds, size):
    return [
        ((r["position"][0] + seconds * r["velocity"][0]) % size[0],
         (r["position"][1] + seconds * r["velocity"][1]) % size[1])
        for r in robots
    ]


def calculate_score(robots, seconds, size):
    end_positions = future_positions(robots, seconds, size)

    quadrants = [[0,0], [0,0]]
    half_point = ((size[0] - 1) // 2, (size[1] - 1) // 2)

    for p in end_positions:
        if p[0] != half_point[0] and p[1] != half_point[1]:
            qx = 0 if p[0] < half_point[0] else 1
            qy = 0 if p[1] < half_point[1] else 1
            quadrants[qx][qy] += 1

    return math.prod(c for line in quadrants for c in line)

if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):
        robots = [ parse_line(line) for line in file ]

        size = (11,7) if type == "test" else (101,103)


        print("\n--- Part one ---")

        initial_positions = [ r["position"] for r in robots ]

        score = calculate_score(robots, 100, size)

        print(score)

        print("\n--- Part two ---")

        if meta["type"] == 'real':
            for seconds in range(10000):
                score = calculate_score(robots, seconds, size)
                if score < 100000000:
                    print(display_positions(future_positions(robots, seconds, size), size))
                    print(f"Seconds: {seconds}, Score for position: {score}", flush=True)
                    time.sleep(0.3)
        else:
            print("Test data is not applicable for part two")

        # exit(0)