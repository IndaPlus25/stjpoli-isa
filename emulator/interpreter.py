import sys
import pathlib

# 8 general-purpose 32-bit registers
registers = [0] * 8

# All labels get logged in the labels dictionary
labels = {}

### Functions for each instruction ###

# rd = imm
def LOAD(args):
    r = int(args[0][1:])
    val = int(args[1])
    registers[r] = val
    print(f'reg{r} = {val}')

# rd = rs + rt
def ADD(args):
    rd = int(args[0][1:])
    rs = int(args[1][1:])
    rt = int(args[2][1:])
    registers[rd] = registers[rs] + registers[rt]
    print(f'reg{rd} = {registers[rs] + registers[rt]}')

# rs = rt
def MOVE(args):
    rd = int(args[0][1:])
    rs = int(args[1][1:])
    registers[rd] = registers[rs]
    print(f'reg{rd} = {registers[rs]}')

 
def JUMP(args, pc):
    r = int(args[0][1:])
    label = args[1]
    if registers[r] != 0: # if the registry is not 0 we return the line of the label that is refered to
        print(f'Jumping to line {labels[label]}')
        return labels[label]
    return pc + 1 # else we go to the next line

# Print whatever is in the register
def OUT(args):
    r = int(args[0][1:])
    print("OUT:", registers[r])
    

### Reading the assembly file ###

def read_instructions(file: pathlib.Path):
    # Create a list with one element for each line of code
    lines = file.read_text().split("\n")
    instructions = []
    for line in lines:
        end_index = len(line) if line.find("//") == -1 else line.find("//")
        instructions.append(line[0:end_index].strip())
    return instructions

# Saves all the jumps to the dictionary where key: "name of the label value" value: "the line number/idx"
def find_labels(instructions):
    idx = 0
    for line in instructions:
        if line.endswith(":"):
            labels[line[:-1]] = idx
        else:
            idx += 1

def execute(instructions):
# pc is the program counter
    pc = 0
    prog = [
    line for line in instructions 
    if not line.endswith(":") and line.strip() != ""
    ] #we remove the lines with labels

    while pc < len(prog):
        print("line:", pc)

        parts = prog[pc].replace(",", "").split() # Take away the commas not to get ["ADD", "r1,", "r2,", "r3"]
        instruction = parts[0].upper()
        args = parts[1:]
        if instruction == "LOAD":
            LOAD(args)
        elif instruction == "ADD":
            ADD(args)
        elif instruction == "MOVE":
            MOVE(args)
        elif instruction == "JUMP":
            pc = JUMP(args, pc)
            continue
        elif instruction == "OUT":
            OUT(args)
        else:
            raise ValueError(f"Unknown instruction '{instruction}' at line {pc}")

        pc += 1

### Main ###

def main():
    file_path = "C:/Users/Test/DD1337/stjpoli-isa/program/factorial.asm"
    file = pathlib.Path(file_path)

    instructions = read_instructions(file)
    find_labels(instructions)
    execute(instructions)
    sys.exit(1)
    


if __name__ == "__main__":
    main()