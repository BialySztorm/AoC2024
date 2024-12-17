from kivy.uix.label import Label

from utils import data_manager as dm


class ThreeBitComputer:
    def __init__(self, register_a, register_b, register_c, program):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.program = program
        self.pointer = 0
        self.output = []
        self.test_failed = False

    def run_program(self, test=False):
        while self.pointer < len(self.program):
            instruction_index = self.program[self.pointer]
            instruction_list = [self._adv, self._bxl, self._bst, self._jnz, self._bxc, self._out, self._bdv, self._cdv]
            instruction_list[instruction_index]()
            self.pointer += 2

        return self.output

    def _get_combo_operand(self, operand):
        if operand < 4:
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c
        if operand == 7:
            throw_error("Invalid operand")

    # Division register a with the power of the two to combo operand
    def _adv(self):
        numerator = self.register_a
        denominator = 2 ** self._get_combo_operand(self.program[self.pointer + 1])
        self.register_a = numerator // denominator

    # Bitwise XOR register b and literal operand
    def _bxl(self):
        self.register_b = self.register_b ^ self.program[self.pointer + 1]

    #  Combo operand modulo 8
    def _bst(self):
        self.register_b = self._get_combo_operand(self.program[self.pointer + 1]) % 8

    # Jump to the literal operand instruction if register a is not zero
    def _jnz(self):
        if self.register_a != 0:
            self.pointer = self.program[self.pointer + 1] - 2

    # Bitwise XOR register b and register c
    def _bxc(self):
        self.register_b = self.register_b ^ self.register_c

    # Outputs combo operand modulo 8
    def _out(self):
        output = self._get_combo_operand(self.program[self.pointer + 1]) % 8
        self.output.append(str(output))

    # Division register a with the power of the two to combo operand
    def _bdv(self):
        numerator = self.register_a
        denominator = 2 ** self._get_combo_operand(self.program[self.pointer + 1])
        self.register_b = numerator // denominator

    # Division register a with the power of the two to combo operand
    def _cdv(self):
        numerator = self.register_a
        denominator = 2 ** self._get_combo_operand(self.program[self.pointer + 1])
        self.register_c = numerator // denominator


def find_initial_register_a(register_b, register_c, program):
    register_a = sum(7 * 8 ** i for i in range(len(program) - 1)) + 1
    target_output = [str(cell) for cell in program]

    while True:
        computer = ThreeBitComputer(register_a, register_b, register_c, program)
        output = computer.run_program()

        if output == target_output:
            return register_a

        for i in range(len(output) - 1, -1, -1):
            if output[i] != str(program[i]):
                add = 8 ** i
                register_a += add
                break


def handle_day(layout, sample=False):
    data = dm.read_data(17, sample)
    answer = ""
    register_a = int(data[0][2])
    register_b = int(data[1][2])
    register_c = int(data[2][2])
    program = [int(cell) for cell in data[4][1].split(',')]

    # * Part one
    computer = ThreeBitComputer(register_a, register_b, register_c, program)
    output = computer.run_program()
    answer += f"Part one: {",".join(output)}\n"
    print([str(cell) for cell in program])
    print(output)

    # * Part two
    initial_a = find_initial_register_a(register_b, register_c, program)
    answer += f"Part two: {initial_a}\n"

    dm.write_data(17, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
