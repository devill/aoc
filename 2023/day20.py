import unittest

class TestParser(unittest.TestCase):

    def test_parse_input(self):
        test_input = "\n".join([
            "broadcaster -> a",
            "%a -> inv, con",
            "&inv -> b",
            "%b -> con",
            "&con -> output"
        ])
        expected_output = {
            'broadcaster': {'type': 'broadcaster', 'destinations': ['a']},
            'a': {'type': 'flip-flop', 'destinations': ['inv', 'con']},
            'inv': {'type': 'conjunction', 'destinations': ['b']},
            'b': {'type': 'flip-flop', 'destinations': ['con']},
            'con': {'type': 'conjunction', 'destinations': ['output']}
        }
        self.assertEqual(parse_input(test_input), expected_output)

def parse_input(input_str):
    lines = input_str.strip('\n').split('\n')
    module_config = {}
    for line in lines:
        parts = line.split(' -> ')
        module_name_with_prefix = parts[0]
        destinations = parts[1].split(', ')

        # Remove type prefix from module name
        if module_name_with_prefix.startswith(('%', '&')):
            module_name = module_name_with_prefix[1:]
        else:
            module_name = module_name_with_prefix

        if module_name_with_prefix.startswith('%'):
            module_type = 'flip-flop'
        elif module_name_with_prefix.startswith('&'):
            module_type = 'conjunction'
        else:
            module_type = 'broadcaster'

        module_config[module_name] = {'type': module_type, 'destinations': destinations}
    return module_config

class TestPulsePropagation(unittest.TestCase):

    def test_initialize_modules(self):
        parsed_modules = {
            'broadcaster': {'type': 'broadcaster', 'destinations': ['a']},
            'a': {'type': 'flip-flop', 'destinations': ['inv', 'con']},
            'inv': {'type': 'conjunction', 'destinations': ['b']},
            'b': {'type': 'flip-flop', 'destinations': ['con']},
            'con': {'type': 'conjunction', 'destinations': ['output']}
        }
        expected_output = {
            'broadcaster': {'type': 'broadcaster', 'destinations': ['a']},
            'a': {'type': 'flip-flop', 'destinations': ['inv', 'con'], 'state': 'off'},
            'inv': {'type': 'conjunction', 'destinations': ['b'], 'last_inputs': {'a': 'low'}},
            'b': {'type': 'flip-flop', 'destinations': ['con'], 'state': 'off'},
            'con': {'type': 'conjunction', 'destinations': ['output'], 'last_inputs': {'a': 'low', 'b': 'low'}}
        }
        pulse_propagation = PulsePropagation(parsed_modules)
        self.assertEqual(pulse_propagation.modules, expected_output)

    def test_signal_handler_flip_flop_module(self):
        parsed_modules = {
            'a': {'type': 'flip-flop', 'destinations': ['inv', 'con'], 'state': 'off'},
            'inv': {'type': 'conjunction', 'destinations': ['b']},
            'con': {'type': 'conjunction', 'destinations': ['output']}
        }
        pulse_propagation = PulsePropagation(parsed_modules)
        expected_output_flip_flop = [('inv', 'high'), ('con', 'high')]
        self.assertEqual(pulse_propagation.handle_signal('broadcaster', 'a', 'low'), expected_output_flip_flop)

    def test_signal_handler_conjunction_module(self):
        parsed_modules = {
            'inv': {'type': 'conjunction', 'destinations': ['b'], 'last_inputs': {'a': 'low'}},
            'b': {'type': 'flip-flop', 'destinations': ['con'], 'state': 'off'}
        }
        pulse_propagation = PulsePropagation(parsed_modules)
        expected_output_conjunction = [('b', 'low')]
        self.assertEqual(pulse_propagation.handle_signal('a', 'inv', 'high'), expected_output_conjunction)

    def test_signal_handler_broadcaster_module(self):
        parsed_modules = {
            'broadcaster': {'type': 'broadcaster', 'destinations': ['a', 'b']}
        }
        pulse_propagation = PulsePropagation(parsed_modules)
        expected_output_broadcaster = [('a', 'high'), ('b', 'high')]
        self.assertEqual(pulse_propagation.handle_signal('source', 'broadcaster', 'high'), expected_output_broadcaster)

    def test_press_button(self):
        parsed_modules = {
            'broadcaster': {'type': 'broadcaster', 'destinations': ['a']},
            'a': {'type': 'flip-flop', 'destinations': ['inv', 'con'], 'state': 'off'},
            'inv': {'type': 'conjunction', 'destinations': ['b'], 'last_inputs': {'a': 'low'}},
            'b': {'type': 'flip-flop', 'destinations': ['con'], 'state': 'off'},
            'con': {'type': 'conjunction', 'destinations': ['output'], 'last_inputs': {'a': 'low', 'b': 'low'}}
        }
        pulse_propagation = PulsePropagation(parsed_modules)
        low_signals, high_signals = pulse_propagation.press_button()
        self.assertEqual((low_signals, high_signals), (4, 4))  # Example counts

    @unittest.skip('Not needed anymore')
    def test_dependencies(self):
        parsed_modules = {
            'broadcaster': {'type': 'broadcaster', 'destinations': ['a']},
            'a': {'type': 'flip-flop', 'destinations': ['inv', 'con'], 'state': 'off'},
            'inv': {'type': 'conjunction', 'destinations': ['b'], 'last_inputs': {'a': 'low'}},
            'b': {'type': 'flip-flop', 'destinations': ['con'], 'state': 'off'},
            'con': {'type': 'conjunction', 'destinations': ['output'], 'last_inputs': {'a': 'low', 'b': 'low'}}
        }
        pulse_propagation = PulsePropagation(parsed_modules)
        result = pulse_propagation.dependencies()
        print(result)

    @unittest.skip('Not needed anymore')
    def test_dependencies_real_data(self):
        with open("input20.txt", "r") as file:
            content = file.read()
        parsed_modules = parse_input(content)
        pulse_propagation = PulsePropagation(parsed_modules)
        result = pulse_propagation.dependencies()
        print(result)


