import os
import re
from utils import data_files_for

class Rules:
    def __init__(self):
        self.precedes = {}
        self.follows = {}

    def add_rule(self, a, b):
        if b not in self.precedes:
            self.precedes[b] = []
        if a not in self.follows:
            self.follows[a] = []
        self.precedes[b].append(a)
        self.follows[a].append(b)

    def cant_follow(self, page):
        return self.precedes.get(page, [])

    def cant_precede(self, page):
        return self.follows.get(page, [])

def is_correctly_ordered(update, rules):
    banned = set()
    banned_by = {}
    for page in update:

        if page in banned:
            return False
        banned.update(rules.cant_follow(page))
        for banned_page in rules.cant_follow(page):
            if banned_page not in banned_by:
                banned_by[banned_page] = []
            banned_by[banned_page].append(page)
    return True

if __name__ == "__main__":

    rulePattern = re.compile(r'(\d+)\|(\d+)')
    listPattern = re.compile(r'(\d+,)+\d+')

    for file in data_files_for(os.path.basename(__file__)):
        rules = Rules()
        updates = []

        for line in file:
            ruleMatch = rulePattern.match(line)
            if ruleMatch:
                rules.add_rule(int(ruleMatch.group(1)), int(ruleMatch.group(2)))
            elif listPattern.match(line):
                updates.append([int(num) for num in line.split(',')])

        print("\n--- Part one ---")

        correct = [update for update in updates if is_correctly_ordered(update, rules)]
        midNumber = [c[(len(c) - 1) // 2] for c in correct]

        print(f"Correctly ordered updates: {len(correct)}")
        print(f"Solution: {sum(midNumber)}")

        print("\n--- Part two ---")

