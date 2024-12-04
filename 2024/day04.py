import os
from utils import data_files_for

if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        data = []
        for line in file:
            data.append(line.strip())

        print("\n--- Part one ---")

        count = 0

        for i in range(len(data)):
            for j in range(len(data[i])-3):
                if data[i][j:j+4] in ['XMAS', 'SAMX']:
                    count += 1

        for i in range(len(data)-3):
            for j in range(len(data[i])):
                column = ''.join([data[i][j], data[i+1][j], data[i+2][j], data[i+3][j]])
                if column in ['XMAS', 'SAMX']:
                    count += 1

        for i in range(len(data)-3):
            for j in range(len(data[i])-3):
                diag1 = ''.join([data[i][j], data[i+1][j+1], data[i+2][j+2], data[i+3][j+3]])
                if diag1 in ['XMAS', 'SAMX']:
                    count += 1
                diag2 = ''.join([data[i][j+3], data[i+1][j+2], data[i+2][j+1], data[i+3][j]])
                if diag2 in ['XMAS', 'SAMX']:
                    count += 1

        print(count)

        print("\n--- Part two ---")

        count = 0
        for i in range(len(data)-2):
            for j in range(len(data[i])-2):
                diag1 = ''.join([data[i][j], data[i+1][j+1], data[i+2][j+2]])
                diag2 = ''.join([data[i][j+2], data[i+1][j+1], data[i+2][j]])
                if diag1 in ['MAS','SAM'] and diag2 in ['MAS','SAM']:
                    count += 1
        print(count)

        # exit(0)