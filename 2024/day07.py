import os
from utils import data_files_for

def parse_line(line):
    result_part, operands_part = line.split(':')
    result_value = int(result_part.strip())
    operands = list(map(int, operands_part.strip().split()))
    return (result_value, operands)

def hasSolution(result, operands, use_concentration):
    if result < 0:
        return False
    if len(operands) == 0:
        return result == 0

    last_operand = operands[-1]
    remaining_operands = operands[:-1]

    if result % last_operand == 0:
        if hasSolution(result // last_operand, remaining_operands, use_concentration):
            return True

    if hasSolution(result - last_operand, remaining_operands, use_concentration):
        return True

    if use_concentration:
        digits = len(str(last_operand))
        if str(result)[-digits:] == str(last_operand):
            newResult = int(str(result)[:-digits])
            if hasSolution(newResult, remaining_operands, use_concentration):
                return True

    return False



if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):

        data = [parse_line(line) for line in file]

        print("\n--- Part one ---")

        solvable = [
            result for result, operands in data if hasSolution(result, operands, False)
        ]

        print(f"Number of solvable equations: {len(solvable)}")
        print(f"Sum of solutions: {sum(solvable)}")

        print("\n--- Part two ---")

        solvable = [
            result for result, operands in data if hasSolution(result, operands, True)
        ]

        print(f"Number of solvable equations: {len(solvable)}")
        print(f"Sum of solutions: {sum(solvable)}")

        # exit(0)