import sys

def parse_file(filename):
    column1 = []
    column2 = []

    with open(filename, 'r') as file:
        for line in file:
            num1, num2 = map(int, line.split())
            column1.append(num1)
            column2.append(num2)

    return column1, column2

if __name__ == "__main__":
    if len(sys.argv) != 2:
        choice = input("Choose input file - production (i) or test (t): ").strip().lower()
        if choice == 'i':
            filename = 'input01.txt'
        elif choice == 't':
            filename = 'test01.txt'
        else:
            print("Invalid choice. Exiting.")
            sys.exit(1)
    else:
        filename = sys.argv[1]


    print("\n--- Part one ---")

    column1, column2 = parse_file(filename)

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