class PulsePropagation:

    def __init__(self, parsed_modules):
        self.modules = parsed_modules
        self.initialize_modules()
        self.listeners = []

    def initialize_modules(self):
        for name, module in self.modules.items():
            if module['type'] == 'flip-flop':
                module['state'] = 'off'
            elif module['type'] == 'conjunction':
                module['last_inputs'] = {}
        for name, module in self.modules.items():
            for destination in module.get('destinations', []):
                if destination in self.modules and self.modules[destination]['type'] == 'conjunction':
                    self.modules[destination]['last_inputs'][name] = 'low'

    def handle_signal(self, sender_name, destination_name, signal):
        module = self.modules[destination_name]
        output_signal = None
        if module['type'] == 'flip-flop':
            if signal == 'low':
                module['state'] = 'on' if module['state'] == 'off' else 'off'
                output_signal = 'high' if module['state'] == 'on' else 'low'
        elif module['type'] == 'conjunction':
            module['last_inputs'][sender_name] = signal
            if all(status == 'high' for status in module['last_inputs'].values()):
                output_signal = 'low'
            else:
                output_signal = 'high'
        elif module['type'] == 'broadcaster':
            output_signal = signal

        if output_signal:
            return [(dest, output_signal) for dest in module['destinations']]
        return []

    def press_button(self):
        # Initialize counters for low and high signals
        low_signals, high_signals = 0, 0
        queue = [('button', 'broadcaster', 'low')]

        while queue:
            sender, destination, signal = queue.pop(0)

            for callback in self.listeners:
                callback(sender, destination, signal, 'before')

            if signal == 'low':
                low_signals += 1
            else:
                high_signals += 1

            if destination in self.modules:
                new_signals = self.handle_signal(sender, destination, signal)
                for dest, sig in new_signals:
                    queue.append((destination, dest, sig))

            for callback in self.listeners:
                callback(sender, destination, signal, 'after')


        return low_signals, high_signals

    def on(self, callback):
        self.listeners.append(callback)

    def dependencies(self):
        dependencies = { name: set() for name in self.modules.keys()}
        for name, module in self.modules.items():
            for destination in module['destinations']:
                if destination not in self.modules.keys():
                    dependencies[destination] = set()
                dependencies[destination].add(name)

        total_dependencies = 0
        while True:
            for name, module in self.modules.items():
                for destination in module['destinations']:
                    dependencies[destination].update(dependencies[name])

            dep_counts = [len(s) for name, s in dependencies.items()]
            total_dep_counts = sum(dep_counts)
            print(total_dep_counts)
            if total_dep_counts == total_dependencies:
                if 'rx' in dependencies:
                    print(dependencies['rx'])
                print(dep_counts)
                break
            total_dependencies = total_dep_counts

        print(dependencies)

class TestSolvePartOne(unittest.TestCase):
    def test_solve_part_one(self):
        with open("test20.txt", "r") as file:
            content = file.read()
        result = solve_part_one(content)
        self.assertEqual(result, 11687500)

    def test_solve_part_one_real_data(self):
        with open("input20.txt", "r") as file:
            content = file.read()
        result = solve_part_one(content)
        self.assertEqual(result, 1020211150)

def solve_part_one(content):
    parsed_data = parse_input(content)
    lows, highs = 0, 0
    pp = PulsePropagation(parsed_data)
    for _ in range(1000):
        low, high = pp.press_button()
        lows += low
        highs += high
    return lows * highs



class TestSolvePartTwo(unittest.TestCase):
    # @unittest.skip('Need a different solution')
    def test_solve_part_one_real_data(self):
        with open("input20.txt", "r") as file:
            content = file.read()
        number_of_presses_required = solve_part_two(content)
        print(f"Solution for part two: {number_of_presses_required}")
        # self.assertEqual(number_of_presses_required, None)

def solve_part_two(content):
    parsed_data = parse_input(content)
    pp = PulsePropagation(parsed_data)
    on_states = {}

    count = 0
    def handler(c_sender, c_receiver, c_signal, phase):
        nonlocal count
        nonlocal on_states
        if c_receiver == 'nc' and phase == 'before':
            #if pp.modules['nc']['last_inputs'][c_sender] != c_signal:
            if "high" == c_signal:
                if c_sender not in on_states:
                    on_states[c_sender] = []
                on_states[c_sender].append(count)
                print(count, c_sender, c_signal)


    print("")
    print("")

    pp.on(lambda c_sender, c_receiver, c_signal, phase: handler(c_sender, c_receiver, c_signal, phase))
    for i in range(20000):
        count += 1
        pp.press_button()
        # print(pp.modules['nc']['last_inputs'])

    print("")
    print(on_states)
    print([v[1] - v[0] for k, v in on_states.items()])
    print("")
    print("")

if __name__ == '__main__':
    unittest.main()
