import unittest
import re


class TestWorkflowParser(unittest.TestCase):
    def test_parse_single_workflow(self):
        workflow_string = "ex{x>10:one,m<20:two,a>30:R,A}"
        expected = {
            "name": "ex",
            "rules": [
                {"condition": {"attribute": "x", "operator": ">", "value": 10}, "action": "one"},
                {"condition": {"attribute": "m", "operator": "<", "value": 20}, "action": "two"},
                {"condition": {"attribute": "a", "operator": ">", "value": 30}, "action": "R"},
                {"condition": None, "action": "A"}
            ]
        }
        result = WorkflowParser.parse_workflow(workflow_string)
        self.assertEqual(result, expected)

    def test_parse_single_part_ratings(self):
        ratings_string = "{x=787,m=2655,a=1222,s=2876}"
        expected = {"x": 787, "m": 2655, "a": 1222, "s": 2876}
        result = WorkflowParser.parse_part_ratings(ratings_string)
        self.assertEqual(result, expected)

    def test_parse_condition(self):
        condition_string = "x>10"
        expected = {"attribute": "x", "operator": ">", "value": 10}
        result = WorkflowParser.parse_condition(condition_string)
        self.assertEqual(result, expected)

    def test_parse_full_puzzle_input(self):
        puzzle_input = (
            "ex{x>10:one,m<20:two,a>30:R,A}\n"
            "ab{m<5:three,x=15:four,s>100:R,A}\n\n"
            "{x=25,m=4,a=30,s=105}\n"
            "{x=15,m=7,a=20,s=95}\n"
        )
        expected = {
            "workflows": {
                "ex": [
                        {"condition": {"attribute": "x", "operator": ">", "value": 10}, "action": "one"},
                        {"condition": {"attribute": "m", "operator": "<", "value": 20}, "action": "two"},
                        {"condition": {"attribute": "a", "operator": ">", "value": 30}, "action": "R"},
                        {"condition": None, "action": "A"}
                    ],
                "ab": [
                        {"condition": {"attribute": "m", "operator": "<", "value": 5}, "action": "three"},
                        {"condition": {"attribute": "x", "operator": "=", "value": 15}, "action": "four"},
                        {"condition": {"attribute": "s", "operator": ">", "value": 100}, "action": "R"},
                        {"condition": None, "action": "A"}
                    ]
            },
            "parts": [
                {"x": 25, "m": 4, "a": 30, "s": 105},
                {"x": 15, "m": 7, "a": 20, "s": 95}
            ]
        }
        result = WorkflowParser.parse_full_input(puzzle_input)
        self.assertEqual(result, expected)



class WorkflowParser:
    @staticmethod
    def parse_workflow(workflow_string):
        name, rules_str = workflow_string.split('{', 1)
        rules_str = rules_str.rstrip('}')
        rules = []
        for rule_str in rules_str.split(','):
            if ':' in rule_str:
                condition_str, action = rule_str.split(':', 1)
                condition = WorkflowParser.parse_condition(condition_str)
            else:
                condition, action = None, rule_str
            rules.append({"condition": condition, "action": action})
        return {"name": name, "rules": rules}

    @staticmethod
    def parse_part_ratings(ratings_string):
        ratings = ratings_string.strip("{}")
        return {k: int(v) for k, v in (rating.split("=") for rating in ratings.split(","))}

    @staticmethod
    def parse_condition(condition_string):
        attribute, operator, value = re.match(r"([a-z]+)([><=])(\d+)", condition_string).groups()
        return {"attribute": attribute, "operator": operator, "value": int(value)}


    @staticmethod
    def parse_full_input(puzzle_input):
        workflows_part, parts_part = puzzle_input.strip().split('\n\n')
        workflows = {}
        for wf in workflows_part.split('\n'):
            parsed_workflow = WorkflowParser.parse_workflow(wf)
            workflows[parsed_workflow['name']] = parsed_workflow['rules']
        parts = [WorkflowParser.parse_part_ratings(pr) for pr in parts_part.split('\n')]
        return {"workflows": workflows, "parts": parts}



