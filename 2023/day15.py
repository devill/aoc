import unittest

class TestHashAlgorithm(unittest.TestCase):
    def test_hash_examples(self):
        test_data = [
            ("rn=1", 30),
            ("cm-", 253),
            ("qp=3", 97),
            ("cm=2", 47),
            ("qp-", 14),
            ("pc=4", 180),
            ("ot=9", 9),
            ("ab=5", 197),
            ("pc-", 48),
            ("pc=6", 214),
            ("ot=7", 231)
        ]

        for input_string, expected_output in test_data:
            with self.subTest(input_string=input_string, expected_output=expected_output):
                self.assertEqual(hash_algorithm(input_string), expected_output)

    def test_initialization_sequence(self):
        sequence = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
        expected_sum = 1320
        self.assertEqual(process_initialization_sequence(sequence), expected_sum)

    def test_process_file(self):
        expected_result = 514025  # Updated with the actual expected result
        self.assertEqual(process_file("input15.txt"), expected_result)

    def test_parse_step(self):
        test_data = [
            ("rn=1", ("rn", "insert", 1)),
            ("cm-", ("cm", "remove", None)),
            ("qp=3", ("qp", "insert", 3)),
            ("pc-", ("pc", "remove", None))
        ]

        for step, expected_output in test_data:
            with self.subTest(step=step):
                self.assertEqual(parse_initialization_step(step), expected_output)

    def test_lens_operations(self):
        operations = ["rn=1", "cm-", "qp=3", "cm=2", "qp-", "pc=4", "ot=9", "ab=5", "pc-", "pc=6", "ot=7"]
        expected_boxes = {
            0: [("rn", 1), ("cm", 2)],
            3: [("ot", 7), ("ab", 5), ("pc", 6)]
        }
        self.assertEqual(perform_operations(operations), expected_boxes)

    def test_focusing_power(self):
        boxes = {
            0: [("rn", 1), ("cm", 2)],
            3: [("ot", 7), ("ab", 5), ("pc", 6)]
        }
        expected_focusing_power = 145  # As calculated in the puzzle example
        self.assertEqual(calculate_focusing_power(boxes), expected_focusing_power)

    def test_process_file_for_focusing_power(self):
        expected_result = 244461  # Updated with the actual expected result
        self.assertEqual(process_file_for_focusing_power("input15.txt"), expected_result)

def hash_algorithm(hash_string):
    current_value = 0
    for char in hash_string:
        ascii_code = ord(char)
        current_value += ascii_code
        current_value *= 17
        current_value %= 256
    return current_value

def process_initialization_sequence(sequence):
    hashes = sequence.split(',')
    return sum(hash_algorithm(hash_string) for hash_string in hashes)

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()  # Removing any trailing newlines or spaces
    return process_initialization_sequence(content)

def parse_initialization_step(step):
    label, operation = step.split('-', 1) if '-' in step else step.split('=', 1)
    operation_type = "remove" if '-' in step else "insert"
    focal_length = None if operation_type == "remove" else int(operation)
    return label, operation_type, focal_length


def perform_operations(operations):
    boxes = {}
    for op in operations:
        label, operation_type, focal_length = parse_initialization_step(op)
        box_index = hash_algorithm(label)

        if operation_type == "insert":
            if box_index not in boxes:
                boxes[box_index] = []
            for i, lens in enumerate(boxes[box_index]):
                if lens[0] == label:
                    boxes[box_index][i] = (label, focal_length)
                    break
            else:
                boxes[box_index].append((label, focal_length))

        elif operation_type == "remove":
            if box_index in boxes:
                boxes[box_index] = [lens for lens in boxes[box_index] if lens[0] != label]
                if not boxes[box_index]:  # Remove the box if it becomes empty
                    del boxes[box_index]

    return boxes

def calculate_focusing_power(boxes):
    total_power = 0
    for box_index, lenses in boxes.items():
        for slot, (label, focal_length) in enumerate(lenses, start=1):
            power = (box_index + 1) * slot * focal_length
            total_power += power
    return total_power

def process_file_for_focusing_power(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
    operations = content.split(',')
    boxes = perform_operations(operations)
    return calculate_focusing_power(boxes)


if __name__ == '__main__':
    unittest.main()
