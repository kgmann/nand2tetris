import re

SPECIAL_SYMBOLS = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "LOOP": 4,
    "STOP": 18,
    "END": 22,
}

DEST = {
    "null": "000",
    "M": "001",
    "D": "010",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "ADM": "111",
    # quick hack to handle variations
    "MD": "011",
    "MA": "101",
    "DA": "110",
    "AMD": "111",
    "DAM": "111",
    "DMA": "111",
    "MAD": "111",
    "MDA": "111",
}

JUMP = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

ALU_CONTROLS = [
    "101010",
    "111111",
    "111010",
    "001100",
    "110000",
    "001101",
    "110001",
    "001111",
    "110011",
    "011111",
    "110111",
    "001110",
    "110010",
    "000010",
    "010011",
    "000111",
    "000000",
    "010101",
]

COMP = {
    # a = 0
    "0": "0" + ALU_CONTROLS[0],
    "1": "0" + ALU_CONTROLS[1],
    "-1": "0" + ALU_CONTROLS[2],
    "D": "0" + ALU_CONTROLS[3],
    "A": "0" + ALU_CONTROLS[4],
    "!D": "0" + ALU_CONTROLS[5],
    "!A": "0" + ALU_CONTROLS[6],
    "-D": "0" + ALU_CONTROLS[7],
    "-A": "0" + ALU_CONTROLS[8],
    "D+1": "0" + ALU_CONTROLS[9],
    "A+1": "0" + ALU_CONTROLS[10],
    "D-1": "0" + ALU_CONTROLS[11],
    "A-1": "0" + ALU_CONTROLS[12],
    "D+A": "0" + ALU_CONTROLS[13],
    "D-A": "0" + ALU_CONTROLS[14],
    "A-D": "0" + ALU_CONTROLS[15],
    "D&A": "0" + ALU_CONTROLS[16],
    "D|A": "0" + ALU_CONTROLS[17],
    # a = 1
    "M": "1" + ALU_CONTROLS[4],
    "!M": "1" + ALU_CONTROLS[6],
    "-M": "1" + ALU_CONTROLS[8],
    "M+1": "1" + ALU_CONTROLS[10],
    "M-1": "1" + ALU_CONTROLS[12],
    "D+M": "1" + ALU_CONTROLS[13],
    "D-M": "1" + ALU_CONTROLS[14],
    "M-D": "1" + ALU_CONTROLS[15],
    "D&M": "1" + ALU_CONTROLS[16],
    "D|M": "1" + ALU_CONTROLS[17],
    # quick hack to handle  (some) variations
    "A+D": "0" + ALU_CONTROLS[13],
    "A&D": "0" + ALU_CONTROLS[16],
    "A|D": "0" + ALU_CONTROLS[17],
    "M+D": "1" + ALU_CONTROLS[13],
    "M&D": "1" + ALU_CONTROLS[16],
    "M|D": "1" + ALU_CONTROLS[17],
}


def process_white_spaces(program: list) -> list:
    """
    Remove comments and strip
    """
    clean_program = []
    for line in program:
        line = line.split("//")[0].strip()
        if line:
            clean_program.append(line)
    return clean_program


def process_symbols(program: list) -> list:
    """
    Creates the full symbol table (special symbols, labels and variables), and apply it to the program
    """
    symbol_table = SPECIAL_SYMBOLS

    def process_labels(program: list) -> list:
        # add labels to the symbol table and remove them from the program
        new_program = []
        line_counter = 0
        for line in program:
            if (line[0] == "(") and (line[-1] == ")"):
                label = line[1:-1]
                symbol_table[label] = line_counter
            else:
                new_program.append(line)
                line_counter += 1
        return new_program

    def process_variables(program: list):
        # Update the symbol table to include variables
        var_counter = 16
        for line in program:
            if (line[0] == "@") and not line[1:].isdigit():
                symb = line[1:]
                if symb not in symbol_table:
                    symbol_table[symb] = var_counter
                    var_counter += 1

    def resolve_symbols(program):
        # Apply the symbol table to the program
        new_program = []
        for line in program:
            if (line[0] == "@") and not line[1:].isdigit():
                new_program.append(f"@{symbol_table[line[1:]]}")
            else:
                new_program.append(line)
        return new_program

    program = process_labels(program)
    process_variables(program)
    program = resolve_symbols(program)
    return program


def process_instructions(program: list) -> list:
    bin_program = []
    dest_pattern = re.compile(r'(.*?)=')
    comp_pattern = re.compile(r'(?:.*?=)?(.*?)(?:;|$)')
    jump_pattern = re.compile(r';(.*)')

    def a_inst_handler(inst: str) -> str:
        bin_num = bin(int(inst[1:]))[2:]
        bin_inst = "0"*(16-len(bin_num)) + bin_num
        return bin_inst

    def c_inst_handler(inst: str) -> str:
        match = dest_pattern.search(inst)
        dest = match.group(1) if match else "null"
        match = comp_pattern.search(inst)
        comp = match.group(1)
        match = jump_pattern.search(inst)
        jump = match.group(1) if match else "null"
        bin_inst = "111" + COMP[comp] + DEST[dest] + JUMP[jump]
        return bin_inst
    
    def inst_handler(inst:str)->str:
        if inst[0] == '@':
            return a_inst_handler(inst)
        else:
            return c_inst_handler(inst)
    
    for inst in program:
        bin_program.append(inst_handler(inst))
    return bin_program

def assembler(program: list)->list:
    program = process_white_spaces(program)
    program = process_symbols(program)
    program = process_instructions(program)
    return program

if __name__ == "__main__":
    import os
    import argparse
    
    parser = argparse.ArgumentParser(prog="HackAssembler", description="An assembler for the Hack Assembly Language")
    parser.add_argument("SOURCE", help="The Hack assembly program to convert to binary")
    parser.add_argument("DEST", nargs='?', help="The destination file  of the assembled program [Optional].")

    args = parser.parse_args()

    if args.DEST is None:
        base_dir, file_name = os.path.split(args.SOURCE)
        base_name, _ = os.path.splitext(file_name)
        default_dest = os.path.join(base_dir, f'{base_name}.hack')
        args.DEST = default_dest

    with open(args.SOURCE, "r") as source:
        program = source.readlines()

    program = assembler(program)

    with open(args.DEST,  "w") as dest:
        lines = [f"{line}\n" for line in program]
        dest.writelines(lines)
