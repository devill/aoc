import os
from utils import data_files_for

def transform_stones(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            half_len = len(str(stone)) // 2
            left_half = int(str(stone)[:half_len])
            right_half = int(str(stone)[half_len:])
            new_stones.extend([left_half, right_half])
        else:
            new_stones.append(stone * 2024)
    return new_stones

def transform_stones_25(stones):
    for i in range(25):
        stones = transform_stones(stones)
    return stones


if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        stones = list(map(int, file.readline().strip().split()))

        print("\n--- Part one ---")

        stones = transform_stones_25(stones)

        print(len(stones))

        print("\n--- Part two ---")


        memo = {}
        for j in range(2):
            next_stones = []
            for stone in stones:
                if stone in memo:
                    next_stones.extend(memo[stone])
                else:
                    result = transform_stones_25([stone])
                    memo[stone] = result
                    next_stones.extend(result)
            stones = next_stones
            print(j, len(stones))
        print(len(stones))