class TestWorkflowAction(unittest.TestCase):
    def test_determine_workflow_action(self):
        workflow = [
            {"condition": {"attribute": "x", "operator": ">", "value": 10}, "action": "one"},
            {"condition": {"attribute": "m", "operator": "<", "value": 20}, "action": "two"},
            {"condition": {"attribute": "a", "operator": ">", "value": 30}, "action": "R"},
            {"condition": None, "action": "A"}
        ]
        part_ratings = {"x": 15, "m": 25, "a": 5}
        expected_action = "one"  # x > 10
        result = determine_workflow_action(workflow, part_ratings)
        self.assertEqual(result, expected_action)


def determine_workflow_action(workflow, part_ratings):
    for rule in workflow:
        if rule["condition"] is None:
            return rule["action"]
        attribute, operator, value = rule["condition"]["attribute"], rule["condition"]["operator"], rule["condition"]["value"]
        if operator == '>' and part_ratings[attribute] > value:
            return rule["action"]
        elif operator == '<' and part_ratings[attribute] < value:
            return rule["action"]
        elif operator == '=' and part_ratings[attribute] == value:
            return rule["action"]
    return None  # Fallback in case no rule matches



class TestProcessPartThroughWorkflows(unittest.TestCase):
    def test_process_part_through_workflows(self):
        workflows = {
            "in": [
                {"condition": {"attribute": "x", "operator": ">", "value": 100}, "action": "next_wf"},
                {"condition": None, "action": "A"}
            ],
            "next_wf": [
                {"condition": {"attribute": "m", "operator": "<", "value": 50}, "action": "R"},
                {"condition": None, "action": "A"}
            ]
        }
        part_ratings = {"x": 120, "m": 30}  # Should be rejected in next_wf
        expected_result = "Rejected"
        result = process_part_through_workflows(workflows, part_ratings)
        self.assertEqual(result, expected_result)

def process_part_through_workflows(workflows, part_ratings):
    current_workflow = "in"
    while True:
        action = determine_workflow_action(workflows[current_workflow], part_ratings)
        if action == "A":
            return "Accepted"
        elif action == "R":
            return "Rejected"
        else:  # Assuming action is the name of the next workflow
            current_workflow = action



class TestSolvePartOne(unittest.TestCase):
    def test_solve_part_one(self):
        with open("test19.txt", "r") as file:
            test19_content = file.read()
        expected_result = 19114
        result = solve_part_one(test19_content)
        self.assertEqual(result, expected_result)

    def test_solve_part_one_real_data(self):
        with open("input19.txt", "r") as file:
            test19_content = file.read()
        expected_result = 509597
        result = solve_part_one(test19_content)
        self.assertEqual(result, expected_result)

def solve_part_one(input_string):
    parsed_data = WorkflowParser.parse_full_input(input_string)
    workflows = parsed_data["workflows"]
    parts = parsed_data["parts"]

    total_ratings = 0
    for part in parts:
        result = process_part_through_workflows(workflows, part)
        if result == "Accepted":
            total_ratings += sum(part.values())
    return total_ratings


class TestReverseWorkflow(unittest.TestCase):
    def test_reverse_workflow(self):
        workflows = {
            "in": [
                {"condition": {"attribute": "x", "operator": ">", "value": 100}, "action": "next_wf"},
                {"condition": None, "action": "A"}
            ],
            "next_wf": [
                {"condition": {"attribute": "m", "operator": "<", "value": 50}, "action": "R"},
                {"condition": None, "action": "A"}
            ]
        }
        result = reverse_workflow(workflows)
        self.assertEqual(result, {
            'A': {"next_wf", "in"},
            'R': {"next_wf"},
            'next_wf': {"in"}
        })



def reverse_workflow(workflows):
    reversed_workflows = {}
    for wf_name, rules in workflows.items():
        for rule in rules:
            action = rule["action"]
            if action not in reversed_workflows:
                reversed_workflows[action] = set()
            reversed_workflows[action].add(wf_name)
    return reversed_workflows


