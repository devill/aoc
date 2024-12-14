import os
from utils import data_files_for

LOOP = True
NO_LOOP = False

def find_guard_position_and_direction(map_data):
    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell in directions:
                return (i, j), directions[cell]
    return None, None

def turn_right(direction):
    return (direction[1], -direction[0])

def print_map(map_data):
    for row in map_data:
        print(''.join(row))

def simulate_guard(map_data, start_pos, start_dir):
    visited = set()
    pos = start_pos
    direction = start_dir
    rows, cols = len(map_data), len(map_data[0])

    i = 0

    while i < rows * cols * 4:
        visited.add(pos)
        next_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if next_pos[0] < 0 or rows <= next_pos[0] or next_pos[1] < 0 or cols <= next_pos[1]:
            return visited, NO_LOOP
        if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and map_data[next_pos[0]][next_pos[1]] != '#':
            pos = next_pos
        else:
            direction = turn_right(direction)
        i+=1

    return visited, LOOP

def simulate_guard_with_obstruction(map_data, start_pos, start_dir, obstruction_pos):
    map_data[obstruction_pos[0]][obstruction_pos[1]] = '#'
    visited, loop_detected = simulate_guard(map_data, start_pos, start_dir)
    map_data[obstruction_pos[0]][obstruction_pos[1]] = '.'  # Reset the obstruction
    return loop_detected

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        map_data = [list(line.strip()) for line in file]

        print("\n--- Part one ---")

        start_pos, start_dir = find_guard_position_and_direction(map_data)
        visited_positions, loop_detected = simulate_guard(map_data, start_pos, start_dir)

        print(f"Distinct positions visited: {len(visited_positions)}")

        print("\n--- Part two ---")

        valid_obstruction_positions = 0
        tries = 0
        for pos in visited_positions:
            if pos == start_pos:
                continue
            if simulate_guard_with_obstruction(map_data, start_pos, start_dir, pos):
                valid_obstruction_positions += 1
            tries += 1
            print(tries)

        print(f"Valid obstruction positions: {valid_obstruction_positions}")

        #exit(0)