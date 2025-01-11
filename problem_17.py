from helpers import load_text
import re

EXAMPLE_FILE = "problem_17_example.txt"
DATA_FILE = "problem_17_data.txt"


def execute(registers: list[int], program: list[int], debug=False):
    ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = list(range(8))

    literal_opcode = [BXL, JNZ]

    output = []
    iptr = 0

    while True:
        if debug:
            print(f"{iptr=}, {registers=}, {output=}")
            input()

        if iptr >= len(program):
            if debug:
                print("HALT")
            break

        opcode = program[iptr]
        operand = program[iptr + 1]
        suppress_ptr_inc = False

        is_literal_operand = opcode in literal_opcode

        if is_literal_operand:
            operand_value = operand
        else:  # combo operand
            match operand:
                case 0 | 1 | 2 | 3:
                    operand_value = operand
                case 4:
                    operand_value = registers[0]
                case 5:
                    operand_value = registers[1]
                case 6:
                    operand_value = registers[2]
                case _:
                    assert False, "Invalid operand"

        match opcode:
            case 0:  # ADV, division
                registers[0] = int(registers[0] / 2**operand_value)
            case 1:  # BXL
                registers[1] ^= operand_value
            case 2:  # BST
                registers[1] = operand_value % 8
            case 3:  # JNZ
                if registers[0] != 0:
                    iptr = operand_value
                    suppress_ptr_inc = True
            case 4:  # BXC
                registers[1] = registers[1] ^ registers[2]
                # reads but ignores operand
            case 5:  # OUT
                output.append(operand_value % 8)
            case 6:  # BDV
                registers[1] = int(registers[0] / 2**operand_value)
            case 7:  # CDV
                registers[2] = int(registers[0] / 2**operand_value)
            case _:
                assert False

        if not suppress_ptr_inc:
            iptr += 2
            suppress_ptr_inc = False

    return ",".join(map(str, output)), ",".join(map(str, registers))


def load_program(file_path) -> tuple[list[int], list[int]]:
    lines = [l.strip() for l in load_text(file_path)]
    registers = [int(l.split(":")[-1].strip()) for l in lines[:3]]
    program = [int(v.strip()) for v in lines[4].split(":")[1].split(",")]
    return registers, program


def main():
    # test 1
    assert execute([0, 0, 9], [2, 6])[1] == "0,1,9"

    # test 2
    assert execute([10, 0, 0], [5, 0, 5, 1, 5, 4])[0] == "0,1,2"

    # test 3
    res = execute([2024, 0, 0], [0, 1, 5, 4, 3, 0])
    assert res[0] == "4,2,5,6,7,7,7,7,3,1,0"
    assert res[1].split(",")[0] == "0"

    # test 4
    assert execute([0, 29, 0], [1, 7])[1].split(",")[1] == "26"

    # test 5
    assert execute([0, 2024, 43690], [4, 0])[1].split(",")[1] == "44354"

    # test example
    assert execute(*load_program(EXAMPLE_FILE))[0] == "4,6,3,5,6,3,5,2,1,0"

    # problem
    prog, reg = load_program(DATA_FILE)
    output, _ = execute(prog, reg)

    print(f"{output=}")  # Answer: 1,5,7,4,1,6,0,3,0


main()
