import os
from utils import data_files_for

import re
import numpy as np

def parse_input(input_text, modifyer = 0):
    machines = []
    machine_pattern = re.compile(
        r"Button A: X\+(\d+), Y\+(\d+)\n"
        r"Button B: X\+(\d+), Y\+(\d+)\n"
        r"Prize: X=(\d+), Y=(\d+)"
    )
    matches = machine_pattern.findall(input_text)
    for match in matches:
        A_x, A_y, B_x, B_y, prize_x, prize_y = map(int, match)
        machines.append(((A_x, A_y, B_x, B_y), (prize_x+modifyer, prize_y+modifyer)))
    return machines

def find_min_tokens(buttons, prize):
    A_x, A_y, B_x, B_y = buttons
    prize_x, prize_y = prize

    # Coefficients matrix and right-hand side vector
    coefficients = np.array([[A_x, B_x], [A_y, B_y]])
    rhs = np.array([prize_x, prize_y])

    try:
        # Check if an integer solution exists
        solution = np.linalg.solve(coefficients, rhs)

        if np.allclose(solution, np.round(solution)) and np.all(solution >= 0):
            a_presses, b_presses = map(int, np.round(solution))
            if a_presses*A_x + b_presses*B_x != prize_x or a_presses*A_y + b_presses*B_y != prize_y:
                return None
            return 3 * a_presses + b_presses

    except np.linalg.LinAlgError:
        return None
    return None

def calculate_total_tokens(machines):

    total_tokens = 0
    prizes_won = 0

    for idx, (buttons, prize) in enumerate(machines):
        min_tokens = find_min_tokens(buttons, prize)
        if min_tokens is not None:
            prizes_won += 1
            total_tokens += min_tokens

    return prizes_won, total_tokens


if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        input_text = file.read()

        print("\n--- Part one ---")

        machines = parse_input(input_text)
        prizes, tokens = calculate_total_tokens(machines)
        # print(f"\nMaximum prizes won: {prizes}")
        print(f"Total minimum tokens spent: {tokens}")

        print("\n--- Part two ---")

        machines = parse_input(input_text, 10000000000000)
        prizes, tokens = calculate_total_tokens(machines)
        # print(f"\nMaximum prizes won: {prizes}")
        print(f"Total minimum tokens spent: {tokens}")