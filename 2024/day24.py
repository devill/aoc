import os
from utils import data_files_for
import re

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


    def get_value(self, name):
        if name not in self.values:
            self.values[name] = self._calculate_value(name)
            # print(f"Calculated {name} = {self.values[name]}")
        return self.values[name]

    def get_all_values(self):
        return {name: self.get_value(name) for name in self.wires.keys()}

    def wires_names(self):
        return self.wires.keys()

    def expected_aliases(self):
        for i in range(0, 44):
            yield f"xor_{i:02}"
            yield f"and_{i:02}"
            yield f"cya_{i:02}"
            yield f"bit_{i:02}"
            yield f"cyo_{i:02}"


    def get_children_of(self, name):
        if name in self.alias_to_name:
            name = self.alias_to_name[name]
        return self.children[name]

    def get_parents_of(self, name):
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

    def get_terminal_names(self):
        return sorted([terminal for terminal in self.wires.keys() if terminal[0] == "z"])

    def get_x_inputs(self):
        return sorted([terminal for terminal in self.wires.keys() if terminal[0] == "x"])

    def get_y_inputs(self):
        return sorted([terminal for terminal in self.wires.keys() if terminal[0] == "y"])

    def input_ids(self):
        for input_terminal in self.get_x_inputs():
            yield int(input_terminal[1:])

    def set_inputs(self, x, y):
        self.values = {}
        i = 0
        while max(x,y) > 0:
            self.wires[f"x{i:02}"] = x & 1
            self.wires[f"y{i:02}"] = y & 1
            x >>= 1
            y >>= 1
            i += 1


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

    def aliased(self, name):
        return name in self.name_to_alias


    def parents_aliased(self, name):
        if self.wires[name] in [0, 1]:
            return False

        if name in self.name_to_alias:
            return False

        left, operator, right = self.wires[name]
        return left in self.name_to_alias and right in self.name_to_alias

    def report_unexpected_children(self, w, param, expected_children_aliases):
        operators = sorted([self.wires[c][1] for c in self.get_children_of(w)])
        if operators != param:
            alias = self.name_to_alias.get(w, w)
            print(f"Expected output operators {param} - {expected_children_aliases} for {alias}[{w}], got {operators}")
            print("- Inputs ")
            left, operator, right = self.wires[w]
            print(f"  {self.get_formula(left)} {operator} {self.get_formula(right)}")
            print("- Outputs ")
            for c in self.get_children_of(w):
                print(f"  {c} = {self.get_formula(c)}")
            print("")

    def report_erros(self):
        found = {}
        for alias in self.expected_aliases():
            if alias not in self.alias_to_name:
                print(f"Expected alias {alias} not found\n")
                continue
            w = self.alias_to_name[alias]
            found[w] = alias
            # if w in self.get_terminal_names():
                # alias = self.name_to_alias.get(w, w)
                # if alias != f"bit_{int(w[1:]):02}":
                #     print(f"Expected alias bit_{int(w[1:]):02} for {alias}[{w}]")
                #     print("- Inputs ")
                #     left, operator, right = self.wires[w]
                #     print(f"  {self.get_formula(left)} {operator} {self.get_formula(right)}")
                #     print("")

            type, id = alias.split("_")
            if type == 'xor':
                self.report_unexpected_children(w, ['AND', 'XOR'], f"bit_{id}, cya_{id}")
            if type == 'and':
                self.report_unexpected_children(w, ['OR'], f"cyo_{id}")
            if type == 'cya':
                self.report_unexpected_children(w, ['OR'], f"cyo_{id}")
            if type == 'cyo':
                self.report_unexpected_children(w, ['AND', 'XOR'], f"bit_{(int(id)+1):02}, cya_{(int(id)+1):02}")

        for w in self.wires_names():
            if w not in found and w not in self.get_terminal_names() and w not in self.get_x_inputs() and w not in self.get_y_inputs():
                print(f"Unexpected wire {w} = {self.get_formula(w)}")
                print("- Inputs ")
                left, operator, right = self.wires[w]
                print(f"  {self.get_formula(left)} {operator} {self.get_formula(right)}")
                print("- Outputs ")
                for c in self.get_children_of(w):
                    print(f"  {c} = {self.get_formula(c)}")
                print("")

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

