
import sys
from functools import reduce

def first_unsafe_level(levels):
    direction = levels[-1] - levels[0]
    if direction == 0:
        return 0

    for i in range(1, len(levels)):
        if abs(levels[i] - levels[i - 1]) > 3:
            return i
        if levels[i] == levels[i - 1]:
            return i
        if (levels[i] - levels[i - 1]) * direction < 0:
            return i
    return -1

def is_safe(levels):
    return first_unsafe_level(levels) == -1

def count_safe_levels(levels):
    return reduce(lambda count, level: count + (1 if is_safe(level) else 0), levels, 0)

def is_almost_safe(levels):
    if is_safe(levels):
        return True
    unsafe = first_unsafe_level(levels)

    remaining_levels = levels[:unsafe] + levels[unsafe + 1:]

    if is_safe(remaining_levels):
        return True

    for i in range(0, len(levels) - 1):
        remaining_levels = levels[:i] + levels[i + 1:]
        if is_safe(remaining_levels):
            return True

    return False

def count_almost_safe_levels(levels):
    return reduce(lambda count, level: count + (1 if is_almost_safe(level) else 0), levels, 0)

def parse_file(filename):
    with open(filename, 'r') as file:
        reports = []
        for line in file:
            # Parse the items in the line as integers
            levels = list(map(int, line.split()))
            reports.append(levels)
    return reports

if __name__ == "__main__":
    filename = None

    if len(sys.argv) != 2:
        choice = input("Choose input file - production (i) or test (t): ").strip().lower()
        if choice == 'i':
            filename = 'input02.txt'
        elif choice == 't':
            filename = 'test02.txt'
        else:
            print("Invalid choice. Exiting.")
            sys.exit(1)
    else:
        filename = sys.argv[1]

    parsed_data = parse_file(filename)

    print("\n--- Part one ---")
    print(count_safe_levels(parsed_data))
    print("\n--- Part two ---")
    print(count_almost_safe_levels(parsed_data))