class TestActionHyperCubes(unittest.TestCase):
    def test_hypercubes_for_action(self):
        workflow_string = "in{x>10:A,m<20:A,a>30:R,A}"
        workflows = { "in": WorkflowParser.parse_workflow(workflow_string)["rules"] }
        result = hypercubes_for_action(workflows, "A")
        expected_hypercubes = [
            {"x": {"min": 11, "max": 4000, "not": []}, "m": {"min": 1, "max": 4000, "not": []}, "a": {"min": 1, "max": 4000, "not": []}, "s": {"min": 1, "max": 4000, "not": []}},
            {"x": {"min": 1, "max": 10, "not": []}, "m": {"min": 1, "max": 19, "not": []}, "a": {"min": 1, "max": 4000, "not": []}, "s": {"min": 1, "max": 4000, "not": []}},
            {"x": {"min": 1, "max": 10, "not": []}, "m": {"min": 20, "max": 4000, "not": []}, "a": {"min": 1, "max": 30, "not": []}, "s": {"min": 1, "max": 4000, "not": []}}
        ]
        self.assertEqual(result, expected_hypercubes)

    def test_hypercubes_for_action_with_eq(self):
        workflow_string = "in{x=10:A,m<20:A,a>30:R,A}"
        workflows = { "in": WorkflowParser.parse_workflow(workflow_string)["rules"] }
        result = hypercubes_for_action(workflows, "A")
        expected_hypercubes = [
            {"x": {"min": 10, "max": 10, "not": []}, "m": {"min": 1, "max": 4000, "not": []}, "a": {"min": 1, "max": 4000, "not": []}, "s": {"min": 1, "max": 4000, "not": []}},
            {"x": {"min": 1, "max": 4000, "not": [10]}, "m": {"min": 1, "max": 19, "not": []}, "a": {"min": 1, "max": 4000, "not": []}, "s": {"min": 1, "max": 4000, "not": []}},
            {"x": {"min": 1, "max": 4000, "not": [10]}, "m": {"min": 20, "max": 4000, "not": []}, "a": {"min": 1, "max": 30, "not": []}, "s": {"min": 1, "max": 4000, "not": []}}
        ]
        self.assertEqual(result, expected_hypercubes)

    def test_hypercubes_for_action_failure_case(self):
        workflow_string = "in{x=10:R,x=10:A,R}"
        workflows = { "in": WorkflowParser.parse_workflow(workflow_string)["rules"] }
        result = hypercubes_for_action(workflows, "A")
        expected_hypercubes = []
        self.assertEqual(result, expected_hypercubes)

    def test_hypercubes_for_action_multi_step(self):
        workflows = {
            "in": [
                {"condition": {"attribute": "x", "operator": ">", "value": 100}, "action": "next_wf"},
                {"condition": None, "action": "A"}
            ],
            "next_wf": [
                {"condition": {"attribute": "m", "operator": "<", "value": 50}, "action": "R"},
                {"condition": None, "action": "A"}
            ]
        }
        result = hypercubes_for_action(workflows, "A")
        expected_hypercubes = [
            {
                "x": {"min": 101, "max": 4000, "not": []},
                "m": {"min": 50, "max": 4000, "not": []},
                "a": {"min": 1, "max": 4000, "not": []},
                "s": {"min": 1, "max": 4000, "not": []}
            },
            {
                "x": {"min": 1, "max": 100, "not": []},
                "m": {"min": 1, "max": 4000, "not": []},
                "a": {"min": 1, "max": 4000, "not": []},
                "s": {"min": 1, "max": 4000, "not": []}
            }
        ]
        self.assertEqual(result, expected_hypercubes)


    def test_hypercubes_for_action_intersections(self):
        workflows = {
            "in": [
                {"condition": {"attribute": "x", "operator": ">", "value": 20}, "action": "next_wf"},
                {"condition": None, "action": "R"}
            ],
            "next_wf": [
                {"condition": {"attribute": "x", "operator": "<", "value": 50}, "action": "A"},
                {"condition": None, "action": "R"}
            ]
        }
        result = hypercubes_for_action(workflows, "A")
        expected_hypercubes = [
            {
                "x": {"min": 21, "max": 49, "not": []},
                "m": {"min": 1, "max": 4000, "not": []},
                "a": {"min": 1, "max": 4000, "not": []},
                "s": {"min": 1, "max": 4000, "not": []}
            }
        ]
        self.assertEqual(result, expected_hypercubes)