class CircuitAnalyzer:
    def __init__(self, circuit):
        self.circuit = circuit
        self._generate_all_values()

    def _set_for(self, l, r):
        circuit.set_inputs(l, r)
        self.all_values[(l, r)] = self.circuit.get_all_values()

    def _generate_all_values(self):
        self.all_values = {}
        self.circuit.set_inputs(0, 0)

        for i in circuit.input_ids():
            self._set_for(1 << i, 1 << i)
            self._set_for(0, 1 << i)
            self._set_for(1 << i, 0)
            if i > 0:
                self._set_for(1 << (i-1), 3 << (i-1))
                self._set_for(3 << (i-1), 1 << (i-1))

        self._set_for(0, 0)

    def excited_by(self, i, w):
        return (self.all_values[(1 << i, 1 << i)][w] != 0 or
                self.all_values[(0, 1 << i)][w] != 0 or
                self.all_values[(1 << i, 0)][w] != 0)

    def is_output_bit(self, i, w):
        if not (self.all_values[(1 << i, 1 << i)][w] == 0 and
                self.all_values[(0, 1 << i)][w] == 1 and
                self.all_values[(1 << i, 0)][w] == 1 and
                self.all_values[(0, 0)][w] == 0):
            return False

        if i > 0:
            if not (self.all_values[(1 << (i-1), 1 << (i-1))][w] == 1 and
                    self.all_values[(0, 1 << (i-1))][w] == 0 and
                    self.all_values[(1 << (i-1), 0)][w] == 0):
                return False

        for j in circuit.input_ids():
            if j == i or j == i-1:
                continue
            if self.excited_by(j, w):
                return False
        return True

    def is_carry_bit(self, i, w):
        if not (self.all_values[(1 << i, 1 << i)][w] == 1 and
                self.all_values[(0, 1 << i)][w] == 0 and
                self.all_values[(1 << i, 0)][w] == 0 and
                self.all_values[(0, 0)][w] == 0):
            return False

        if i > 0:
            if not (self.all_values[(1 << (i-1), 3 << (i-1))][w] == 1 and
                    self.all_values[(1 << (i-1), 3 << (i-1))][w] == 0 and
                    self.all_values[(3 << (i-1), 1 << (i-1))][w] == 0):
                return False

        for j in circuit.input_ids():
            if j == i:
                continue
            if self.excited_by(j, w):
                return False
        return True

    def is_xor_bit(self, i, w):
        if not (self.all_values[(1 << i, 1 << i)][w] == 0 and
                self.all_values[(0, 1 << i)][w] == 1 and
                self.all_values[(1 << i, 0)][w] == 1 and
                self.all_values[(0, 0)][w] == 0):
            return False

        for j in circuit.input_ids():
            if j == i:
                continue
            if self.excited_by(j, w):
                return False
        return True

    def attempt_aliasing(self):
        for i in self.circuit.input_ids():
            for w in self.circuit.wires_names():
                if self.is_xor_bit(i, w):
                    self.circuit.set_alias(w, f"xor_{i:02}")
                if self.is_carry_bit(i, w):
                    self.circuit.set_alias(w, f"car_{i:02}")
                if self.is_output_bit(i, w):
                    self.circuit.set_alias(w, f"out_{i:02}")

        for w in self.circuit.get_x_inputs():
            self.circuit.set_alias(w, f"xin_{int(w[1:]):02}")
        for w in self.circuit.get_y_inputs():
            self.circuit.set_alias(w, f"yin_{int(w[1:]):02}")





