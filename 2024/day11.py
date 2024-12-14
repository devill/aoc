import os
from utils import data_files_for

memo = {}

def result_length(n, remaining_blinks): 
    if remaining_blinks == 0:
        return 1
    elif (n, remaining_blinks) in memo:
        return memo[(n, remaining_blinks)]
    elif n == 0:
        r = result_length(1, remaining_blinks - 1)
        memo[(n, remaining_blinks)] = r
        return r
    elif len(str(n)) % 2 == 0:
        half_len = len(str(n)) // 2
        left_half = int(str(n)[:half_len])
        right_half = int(str(n)[half_len:])
        r = result_length(left_half, remaining_blinks - 1) +result_length(right_half, remaining_blinks-1)
        memo[(n, remaining_blinks)] = r
        return r
    else:
        r = result_length(n * 2024, remaining_blinks - 1)
        memo[(n, remaining_blinks)] = r
        return r

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        stones = list(map(int, file.readline().strip().split()))

        print("\n--- Part one ---")

        print(sum([result_length(n,25) for n in stones]))

        print("\n--- Part two ---")

        print(sum([result_length(n,75) for n in stones]))

        
