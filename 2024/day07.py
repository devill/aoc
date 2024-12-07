import os
from utils import data_files_for

def parse_line(line):
    result_part, operands_part = line.split(':')
    result_value = int(result_part.strip())
    operands = list(map(int, operands_part.strip().split()))
    return {"result": result_value, "operands": operands}

def hasSolution(result, operands):
    if result < 0:
        return False
    if len(operands) == 0:
        return result == 0

    last_operand = operands[-1]
    remaining_operands = operands[:-1]

    if result % last_operand == 0:
        if hasSolution(result // last_operand, remaining_operands):
            return True

    return hasSolution(result - last_operand, remaining_operands)


if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):

        data = [parse_line(line) for line in file]

        print("\n--- Part one ---")

        solvable = [line['result'] for line in data if hasSolution(line["result"], line["operands"])]

        print(f"Number of solvable equations: {len(solvable)}")
        print(f"Sum of solutions: {sum(solvable)}")

        print("\n--- Part two ---")

        # exit(0)