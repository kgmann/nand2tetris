"""
This needs to be cleaned, I submitted and it's working so I'll just keep it and move on for now.
"""

import os
import sys
import uuid
from enum import Enum
from typing import Tuple, List


class CommandTypes(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


class Parser:
    """
    Parses a single '.vm' file, processes the VM commands, and provides convenient access to their components.
    """

    def __init__(self, vm_file_path: str) -> None:
        self.vm_file_path = vm_file_path
        self.vm_file_content, self.current_command_index, self.current_command = (
            [],
            -1,
            "",
        )

        # NOTE: I should ideally open the file and read one line at a time for memory efficiency, but this is just fine for now
        with open(vm_file_path, "r") as f:
            self.vm_file_content = [
                line.strip()
                for line in f.readlines()
                if (line.strip() != "" and not line.strip().startswith("//"))
            ]  # ignore comments

    def has_more_commands(self) -> bool:
        return self.current_command_index < (len(self.vm_file_content) - 1)

    def advance(self) -> None:
        """
        Moves to the next command in the vm file. Raises a runtime error if there's no next command.
        """
        if self.has_more_commands():
            self.current_command_index += 1
            self.current_command = self.vm_file_content[self.current_command_index]
        else:
            raise RuntimeError("No more commands are available")

    def get_current_command_data(self) -> Tuple[CommandTypes, str, str]:
        """
        Returns a tuple (command type, first arg, second arg).
        Second arg can be none if there's none, and for arithmetic and logical commands, first arg is the command.
        """
        command_parts = self.current_command.split()
        if command_parts[0] == "push":
            return (CommandTypes.C_PUSH, command_parts[1], command_parts[2])
        elif command_parts[0] == "pop":
            return (CommandTypes.C_POP, command_parts[1], command_parts[2])
        elif command_parts[0] in [
            "add",
            "sub",
            "neg",
            "eq",
            "gt",
            "lt",
            "and",
            "or",
            "not",
        ]:
            return (CommandTypes.C_ARITHMETIC, command_parts[0], None)
        else:
            raise NotImplementedError


class CodeWriter:
    def __init__(self, output_file_path: str, parser: Parser) -> None:
        self.output_file_path = output_file_path
        self.parser = parser

        # Temporary labels
        self.temp_unique_labels = set()  # unique temporary labels used in hack assembly
        self.temp_vars = (
            set()
        )  # I need a temp variables for some commands like 'pop segment k' and I just want to keep track of them

        # Init memory segments' special pointers
        self.SP, self.LCL, self.ARG, self.THIS, self.THAT = (
            "SP",
            "LCL",
            "ARG",
            "THIS",
            "THAT",
        )
        self.TEMP = 5  # fixed base address of the temp segment

        # Create a new file or empty content if file exists
        with open(self.output_file_path, "w") as f:
            f.write("")

    def translate(self):
        """
        Translate the VM code in the input file to Hack assembly code and save it to the output file
        """
        while self.parser.has_more_commands():
            self.parser.advance()

            cmd = self.parser.current_command
            cmd_type, arg1, arg2 = self.parser.get_current_command_data()

            hack_asm_code = []
            if cmd_type == CommandTypes.C_ARITHMETIC:
                hack_asm_code = self.translate_arithmetic(arg1)
            elif cmd_type in [CommandTypes.C_PUSH, CommandTypes.C_POP]:
                hack_asm_code = self.translate_push_pop(cmd_type, arg1, arg2)
            else:
                raise ValueError("Invalid command type")

            self.write_lines([f"//{cmd}", *hack_asm_code])

    def translate_arithmetic(self, command: str) -> List:
        """
        Translates an arithmetic and logical VM command code to a list of Hack assembly code.
        """

        def vm_to_hack_binary_arithmetic(op: str) -> List:
            return [
                # *(SP-2)= *(SP-1) op *(SP-2)
                f"@{self.SP}",
                # f"A=M",
                f"A=M-1",
                f"D=M",
                f"A=A-1",
                f"D=M{op}D",
                f"M=D",
                # SP = SP-1
                f"@{self.SP}",
                f"M=M-1",
            ]

        def vm_to_hack_binary_conditional(op: str, jump_condition: str) -> List:
            while True:  # feels like an overkill but it's aight
                if (
                    f"TEMP_{str(uuid.uuid4()).upper().replace('-', '_')}"
                    not in self.temp_unique_labels
                ):
                    temp_label_jump = (
                        f"TEMP_{str(uuid.uuid4()).upper().replace('-', '_')}"
                    )
                    self.temp_unique_labels.add(temp_label_jump)
                    break
            temp_label_end = f"{temp_label_jump}_END"

            return [
                # D = *(SP-2) op *(SP-1) [x op y]
                f"@{self.SP}",
                # f"A=M",
                f"A=M-1",
                f"D=M",
                f"A=A-1",
                f"D=M{op}D",
                # SP = SP-1
                f"@{self.SP}",
                f"M=M-1",
                # if else jump
                f"@{temp_label_jump}",
                f"D;{jump_condition}",
                f"@{self.SP}",
                f"A=M-1",
                # f"A=A-1",
                f"M=0",
                f"@{temp_label_end}",
                f"0;JEQ",
                f"({temp_label_jump})",
                f"@{self.SP}",
                f"A=M-1",
                # f"A=A-1",
                f"M=-1",
                f"({temp_label_end})",
                # # SP = SP-1
                # f"@{self.SP}",
                # f"M=M-1"
            ]

        def vm_to_hack_unary_ops(op: str):
            return [
                # D = op (SP-1)
                f"@{self.SP}",
                # f"A=M",
                f"A=M-1",
                f"M={op}M",
            ]

        cmd_op_map_arithmetic = {"add": "+", "sub": "-", "and": "&", "or": "|"}
        cmd_op_map_condional_jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
        cmd_op_map_unary = {"neg": "-", "not": "!"}

        if command in ("add", "sub", "and", "or"):
            asm_code = vm_to_hack_binary_arithmetic(cmd_op_map_arithmetic[command])
        elif command in ["eq", "gt", "lt"]:
            asm_code = vm_to_hack_binary_conditional(
                "-", cmd_op_map_condional_jump[command]
            )
        elif command in ["neg", "not"]:
            asm_code = vm_to_hack_unary_ops(cmd_op_map_unary[command])
        else:
            raise ValueError(f"Command '{command}' not recognized")

        return asm_code

    def translate_push_pop(self, cmd_type: str, segment: str, value: str) -> List:
        """
        Translates a VM command code to a list of Hack assembly code.
        """

        def translate_regular_push(mem_segment_ptr: str, value: str) -> List:
            return [
                # D = *(*mem_segment_ptr + value)
                f"@{mem_segment_ptr}",
                f"D=M",
                f"@{value}",
                f"A=D+A",
                f"D=M",
                # *SP = D, *SP = *SP + 1
                f"@{self.SP}",
                f"M=M+1",
                f"A=M-1",
                f"M=D",
            ]

        def translate_regular_pop(mem_segment_ptr: str, value: str) -> List:
            self.temp_vars.add("temp_var_0")
            return [
                # temp_var_0 = (*mem_segment_ptr + value)
                f"@{mem_segment_ptr}",
                f"D=M",
                f"@{value}",
                f"D=D+A",
                f"@temp_var_0",
                f"M=D",
                # *SP = *SP-1, *temp_var_0 = *SP
                f"@{self.SP}",
                f"M=M-1",
                f"A=M",
                f"D=M",
                f"@temp_var_0",
                f"A=M",
                f"M=D",
            ]

        mem_segment_base_map = {
            "local": self.LCL,
            "argument": self.ARG,
            "this": self.THIS,
            "that": self.THAT,
        }

        if cmd_type == CommandTypes.C_PUSH:
            if segment == "constant":
                asm_code = [
                    f"@{value}",
                    f"D=A",
                    f"@{self.SP}",
                    f"M=M+1",
                    f"A=M-1",
                    f"M=D",
                ]
            elif segment in ["local", "argument", "this", "that"]:
                asm_code = translate_regular_push(mem_segment_base_map[segment], value)
            elif segment == "pointer":
                pointer_value_map = {"0": self.THIS, "1": self.THAT}
                asm_code = [
                    f"@{pointer_value_map[value]}",
                    f"D=M",
                    f"@{self.SP}",
                    f"M=M+1",
                    f"A=M-1",
                    f"M=D",
                ]
            elif segment == "temp":
                asm_code = [
                    # D = *(mem_segment_base + value)
                    f"@{self.TEMP}",
                    f"D=A",
                    f"@{value}",
                    f"A=D+A",
                    f"D=M",
                    # *SP = D, *SP = *SP + 1
                    f"@{self.SP}",
                    f"M=M+1",
                    f"A=M-1",
                    f"M=D",
                ]
            elif segment == "static":
                file_basename = "".join(
                    os.path.basename(self.output_file_path).split(".")[:-1]
                )
                asm_code = [
                    f"@{file_basename}.{value}",
                    f"D=M",
                    f"@{self.SP}",
                    f"M=M+1",
                    f"A=M-1",
                    f"M=D",
                ]

        elif cmd_type == CommandTypes.C_POP:
            if segment in ["local", "argument", "this", "that"]:
                asm_code = translate_regular_pop(mem_segment_base_map[segment], value)
            elif segment == "pointer":
                pointer_value_map = {"0": self.THIS, "1": self.THAT}
                asm_code = [
                    # *SP = *SP-1, D = *SP
                    f"@{self.SP}",
                    f"M=M-1",
                    f"A=M",
                    f"D=M",
                    # THIS/THAT = D
                    f"@{pointer_value_map[value]}",
                    f"M=D",
                ]
            elif segment == "temp":
                self.temp_vars.add("temp_var_0")
                asm_code = [
                    # temp_var_0 = (*mem_segment_ptr + value)
                    f"@{self.TEMP}",
                    f"D=A",
                    f"@{value}",
                    f"D=D+A",
                    f"@temp_var_0",
                    f"M=D",
                    # *SP = *SP-1, *temp_var_0 = *SP
                    f"@{self.SP}",
                    f"M=M-1",
                    f"A=M",
                    f"D=M",
                    f"@temp_var_0",
                    f"A=M",
                    f"M=D",
                ]
            elif segment == "static":
                file_basename = "".join(
                    os.path.basename(self.output_file_path).split(".")[:-1]
                )
                asm_code = [
                    f"@{self.SP}",
                    f"M=M-1",
                    f"A=M",
                    f"D=M",
                    f"@{file_basename}.{value}",
                    f"M=D",
                ]

        return asm_code

    def write_lines(self, lines: list) -> None:
        with open(self.output_file_path, "a") as f:
            f.writelines((f"{line}\n" for line in lines))


if __name__ == "__main__":
    VM_FILE_EXTENSION = ".vm"
    vm_dir, vm_files = "", []

    _, path = sys.argv
    if os.path.isfile(path):
        vm_dir = os.path.dirname(path)
        vm_files = [os.path.basename(path)] if path.endswith(VM_FILE_EXTENSION) else []
    elif os.path.isdir(path):
        vm_dir = os.path.dirname(path)
        vm_files = [f for f in os.listdir(vm_dir) if f.endswith(VM_FILE_EXTENSION)]

    for vm_file in vm_files:
        output_file_path = os.path.join(
            vm_dir, f"{vm_file[:-len(VM_FILE_EXTENSION)]}.asm"
        )
        parser = Parser(os.path.join(vm_dir, vm_file))
        codewriter = CodeWriter(output_file_path, parser=parser)
        codewriter.translate()
        print(f"Processed {vm_file}")
