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
    file_id = 0
    i = 0
    while i < len(compressed_disk_map):

        disk_map.extend([file_id] * compressed_disk_map[i])
        if i + 1 < len(compressed_disk_map):
            disk_map.extend([None] * compressed_disk_map[i + 1])
        file_id += 1
        i += 2
    return disk_map

def print_map(disk_map):
    print(''.join([ str(i) if i != None else "." for i in disk_map]))


def file_defragment(input_disk_map):
    disk_map = input_disk_map.copy()
    n = len(disk_map)

    def find_block_start(end):
        file_id = disk_map[end]
        start = end
        while start >= 0 and disk_map[start] == file_id:
            start -= 1
        return start + 1

    def find_none_sequence(length):
        start = 0
        while start < n:
            if disk_map[start] is None:
                end = start
                while end < n and disk_map[end] is None:
                    end += 1
                if end - start >= length:
                    return start, end
                start = end - 1
            start += 1
        return None, None

    i = n - 1
    moved = set()
    while i >= 0:
        if disk_map[i] is not None and disk_map[i] not in moved:
            moved.add(disk_map[i])
            block_end = i + 1
            block_start = find_block_start(i)
            block_length = block_end - block_start

            none_start, none_end = find_none_sequence(block_length)
            if none_start is not None and none_end < block_start:
                disk_map[none_start:none_start + block_length] = disk_map[block_start:block_end]
                disk_map[block_start:block_end] = [None] * block_length

            i = block_start - 1
        else:
            i -= 1

    return disk_map


if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        data = []
        for line in file:
            data = [ int(i) for i in list(line.strip())]

        print(len(data))

        print("\n--- Part one ---")

        disk_map = generate_disk_map(data)

        defragmented_disk_map = defragment(disk_map)

        checksum = calculate_checksum(defragmented_disk_map)
        print(f"Checksum: {checksum}")

        print("\n--- Part two ---")

        disk_map = generate_disk_map(data)
        
        file_defragmented_disk_map = file_defragment(disk_map)
        
        checksum = calculate_checksum(file_defragmented_disk_map)
        print(f"Checksum: {checksum}")

        # 6359213660505 too low
        # 6381625147860 too high
        # 6381625147860

        # exit(0)