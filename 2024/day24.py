import os
from utils import data_files_for

class CircuitBuilder:
    def __init__(self):
        self.wires = {}

    def add_gate(self, left, operator, right, output):
        self.wires[output] = (left, operator, right)

    def add_input_value(self, name, value):
        self.wires[name] = value

    def get_circuit(self):
        return Circuit(self.wires)

class Circuit:
    def __init__(self, wires):
        self.formulas = {}
        self.wires = wires
        self.children = self._generate_children()
        self.values = {}
        self.name_to_alias = {}
        self.alias_to_name = {}
        self.input_length = self.find_input_length()
        self.output_length = self.find_output_length()

    def _generate_children(self):
        children = {name: [] for name in self.wires.keys()}
        for name, value in self.wires.items():
            if value in [0, 1]:
                continue
            left, operator, right = value
            children[left].append(name)
            children[right].append(name)
        return children

    def set_alias(self, name, alias):
        self.formulas = {}
        if alias in self.alias_to_name:
            print(f"Alias {alias} already in use by {self.alias_to_name[alias]}")

        self.name_to_alias[name] = alias
        self.alias_to_name[alias] = name

    def display_name(self, name):
        if name in self.name_to_alias:
            return f"{self.name_to_alias[name]}[{name}]"
        return name

    def get_value(self, name):
        if name not in self.values:
            self.values[name] = self._calculate_value(name)
        return self.values[name]

    def get_all_values(self):
        return {name: self.get_value(name) for name in self.wires.keys()}

    def wires_names(self):
        return self.wires.keys()

    def expected_aliases(self):
        for i in range(2,self.input_length):
            yield f"and_{i:02}"
            yield f"xor_{i:02}"
            yield f"carry_{i:02}"
            yield f"carryand_{i:02}"
            yield f"bit_{i:02}"

    def get_outputs(self, name):
        if name in self.alias_to_name:
            name = self.alias_to_name[name]
        return self.children[name]

    def get_inputs(self, name):
        if name in self.alias_to_name:
            name = self.alias_to_name[name]
        return [self.wires[name][0], self.wires[name][2]]

    def _calculate_value(self, name):
        if self.wires[name] in [0, 1]:
            return int(self.wires[name])

        left, operator, right = self.wires[name]
        if operator == "AND":
            return self.get_value(left) & self.get_value(right)
        if operator == "OR":
            return self.get_value(left) | self.get_value(right)
        if operator == "XOR":
            return self.get_value(left) ^ self.get_value(right)

        raise ValueError(f"Unknown node: {operator}")

    def terminal_value(self):
        terminals = sorted([terminal for terminal in self.wires.keys() if terminal[0] == "z"])
        values = reversed([self.get_value(terminal) for terminal in terminals])
        binary_value = ''.join([str(value) for value in values])
        return int(binary_value, 2)

    def reset(self):
        self.wires = {}

    def __str__(self):
        return str(self.wires)

    def __repr__(self):
        return str(self)


    def get_formula(self, name):
        if name not in self.formulas:
            self.formulas[name] = self._calculate_formula(name)
        return self.formulas[name]

    def _calculate_formula(self, name):
        if self.wires[name] in [0, 1]:
            return name

        return self._wire_to_subformula(name)

    def _wire_to_subformula(self, name):
        if name in self.name_to_alias:
            return f"{self.name_to_alias[name]}[{name}]"

        left, operator, right = self.wires[name]
        if left > right:
            left, right = right, left
        if operator == "AND":
            return f"({self.get_formula(left)} AND {self.get_formula(right)})[{name}]"
        if operator == "OR":
            return f"({self.get_formula(left)} OR {self.get_formula(right)})[{name}]"
        if operator == "XOR":
            return f"({self.get_formula(left)} XOR {self.get_formula(right)})[{name}]"

        raise ValueError(f"Unknown node: {operator}")

    def is_aliased(self, name):
        return name in self.name_to_alias

    def find_input_length(self):
        return len([name for name in self.wires.keys() if name[0] == "x"])

    def find_output_length(self):
        return len([name for name in self.wires.keys() if name[0] == "z"])


