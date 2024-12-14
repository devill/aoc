import os
from utils import data_files_for

def parse_file(file):
    column1 = []
    column2 = []

    for line in file:
        num1, num2 = map(int, line.split())
        column1.append(num1)
        column2.append(num2)

    return column1, column2

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        print("\n--- Part one ---")

        column1, column2 = parse_file(file)

        # Sort both columns in ascending order
        column1.sort()
        column2.sort()

        # Calculate pairwise differences between the two columns
        differences = [abs(num1 - num2) for num1, num2 in zip(column1, column2)]

        print("Sum of differences:", sum(differences))

        print("\n--- Part two ---")

        # Count the number of occurences of each number in column2 in a dictionary
        column2_dict = {}
        for num in column2:
            column2_dict[num] = column2_dict.get(num, 0) + 1

        similarities = [column2_dict.get(i, 0) * i for i in column1]
        print("Sum of similarities:", sum(similarities))