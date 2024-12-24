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
        self.wires = wires
        self.values = {}

    def get_value(self, name):
        if name not in self.values:
            self.values[name] = self._calculate_value(name)
            print(f"Calculated {name} = {self.values[name]}")
        return self.values[name]

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
    for file, _ in data_files_for(os.path.basename(__file__)):
        raw_data = file.read()

        circuit_parser = CircuitParser()
        circuit = circuit_parser.parse_data(raw_data)
        print(circuit.terminal_value())

        print("\n--- Part one ---")

        print("\n--- Part two ---")