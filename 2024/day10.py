import os
from utils import data_files_for

def neighbors(location, data):
    i, j = location
    if i - 1 >= 0:
        yield (i - 1, j)
    if i + 1 < len(data):
        yield (i + 1, j)
    if j - 1 >= 0:
        yield (i, j - 1)
    if j + 1 < len(data[0]):
        yield (i, j + 1)

def build_trail_graph(data):
    graph = {}
    trailheads = []
    peaks = []
    for i, line in enumerate(data):
        for j, elevation in enumerate(line):
            graph[(i, j)] = []
            if elevation == 0:
                trailheads.append((i, j))
            if elevation == 9:
                peaks.append((i, j))
            if elevation < 9:
                for ni, nj in neighbors((i, j), data):
                    if data[ni][nj] == elevation + 1:
                        graph[(i, j)].append((ni, nj))
    return graph, trailheads, peaks

def find_reachable_peaks_with_multiplicity(data):
    graph, trailheads, peaks = build_trail_graph(data)
    return [search_peaks(trailhead, graph, peaks) for trailhead in trailheads]

def search_peaks(location, graph, peaks):
    if location in peaks:
        return [location]
    reachable_peaks = []
    for neighbor in graph[location]:
        reachable_peaks += search_peaks(neighbor, graph, peaks)
    return reachable_peaks

if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        data = [[int(i) for i in list(line.strip())] for line in file]

        reachable_peaks = find_reachable_peaks_with_multiplicity(data)

        print("\n--- Part one ---")

        head_scores = [len(set(peaks)) for peaks in reachable_peaks]
        print(f"Total score: {sum(head_scores)}")

        print("\n--- Part two ---")

        head_ratings = [len(peaks) for peaks in reachable_peaks]
        print(f"Total rating: {sum(head_ratings)}")

        # exit(0)
