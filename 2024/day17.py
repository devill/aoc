import os
from utils import data_files_for

def parse(raw_data):
    lines = raw_data.strip().split('\n')
    registers = [int(x.split(': ')[1]) for x in lines[:3]]
    program = [int(x) for x in lines[4].split(': ')[1].split(',')]
    return registers, program

class ChronospatialComputer:
    def __init__(self, registers):
        self.registers = registers
        self.instruction_pointer = 0
        self.output = []

    def get_combo_operand_value(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.registers[0]
        elif operand == 5:
            return self.registers[1]
        elif operand == 6:
            return self.registers[2]
        else:
            raise ValueError("Invalid combo operand")

    def adv(self, operand):
        denominator = 2 ** self.get_combo_operand_value(operand)
        self.registers[0] //= denominator

    def bxl(self, operand):
        self.registers[1] ^= operand

    def bst(self, operand):
        self.registers[1] = self.get_combo_operand_value(operand) % 8

    def jnz(self, operand):
        if self.registers[0] != 0:
            self.instruction_pointer = operand
            return True
        return False

    def bxc(self, operand):
        self.registers[1] ^= self.registers[2]

    def out(self, operand):
        self.output.append(self.get_combo_operand_value(operand) % 8)

    def bdv(self, operand):
        denominator = 2 ** self.get_combo_operand_value(operand)
        self.registers[1] = self.registers[0] // denominator

    def cdv(self, operand):
        denominator = 2 ** self.get_combo_operand_value(operand)
        self.registers[2] = self.registers[0] // denominator

    def run_program(self, program):
        while self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            operand = program[self.instruction_pointer + 1]
            opname = ["ADV", "BXL", "BST", "JNZ", "BXC", "OUT", "BDV", "CDV"]
            #print(f"{self.instruction_pointer}: {opname[opcode]} {operand} ({self.registers})")
            if opcode == 0:
                self.adv(operand)
            elif opcode == 1:
                self.bxl(operand)
            elif opcode == 2:
                self.bst(operand)
            elif opcode == 3:
                if self.jnz(operand):
                    continue
            elif opcode == 4:
                self.bxc(operand)
            elif opcode == 5:
                self.out(operand)
            elif opcode == 6:
                self.bdv(operand)
            elif opcode == 7:
                self.cdv(operand)
            else:
                raise ValueError("Invalid opcode")
            self.instruction_pointer += 2
        return ','.join(map(str, self.output))


def find_initial_value_for(program, expected_output, v):
    if len(expected_output) == 0:
        return v
    o = expected_output[-1]

    for i in range(8):
        computer = ChronospatialComputer([8*v + i, 0, 0])
        output = int(computer.run_program(program))
        if output == o:
            val = find_initial_value_for(program, expected_output[:-1], 8 * v + i)
            if val is not None:
                return val
    return None

if __name__ == "__main__":
    for file, _ in data_files_for(os.path.basename(__file__)):
        raw_data = file.read()

        registers, program = parse(raw_data)
        print("Registers:", registers)
        print("Program:", program)

        print("\n--- Part one ---")

        computer = ChronospatialComputer(registers)
        output = computer.run_program(program)
        print(output)

        print("\n--- Part two ---")


        program_without_jnz = program[:len(program)-2]

        init = find_initial_value_for(program_without_jnz, program, 0)

        print(f"Initial value: {init}")
        computer = ChronospatialComputer([init, 0, 0])
        output = computer.run_program(program)
        print(output)

        # 37186267430023 too low
        #2, 4, 1, 2, 7, 5, 4, 1, 1, 3, 5, 5, 0, 3, 3, 0