class CircuitParser:
    def _parse_input_value(self, raw_input_value):
        name, value = raw_input_value.split(": ")
        return name, int(value)

    def _parse_gate(self, raw_gate):
        left, operator, right, _, output = raw_gate.split(" ")
        return left, operator, right, output

    def parse_data(self, raw_data):
        raw_input_values, raw_gates = raw_data.split("\n\n")
        input_values = [ self._parse_input_value(raw_input_value) for raw_input_value in raw_input_values.strip().split("\n")]
        gates = [ self._parse_gate(raw_gate) for raw_gate in raw_gates.strip().split("\n")]

        circuit_builder = CircuitBuilder()
        for name, value in input_values:
            circuit_builder.add_input_value(name, value)
        for left, operator, right, output in gates:
            circuit_builder.add_gate(left, operator, right, output)

        circuit = circuit_builder.get_circuit()
        return circuit



if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):
        raw_data = file.read()

        circuit_parser = CircuitParser()
        circuit = circuit_parser.parse_data(raw_data)

        print("\n--- Part one ---")
        print(circuit.terminal_value())

        print("\n--- Part two ---")
        if meta['type'] != 'real':
            continue

        and_operators = []
        xor_operators = []
        for i in range(circuit.input_length):
            wire = circuit.wires[f"x{i:02}"]
            if not wire in [0, 1]:
                print(f"x{i:02} should be initial input")
                continue
            if sorted([circuit.wires[o][1] for o in circuit.get_outputs(f"x{i:02}")]) != ["AND", "XOR"]:
                print(f"x{i:02} should have AND and XOR operators")
                continue
            for output in circuit.get_outputs(f"x{i:02}"):
                _, operator, _ = circuit.wires[output]
                if operator == "AND":
                    circuit.set_alias(output, f"and_{i:02}")
                    and_operators.append(output)
                if operator == "XOR":
                    circuit.set_alias(output, f"xor_{i:02}")
                    xor_operators.append(output)


        for i in range(circuit.output_length):
            wire = circuit.wires[f"z{i:02}"]
            if wire in [0, 1]:
                continue
            left, operator, right = wire
            if operator != "XOR":
                continue
            circuit.set_alias(f"z{i:02}", f"bit_{i:02}")

        # Note that the first carry is simply the first AND operator
        current_carry = and_operators[0]
        i = 0
        while True:
            i += 1
            carry_outputs = circuit.get_outputs(current_carry)

            if len(carry_outputs) != 2:
                break

            # Take the other child of carry
            carry_and = [child for child in carry_outputs if child != f"z{i:02}"][0]
            circuit.set_alias(carry_and, f"carryand_{i:02}")
            carry_and_inputs = circuit.get_inputs(carry_and)

            carry_and_outputs = circuit.get_outputs(carry_and)
            if len(carry_and_outputs) != 1:
                break

            current_carry = carry_and_outputs[0]
            circuit.set_alias(current_carry, f"carry_{i:02}")

        for i in range(circuit.input_length):
            circuit.set_alias(f"x{i:02}", f"xin_{i:02}")
            circuit.set_alias(f"y{i:02}", f"yin_{i:02}")

        print(" ")
        current_carry = and_operators[0]
        i = 0
        while True:
            i += 1
            if i >= circuit.input_length:
                break
            carry_outputs = circuit.get_outputs(current_carry)

            if len(carry_outputs) != 2:
                left, operator, right = circuit.wires[current_carry]
                print(f"Carry should have two outputs:  {circuit.display_name(current_carry)}  -> {list(map(circuit.display_name, carry_outputs))}")
                break

            if f"z{i:02}" not in carry_outputs:
                print(f"Carry should have z{i:02} as output: {circuit.display_name(current_carry)} -> {list(map(circuit.display_name, carry_outputs))}")
                #break

            # Take the other child of carry
            carry_and = [child for child in carry_outputs if child != f"z{i:02}"][0]
            carry_and_inputs = circuit.get_inputs(carry_and)
            if len(carry_and_inputs) != 2:
                left, operator, right = circuit.wires[carry_and]
                print(f"Carry_and should have two inputs: {circuit.display_name(carry_and)} = {circuit.display_name(left)} {operator} {circuit.display_name(right)}")
                #break

            carry_and_outputs = circuit.get_outputs(carry_and)
            if len(carry_and_outputs) != 1:
                print(f"Carry_and should have one output: {circuit.display_name(carry_and)} -> {list(map(circuit.display_name, carry_and_outputs))}")
                break

            current_carry = carry_and_outputs[0]

        print("")
        for i in range(circuit.output_length):
            wire = circuit.wires[f"z{i:02}"]
            if wire in [0, 1]:
                print(f"z{i:02} should have inputs")
            left, operator, right = wire
            if operator != "XOR":
                print(f"z{i:02} should have XOR operator")
                print(f"Instead it is {circuit.display_name(left)} {operator} {circuit.display_name(right)}")

        print("")
        for alias in circuit.expected_aliases():
            if alias not in circuit.alias_to_name:
                print(f"Missing alias: {alias}")

            inputs = circuit.get_inputs(circuit.alias_to_name[alias])
            type, id = alias.split("_")
            input_alises = sorted([circuit.name_to_alias[input] for input in inputs])
            if type == "and":
                if input_alises != [f"xin_{id}", f"yin_{id}"]:
                    print(f"{alias}: {circuit.display_name(inputs[0])} {circuit.display_name(inputs[1])} (expected: {f'xin_{id} yin_{id}'})")
            elif type == "xor":
                if input_alises != [f"xin_{id}", f"yin_{id}"]:
                    print(f"{alias}: {circuit.display_name(inputs[0])} {circuit.display_name(inputs[1])} (expected: {f'xin_{id} yin_{id}'})")
            elif type == "carryand":
                if input_alises != [f"carry_{(int(id)-1):02}", f"xor_{id}"]:
                    print(f"{alias}: {circuit.display_name(inputs[0])} {circuit.display_name(inputs[1])} (expected: {f'xor_{id} carry_{(int(id)-1):02}'})")
            elif type == "carry":
                if input_alises != [f"and_{id}", f"carryand_{id}"]:
                    print(f"{alias}: {circuit.display_name(inputs[0])} {circuit.display_name(inputs[1])} (expected: {f'and_{id} carryand_{id}'})")
            elif type == "bit":
                if input_alises != [f"carry_{(int(id)-1):02}", f"xor_{id}"]:
                    print(f"{alias}: {circuit.display_name(inputs[0])} {circuit.display_name(inputs[1])} (expected: {f'xor_{id} carry_{(int(id)-1):02}'})")
            else:
                print(f"{alias}: {circuit.display_name(inputs[0])} {circuit.display_name(inputs[1])} (expected: {f'xin_{id} yin_{id}'}")

        print("")
        for alias in circuit.expected_aliases():
            if alias not in circuit.alias_to_name:
                print(f"Missing alias: {alias}")

            display_name = circuit.display_name(circuit.alias_to_name[alias])
            outputs = circuit.get_outputs(circuit.alias_to_name[alias])
            output_display_names = [circuit.display_name(output) for output in outputs]
            type, id = alias.split("_")
            output_alises = sorted([circuit.name_to_alias[output] for output in outputs])
            if type == "and":
                if output_alises != [f"carry_{id}"]:
                    print(f"{display_name}: {output_display_names} (expected: {f'carry_{id}'})")
            elif type == "xor":
                if output_alises != [f"bit_{id}",f"carryand_{id}"]:
                    print(f"{display_name}: {output_display_names} (expected: {f'bit_{id} carryand_{id}'})")
            elif type == "carryand":
                if output_alises != [f"carry_{id}"]:
                    print(f"{display_name}: {output_display_names} (expected: {f'carry_{id}'})")
            elif type == "carry":
                if output_alises != [f"bit_{(int(id)+1):02}", f"carryand_{(int(id)+1):02}"]:
                    print(f"{display_name}: {output_display_names} (expected: {f'bit_{(int(i)+1):02} carryand_{(int(i)+1):02}'})")


    print(','.join(sorted(['mvb', 'z08', 'z23', 'bmn', 'z18', 'wss', 'rds', 'jss'])))