class TestCalculateHypercubeVolume(unittest.TestCase):
    def test_volume_with_no_exclusions(self):
        hypercube = {
            "x": {"min": 1, "max": 10, "not": []},
            "m": {"min": 1, "max": 20, "not": []},
            "a": {"min": 1, "max": 30, "not": []},
            "s": {"min": 1, "max": 40, "not": []}
        }
        expected_volume = 10 * 20 * 30 * 40
        result = calculate_hypercube_volume(hypercube)
        self.assertEqual(result, expected_volume)

    def test_volume_with_some_exclusions(self):
        hypercube = {
            "x": {"min": 1, "max": 10, "not": [2, 3]},
            "m": {"min": 1, "max": 20, "not": [10]},
            "a": {"min": 1, "max": 30, "not": []},
            "s": {"min": 1, "max": 40, "not": [20, 25, 30]}
        }
        expected_volume = 8 * 19 * 30 * 37  # Adjusted for exclusions
        result = calculate_hypercube_volume(hypercube)
        self.assertEqual(result, expected_volume)

    def test_volume_with_exclusions_outside_range(self):
        hypercube = {
            "x": {"min": 1, "max": 10, "not": [15, 20]},  # Exclusions outside range
            "m": {"min": 5, "max": 20, "not": [1, 2, 3, 4]},  # Exclusions outside range
            "a": {"min": 10, "max": 30, "not": [31, 32, 33]},
            "s": {"min": 20, "max": 40, "not": [41, 42, 43]}
        }
        expected_volume = 10 * 16 * 21 * 21  # Exclusions outside range don't affect volume
        result = calculate_hypercube_volume(hypercube)
        self.assertEqual(result, expected_volume)


def calculate_hypercube_volume(hypercube):
    volume = 1
    for attribute in hypercube:
        min_val = hypercube[attribute]['min']
        max_val = hypercube[attribute]['max']
        excluded = hypercube[attribute]['not']

        # Calculate range excluding 'not' values
        range_size = max_val - min_val + 1 - sum(min_val <= ex <= max_val for ex in excluded)
        volume *= range_size

    return volume


class TestSolvePartTwo(unittest.TestCase):
    def test_solve_part_two(self):
        with open("test19.txt", "r") as file:
            workflows = WorkflowParser.parse_full_input(file.read())['workflows']
            result = solve_part_two(workflows)
            self.assertEqual(result, 167409079868000)

    def test_solve_part_two_real_data(self):
        with open("input19.txt", "r") as file:
            workflows = WorkflowParser.parse_full_input(file.read())['workflows']
            result = solve_part_two(workflows)
            self.assertEqual(result, 0)

def solve_part_two(workflows):
    hypercubes = hypercubes_for_action(workflows, "A")
    total_volume = sum(calculate_hypercube_volume(cube) for cube in hypercubes)
    return total_volume


def hypercubes_for_action(workflows, action):

    def get_hypercubes_for_workflow(workflow_name, remainder):
        if workflow_name not in workflows:
            return []

        hypercubes = []
        for rule in workflows[workflow_name]:
            # Create a hypercube for the current rule
            hypercube = {attr: {key: val for key, val in remainder[attr].items()} for attr in remainder}
            # ... Populate hypercube based on rule's condition ...

            if rule['condition']:
                attribute = rule['condition']['attribute']
                operator = rule['condition']['operator']
                value = rule['condition']['value']

                if operator == '>':
                    hypercube[attribute]['min'] = value + 1
                    remainder[attribute]['max'] = value
                elif operator == '<':
                    hypercube[attribute]['max'] = value - 1
                    remainder[attribute]['min'] = value
                elif operator == '=':
                    if value in hypercube[attribute]['not']:
                        hypercube = None
                    else:
                        hypercube[attribute]['min'] = hypercube[attribute]['max'] = value
                        hypercube[attribute]['not'] = []
                        # Add value to 'not' list for the remainder
                        remainder[attribute]['not'].append(value)

            # If the rule's action matches the target action, add the hypercube
            if rule['action'] == action and hypercube:
                hypercubes.append(hypercube)
            elif rule['action'] in workflows:  # If action is another workflow
                next_hypercubes = get_hypercubes_for_workflow(rule['action'], hypercube)
                for next_cube in next_hypercubes:
                    hypercubes.append(next_cube)

        return hypercubes

    initial_remainder = {
        "x": {"min": 1, "max": 4000, "not": []},
        "m": {"min": 1, "max": 4000, "not": []},
        "a": {"min": 1, "max": 4000, "not": []},
        "s": {"min": 1, "max": 4000, "not": []}
    }

    return get_hypercubes_for_workflow("in", initial_remainder)




if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
