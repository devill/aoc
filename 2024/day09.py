import os
from utils import data_files_for

def defragment(input_disk_map):
    disk_map = input_disk_map.copy()
    n = len(disk_map)
    first_none = 0
    last_none = n - 1

    while first_none < last_none:
        while first_none < n and disk_map[first_none] is not None:
            first_none += 1
        while last_none >= 0 and disk_map[last_none] is None:
            last_none -= 1
        if first_none < last_none:
            disk_map[first_none], disk_map[last_none] = disk_map[last_none], disk_map[first_none]

    return disk_map


def calculate_checksum(defragmented_disk_map):
    checksum = 0
    for block, i in enumerate(defragmented_disk_map):
        p = checksum
        if i is not None:
            checksum += block * i
            #print(f"{block} * {i} = {block * i} -> {p} + {block * i} = {checksum}")

    return checksum


def generate_disk_map(compressed_disk_map):

    disk_map = []
    file_locations = []
    file_lengths = []
    file_id = 0
    i = 0
    while i < len(compressed_disk_map):

        file_locations.append(len(disk_map))
        file_lengths.append(compressed_disk_map[i])
        disk_map.extend([file_id] * compressed_disk_map[i])
        if i + 1 < len(compressed_disk_map):
            disk_map.extend([None] * compressed_disk_map[i + 1])
        file_id += 1
        i += 2
    return (disk_map, file_locations, file_lengths)

def print_map(disk_map):
    print(''.join([ str(i) if i != None else "." for i in disk_map]))


def file_defragment(input_disk_map, file_locations, file_lengths):
    disk_map = input_disk_map.copy()

    def find_none_sequence(length):
        start = 0
        while start < len(disk_map):
            if disk_map[start] is None:
                end = start
                while end < len(disk_map) and disk_map[end] is None:
                    end += 1
                if end - start >= length:
                    return start, end
            start += 1
        return None, None

    n = len(file_locations) - 1
    while n > 0:
        # print(n)
        # print_map(disk_map)
        start, end = find_none_sequence(file_lengths[n])
        if start is not None and start < file_locations[n]:
            disk_map[start:start + file_lengths[n]] = [n] * file_lengths[n]
            disk_map[file_locations[n]:file_locations[n] + file_lengths[n]] = [None] * file_lengths[n]
        n -= 1

    return disk_map


if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        data = []
        for line in file:
            data = [ int(i) for i in list(line.strip())]

        print(len(data))

        print("\n--- Part one ---")

        disk_map, _, _ = generate_disk_map(data)

        defragmented_disk_map = defragment(disk_map)

        checksum = calculate_checksum(defragmented_disk_map)
        print(f"Checksum: {checksum}")

        print("\n--- Part two ---")

        disk_map, file_locations, file_lengths  = generate_disk_map(data)
        # print(file_locations, file_lengths)

        file_defragmented_disk_map = file_defragment(disk_map, file_locations, file_lengths)

        checksum = calculate_checksum(file_defragmented_disk_map)
        print(f"Checksum: {checksum}")

        # exit(0)