import unittest

class HotSprings:
    def parse_line(self, line):
        parts = line.split(' ')
        spring_conditions = list(parts[0])
        group_sizes = [int(x) for x in parts[1].split(',')]
        return (spring_conditions, group_sizes)

    def unfold(self, line):
        conditions, groups = line.split(' ')
        unfolded_conditions = '?'.join([conditions] * 5)
        unfolded_groups = ','.join([groups] * 5)
        return unfolded_conditions + ' ' + unfolded_groups

    def validate_input(self, springs, groups, valid_until=(0, 0)):
        block_index = valid_until[1]
        block_size = 0
        valid_until_index = valid_until[0]

        for index in range(valid_until_index, len(springs)):
            c = springs[index]
            if c == '?':
                return True, (valid_until_index, block_index)
            elif c == '#':
                if block_index >= len(groups):
                    return False, (valid_until_index, block_index)
                block_size += 1
            else:  # c is '.'
                if block_size > 0:
                    if block_size != groups[block_index]:
                        return False, (valid_until_index, block_index)
                    block_size = 0
                    block_index += 1
                valid_until_index = index + 1

        # Check the last block if it exists
        if block_size > 0:
            if block_index != len(groups) - 1 or block_size != groups[-1]:
                return False, (valid_until_index, block_index)
            else:
                return True, (len(springs), len(groups))

        return block_index == len(groups), (len(springs), block_index)

    def count_arrangements(self, line):
        springs, groups = self.parse_line(line)
        num_hash = springs.count('#')
        num_question = springs.count('?')
        total_group_length = sum(groups)
        self.cache = {}
        return self.count_memo(springs, groups, num_hash, num_question, total_group_length)

    def count_memo(self, springs, groups, num_hash, num_question, total_group_length, valid_until=(0, 0)):
        if (num_hash, valid_until) in self.cache:
            return self.cache[(num_hash, valid_until)]
        result = self.count(springs, groups, num_hash, num_question, total_group_length, valid_until)
        self.cache[(num_hash, valid_until)] = result
        return result

    def count(self, springs, groups, num_hash, num_question, total_group_length, valid_until=(0, 0)):
        if total_group_length < num_hash or total_group_length > num_hash + num_question:
            return 0

        is_valid, valid_until = self.validate_input(springs, groups, valid_until)
        if not is_valid:
            return 0
        if '?' not in springs:
            return 1

        index = springs.index('?')
        count = 0
        for replacement in ['.', '#']:
            new_springs = springs[:]
            new_springs[index] = replacement
            count += self.count_memo(new_springs, groups, num_hash if replacement == '.' else num_hash + 1, num_question - 1, total_group_length, valid_until)
        return count


class TestHotSprings(unittest.TestCase):
    def test_parse_line(self):
        hot_springs = HotSprings()
        expected_output = (['?', '?', '?', '.', '#', '#', '#'], [1, 1, 3])
        self.assertEqual(hot_springs.parse_line("???.### 1,1,3"), expected_output)


    def test_validate_input_with_valid_until(self):
        hot_springs = HotSprings()
        test_cases = [
            (list("#.#"), [1, 1], (3, 2)),
            (list("#.#."), [1, 1], (4, 2)),
            (list("#.#.?.#"), [1, 1, 1], (4, 2)),
            (list("#.##?.#"), [1, 3, 1], (2, 1)),
            (list("?.#"), [1, 1], (0, 0)),
            (list("##..##."), [2, 1], (4, 1))
        ]

        for springs, groups, expected in test_cases:
            with self.subTest(springs=springs, groups=groups, expected=expected):
                self.assertEqual(hot_springs.validate_input(springs, groups)[1], expected)


    def test_count_arrangements(self):
        hot_springs = HotSprings()
        self.assertEqual(hot_springs.count_arrangements("???.### 1,1,3"), 1)
        self.assertEqual(hot_springs.count_arrangements(".??..??...?##. 1,1,3"), 4)
        self.assertEqual(hot_springs.count_arrangements("?###???????? 3,2,1"), 10)

    def test_unfold_line(self):
        hot_springs = HotSprings()
        self.assertEqual(hot_springs.unfold(".# 1"), ".#?.#?.#?.#?.# 1,1,1,1,1")
        self.assertEqual(hot_springs.unfold("???.### 1,1,3"), "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3")

    def test_on_real_input(self):
        unfolded_total_count = 0
        total_count = 0
        hot_springs = HotSprings()

        with open('input12.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    total_count += hot_springs.count_arrangements(line)
                    unfolded_line = hot_springs.unfold(line)
                    unfolded_total_count += hot_springs.count_arrangements(unfolded_line)

        self.assertEquals(total_count, 7674) # Part One
        self.assertEquals(unfolded_total_count, 4443895258186) # Part Two

unittest.main()