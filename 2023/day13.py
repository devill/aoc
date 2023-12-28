import unittest
import re

def parse_pattern(pattern):
    return list(map(lambda l: list(l), pattern.split("\n")))

def parse_patterns(patterns_text):
    return list(map(lambda p: parse_pattern(p), patterns_text.strip('\n').split("\n\n")))

def parse_test_cases(test_cases_text):
    # Regular expression to capture test case metadata and patterns
    test_case_regex = r"\[(.*?) - (.*?) - expected: ([^\]]+)\]\n(.*?)\n(?=\[|$)"
    test_cases = []

    # Joining the list of lines into a single string for regex matching
    test_cases_text = ''.join(test_cases_text)

    # Finding all matches in the test_cases_text
    matches = re.findall(test_case_regex, test_cases_text, re.DOTALL)
    for match in matches:
        name, function, expected, patterns_text = match
        test_case = {
            "name": name,
            "function": function,
            "expected": expected,
            "patterns": parse_patterns(patterns_text)
        }
        test_cases.append(test_case)

    return test_cases


class TestParsingFunctions(unittest.TestCase):
    def test_parse_patterns(self):
        patterns_text = """#.#
.#.
#.#

..#
#..
..#
"""
        expected = [[["#", ".", "#"], [".", "#", "."], ["#", ".", "#"]],
                    [[".", ".", "#"], ["#", ".", "."], [".", ".", "#"]]]
        self.assertEqual(parse_patterns(patterns_text), expected)

    def test_parse_test_cases(self):
        test_cases_text = ["[Test Case 1 - horizontal_reflection() - expected: 2]\n", "#.#\n", ".#.\n", "#.#\n", "\n",
                           "[Test Case 2 - vertical_reflection() - expected: 3]\n", "..#\n", "#..\n", "..#\n"]
        expected = [
            {"name": "Test Case 1", "function": "horizontal_reflection()", "expected": "2",
             "patterns": [[["#", ".", "#"], [".", "#", "."], ["#", ".", "#"]]]},
            {"name": "Test Case 2", "function": "vertical_reflection()", "expected": "3",
             "patterns": [[[".", ".", "#"], ["#", ".", "."], [".", ".", "#"]]]}
        ]
        self.assertEqual(parse_test_cases(test_cases_text), expected)

    def test_real_data(self):
        with open('input13.txt', 'r') as file:
            data = file.read()

            score_1 = reflection_score(parse_patterns(data))
            self.assertEqual(score_1, 27202)

            score_2 = reflection_score_smudges(parse_patterns(data))
            self.assertEqual(score_2, 41566)

def horizontal_reflection(pattern):
    total = 0
    items = []
    l = len(pattern)
    for i in range(1, l, 1):
        w = min(i, l - i)
        if horizontal_sub_reflection(pattern[i-w:i+w]):
            total += i
            items.append(i)

    return (total, items)

def horizontal_sub_reflection(pattern):
    num_rows = len(pattern)

    for i in range(num_rows // 2):
        if pattern[i] != pattern[num_rows - i - 1]:
            return False

    return True  # Correct reflection found, return half the number of rows

def vertical_reflection(pattern):
    # Transpose the pattern
    transposed_pattern = [list(row) for row in zip(*pattern)]
    return horizontal_reflection(transposed_pattern)

def reflection_score(patterns):
    total_score = 0
    for i, pattern in enumerate(patterns):
        score = 100*horizontal_reflection(pattern)[0] + vertical_reflection(pattern)[0]
        total_score += score
    return total_score

def desmudge(pattern):
    smudge = horizontal_smudges(pattern)
    if not smudge:
        transposed_pattern = [list(row) for row in zip(*pattern)]
        smudge = horizontal_smudges(transposed_pattern)
        smudge = (smudge[1],smudge[0])
    if smudge:
        result = [l[:] for l in pattern]
        result[smudge[0]][smudge[1]] = '#'
        return result
    return None

def horizontal_smudges(pattern):
    l = len(pattern)
    for i in range(1, l):
        w = min(i, l - i)
        smudges = horizontal_sub_smudges(pattern[i-w:i+w])
        if len(smudges) == 1:
            return (smudges[0][0] + (i - w), smudges[0][1])
    return None

def horizontal_sub_smudges(pattern):
    num_rows = len(pattern)
    smudges = []
    for i in range(num_rows // 2):
        for j in range(len(pattern[i])):
            if pattern[i][j] != pattern[num_rows - i - 1][j]:
                if pattern[i][j] == '.':
                    smudges.append((i,j))
                else:
                    smudges.append((num_rows - i - 1,j))
    return smudges


def reflection_score_smudges(patterns):
    total_score = 0
    for i, pattern in enumerate(patterns):
        desmudged = desmudge(pattern)
        ohr = horizontal_reflection(pattern)[1]
        dhr = horizontal_reflection(desmudged)[1]
        nhr = [i for i in dhr if i not in ohr]

        ovr = vertical_reflection(pattern)[1]
        dvr = vertical_reflection(desmudged)[1]
        nvr = [i for i in dvr if i not in ovr]

        score = 100*sum(nhr) + sum(nvr)
        total_score += score
    return total_score


class MirrorReflectionDetectionTests(unittest.TestCase):

    def test_reflection_detection(self):
        with open('test13.txt', 'r') as file:
            test_cases = file.readlines()
        parsed_test_cases = parse_test_cases(test_cases)

        for test in parsed_test_cases:
            with self.subTest(test['name']):
                result = 0
                expected = None
                if test['function'] == 'horizontal_reflection()':
                    result = horizontal_reflection(test['patterns'][0])[0]
                    expected = int(test['expected'])
                elif test['function'] == 'vertical_reflection()':
                    result = vertical_reflection(test['patterns'][0])[0]
                    expected = int(test['expected'])
                elif test['function'] == 'reflection_score()':
                    result = reflection_score(test['patterns'])
                    expected = int(test['expected'])
                elif test['function'] == 'reflection_score_smudges()':
                    result = reflection_score_smudges(test['patterns'])
                    expected = int(test['expected'])
                elif test['function'] == 'desmudge()':
                    result = desmudge(test['patterns'][0])

                    x, y = list(map(lambda x: int(x), test['expected'].strip('()').split(',')))
                    expected = [l[:] for l in test['patterns'][0]]
                    expected[y][x] = '#'
                else:
                    print(test)
                self.assertEqual(result, expected)


unittest.main()
