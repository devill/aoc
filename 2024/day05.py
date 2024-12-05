import os
import re
from utils import data_files_for

def is_correctly_ordered(update, follows):
    banned = set()
    for page in update:
        if page in banned:
            return False
        if str(page) in follows:
            banned.add(follows[str(page)])
    return True

if __name__ == "__main__":
    for file in data_files_for(os.path.basename(__file__)):
        precedes = {}
        follows = {}
        updates = []
        rulePattern = re.compile(r'(\d+)\|(\d+)')
        listPattern = re.compile(r'(\d+,)+\d+')
        for line in file:
            ruleMatch = rulePattern.match(line)
            if ruleMatch:
                precedes[ruleMatch.group(1)] = ruleMatch.group(2)
                follows[ruleMatch.group(2)] = ruleMatch.group(1)
            elif listPattern.match(line):
                updates.append([int(num) for num in line.split(',')])

        print("\n--- Part one ---")


        correct = [update for update in updates if is_correctly_ordered(update, follows)]

        print(f"Correctly ordered updates: {len(correct)}")
        print(correct)

        print("\n--- Part two ---")

        exit(0)