if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):
        raw_data = file.read()

        circuit_parser = CircuitParser()
        circuit = circuit_parser.parse_data(raw_data)

        print("\n--- Part one ---")
        print(circuit.terminal_value())

        print("\n--- Part two ---")
        if not meta["type"] =='real':
            continue

        # circuit_analyzer = CircuitAnalyzer(circuit)
        # circuit_analyzer.attempt_aliasing()

        # for t in circuit.get_terminal_names():
        #     print(f"{t} = {circuit.get_formula(t)}")
            # out_i = (xin_i XOR yin_i) XOR car_{i-1}
            # car_i = (xin_i AND yin_i) OR (xin_i AND car_{i-1}) OR (yin_i AND car_{i-1})

        ids = {}
        for i in range(0, 44):
            children = circuit.get_children_of("x{:02}".format(i))
            if len(children) != 2:
                raise ValueError(f"Expected 2 children for x{i:02}, got {len(children)}")
            for c in children:
                formula = circuit.get_formula(c)
                if formula[1:4] != "x{:02}".format(i):
                    raise ValueError(f"Expected x{i:02} in formula {formula}")
                if formula[9:12] != "y{:02}".format(i):
                    raise ValueError(f"Expected y{i:02} in formula {formula}")
                if (circuit.wires[c][1] == "XOR"):
                    circuit.set_alias(c, f"xor_{i:02}")
                    ids[c] = i
                if (circuit.wires[c][1] == "AND"):
                    circuit.set_alias(c, f"and_{i:02}")
                    ids[c] = i
        #
        # for i in range(1, 44):
        #     children = circuit.get_children_of("xor_{:02}".format(i))
        #     for c in children:
        #         formula = circuit.get_formula(c)
        #         if formula[1:7] != "and_{:02}".format(i-1):
        #             continue
        #         if formula[17:23] != "xor_{:02}".format(i):
        #             continue
        #         if (circuit.wires[c][1] == "XOR"):
        #             circuit.set_alias(c, f"bit_{i:02}")
        #         if (circuit.wires[c][1] == "AND"):
        #             circuit.set_alias(c, f"cya_{i:02}")

        circuit.set_alias("z01", "bit_01")
        circuit.set_alias("kmj", "cya_01")
        for w in circuit.wires_names():
            wire = circuit.wires[w]
            if wire in [0, 1]:
                continue
            children_count  = len(circuit.get_children_of(w))
            operator = wire[1]
            id = ids.get(w, None)
            if id is None:
                p = circuit.get_parents_of(w)
                if p[0] in ids:
                    id = ids[p[0]]
                elif p[1] in ids:
                    id = ids[p[1]]
                else:
                    id = -1
            else:
                id = ids[w]
            if children_count == 1:
                if operator == "XOR":
                    circuit.set_alias(w, f"bit_{id:02}")
                if operator == "AND":
                    circuit.set_alias(w, f"cya_{id:02}")
            if operator == "OR":
                circuit.set_alias(w, f"cyo_{id:02}")


        circuit.report_erros()

        print(circuit.alias_to_name["xor_00"])


        # input_pattern = re.compile(r"([xy][0-9]{2})")
        # for w in circuit.wires_names():
        #     if not circuit.aliased(w) and not input_pattern.match(w):
        #         print(f"{w} = {circuit.get_formula(w)}")
        # for w in circuit.wires_names():
        #     if circuit.parents_aliased(w):
        #         print(f"{w} = {circuit.get_formula(w)}")


        # print(circuit_analyzer.is_carry_bit(1,"nfw"))

        # for w in circuit.get_terminal_names():
        #     print(f"{w} = {circuit.get_formula(w)}")

        # Identified errors:
        # (x14 AND y14) should be connected to cyo_14 but connected to dcv and z14
        # (x18 AND y18) should be connected to cyo_18 but connected to z18


        # mgk -