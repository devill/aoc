import heapq
import os
from utils import data_files_for

START = 'S'
END = 'E'
WALL = '#'
TRACK = '.'

class Racetrack:
    def __init__(self, data):
        self.data = data
        self.width = len(data[0])
        self.height = len(data)

    def find_start(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == START:
                    return x, y
        return None

    def find_end(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                if cell == END:
                    return x, y
        return None

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height and self.data[y][x] != WALL

    def neighbors(self, position):
        for neighbor, _ in self.all_neighbors(position):
            if self.is_valid_position(neighbor):
                yield neighbor, 1

    def all_neighbors(self, position):
        x, y = position
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height and neighbor != position:
                yield neighbor, self.data[y + dy][x + dx]

    def wall_neighbors(self, position):
        for neighbor, _ in self.all_neighbors(position):
            if self.data[neighbor[1]][neighbor[0]] == WALL:
                yield neighbor

    def valid_positions(self):
        for x, y in self.all_positions():
            if self.is_valid_position((x, y)):
                yield x, y

    def walls(self):
        for x, y in self.all_positions():
            if self.data[y][x] == WALL:
                yield x, y

    def all_positions(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                yield x, y


def generate_cheat_path(cheat_start, cheat_end):
    for x in range(cheat_start[0], cheat_end[0] + 1, 1 if cheat_start[0] < cheat_end[0] else -1):
        yield x, cheat_start[1]
    for y in range(cheat_start[1], cheat_end[1] + 1, 1 if cheat_start[1] < cheat_end[1] else -1):
        yield cheat_end[0], y


class CheatFinder:
    def __init__(self, racetrack):
        self.racetrack = racetrack
        self.start = racetrack.find_start()
        self.end = racetrack.find_end()
        self.distance_to_start, self.trace_to_start = self.find_shortest_paths(self.start)
        self.distance_to_end, self.trace_to_end = self.find_shortest_paths(self.end)
        self.shortest_path_length = self.distance_to_start[self.end]

    def find_shortest_paths(self, start):
        frontier = [(0, start)]
        cost_so_far = {start: 0}
        came_from = {}
        came_from[start] = None

        while frontier:
            current_cost, current_position = heapq.heappop(frontier)

            for neighbor, weight in self.racetrack.neighbors(current_position):
                new_cost = current_cost + weight
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current_position

        return cost_so_far, came_from

    def reconstruct_path(self, come_from, end):
        path = [end]
        while come_from[end] is not None:
            end = come_from[end]
            path.append(end)
        path.reverse()
        return path

    def find_cheats(self, max_length):
        for cheat_start in self.racetrack.valid_positions():
            for cheat_end in self.positions_in_range(cheat_start, max_length):
                if not self.racetrack.is_valid_position(cheat_end):
                    continue
                if self.distance_between(cheat_start, cheat_end) < 2:
                    continue
                saved_time = self.shortest_path_length - (self.distance_to_start[cheat_start] + self.distance_to_end[cheat_end] + self.distance_between(cheat_start, cheat_end))
                if saved_time > 0:
                    #path_start = self.reconstruct_path(self.trace_to_start, cheat_start)
                    #cheat_path = [position for position in generate_cheat_path(cheat_start, cheat_end)]
                    #final_approach = self.reconstruct_path(self.trace_to_end, cheat_end)
                    yield saved_time, [], [], [] #, path_start, cheat_path, final_approach

    def positions_in_range(self, position, max_length):
        for x in range(-max_length, max_length + 1):
            for y in range(-max_length, max_length + 1):
                if abs(x) + abs(y) <= max_length and (x, y) != (0, 0):
                    yield position[0] + x, position[1] + y

    def distance_between(self, cheat_start, cheat_end):
        return abs(cheat_start[0] - cheat_end[0]) + abs(cheat_start[1] - cheat_end[1])


def draw_cheat_path(racetrack, path_start, cheat_path, final_approach):
    for y, row in enumerate(racetrack.data):
        for x, cell in enumerate(row):
            if (x, y) in cheat_path:
                print('\033[91m' + cell + '\033[0m', end='')
            elif (x, y) in path_start:
                print('\033[92m' + cell + '\033[0m', end='')
            elif (x, y) in final_approach:
                print('\033[94m' + cell + '\033[0m', end='')
            else:
                print(cell, end='')
        print()


if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):
        limit = 100 if meta['type'] == 'real' else 50
        data = [list(line.strip()) for line in file]

        racetrack = Racetrack(data)
        cheat_finder = CheatFinder(racetrack)

        parts = [
            ("--- Part one ---", 2),
            ("--- Part two ---", 20)
        ]

        for part_title, max_length in parts:
            print(part_title)

            cheat_count = 0
            saved_time_frequency = {}
            for saved_time, path_start, cheat_path, final_approach in cheat_finder.find_cheats(max_length):
                if saved_time >= limit:
                    cheat_count += 1
                    saved_time_frequency[saved_time] = saved_time_frequency.get(saved_time, 0) + 1

                    #print(f"\n\nSaved time: {saved_time}")
                    #draw_cheat_path(racetrack, path_start, cheat_path, final_approach)

            print(f"Cheats worth at least {limit} picoseconds: {cheat_count}")
            # print("Saved time frequency:")
            # for saved_time, frequency in sorted(saved_time_frequency.items()):
            #     print(f"{frequency} cheats saved {saved_time} picoseconds ")

    # test value should be 285
        # too low 233268
        # too high 1061108

        # exit(0)