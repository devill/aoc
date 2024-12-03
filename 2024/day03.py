import os
import re
from utils import data_files_for

def parse_file(file):
    input = []
    for line in file:
        input.append(line.strip())
    return input

def parse_line_one(line):
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    matches = re.findall(pattern, line)
    return [(int(match[0]), int(match[1])) for match in matches]

def parse_line_two(line):
    pattern = r'(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))'
    matches = re.findall(pattern, line)

    result = []
    skip = False

    for match in matches:
        if match[0] == "don't()":
            skip = True
        elif match[0] == "do()":
            skip = False
        elif match[0].startswith('mul') and not skip:
            result.append((int(match[1]), int(match[2])))

    return result

def calculate_sum_of_products(parsed_line):
    return sum([a * b for a, b in parsed_line])

if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        parsed_data = parse_file(file)

        print("\n--- Part one ---")
        total = 0
        for line in parsed_data:

            parsed_line = parse_line_one(line)
            sum_of_products = calculate_sum_of_products(parsed_line)
            total += sum_of_products
        print(total)

        print("\n--- Part two ---")
        total = 0
        full_line = "".join(parsed_data)
        parsed_line = parse_line_two(full_line)
        print(parsed_line)
        total += calculate_sum_of_products(parsed_line)
        print(total)

        # exit(0)
