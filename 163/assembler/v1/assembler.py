"""
======== LIBRARIES ========
"""
import sys
from colorama import Fore, Style
import json


"""
======== FUNCTIONS ========
"""
def dec2bin(val:int, bits):
    return ("{:0>" + str(bits) + "b}").format(val)

def bin2dec(val):
    val = list(val)
    val.reverse()
    a = 0
    for i in range(len(val)):
        if val[i] == "1":
            a += 2**i
        elif val[i] != "0":
            raise Exception()
    return a
print()


"""
======== PARSING ARGV ========
"""
argv = sys.argv

input_path = ""
output_path = ""

print(f"Assembler path: {argv[0]}")
if len(argv) > 1:
    input_path = argv[1]
    print(f"Found input path: {input_path}")
else:
    print("No input file!")
    quit()

if len(argv) > 2:
    output_path = argv[2]
    print(f"Found output path: {output_path}")
else:
    print("No output file!")
    quit()


"""
======== READING INPUT FILE ========
"""
try:
    with open(input_path, "r") as f:
        input_content = str(f.read())
except Exception as e:
    print(f"An error occured while reading input file: {e}")


"""
======== SECTIONING CODE LINES ========
"""
code = {
    "include":[],
    "data":[],
    "prog":[],
}
curr_section = None
lines = input_content.split("\n")
for i in range(len(lines)):
    line = lines[i].strip()
    if len(line) > 0:
        if line[-1] == ":":
            section = line[:-1].lower()
            if section in code:
                curr_section = section
        else:
            if curr_section != None:
                code[curr_section].append({"line": line, "line_num": i + 1, "from": input_path})
            else:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no section specified on line {i + 1} in file \"{input_path}\"!")
                quit()

"""
======== REMOVING COMMENTS ========
"""
code_wo_comments = {
    "include":[],
    "data":[],
    "prog":[],
}

for sec in code:
    for line_data in code[sec]:
        new_line = ""
        include_is_path = False
        include_path_def = ""
        line = line_data["line"]
        line_num = line_data["line_num"]
        file_from = line_data["from"]
        for i in range(len(line)):
            # includes are special cuz they have "" and '' where we dont want to find any --
            if sec == "include":
                if len(line) - i > 1:
                    if line[i] == "-" and line[i + 1] == "-" and not include_is_path:
                        break
                if line[i] in ["'", '"'] and not include_is_path and include_path_def == "":
                    new_line += line[i]
                    include_is_path = True
                    include_path_def = line[i]
                elif line[i] == include_path_def and include_is_path:
                    new_line += line[i]
                    include_is_path = False
                elif include_is_path:
                    new_line += line[i]
                elif line[i] in ["'", '"'] and not include_is_path and include_path_def != "":
                    print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant define second path in one line on line {line_num} in file \"{file_from}\"!")
                    quit()
                else:
                    new_line += line[i]
            else:
                if line[i] == "-" and line[i + 1] == "-" and not include_is_path:
                    break
                else:
                    new_line += line[i]
        if sec == "include" and include_is_path:
            print(f"{Fore.RED}FAILED:{Style.RESET_ALL} path string never ended on line {line_num} in file \"{file_from}\"!")
            quit()
        new_line = new_line.strip()
        if new_line != "":
            code_wo_comments[sec].append({"line": new_line, "line_num": line_num, "from": file_from})


"""
======== PREDEFINING STUFF ========
"""
vars = {}
pointers = {}


"""
======== READING INCLUDES ========
"""
includes = []
for i in range(len(code_wo_comments["include"])):
    line_data = code_wo_comments["include"][i]
    line = line_data["line"]
    line_num = line_data["line_num"]
    file_from = line_data["from"]
    if line[0] == line[-1] and line[0] in ["'", '"']:
        includes.append({"path": line[1:-1], "line_num": line_num, "from": file_from})
    else:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} failed to parse path on line {line_num} in file \"{file_from}\"!")
        quit()

for i in includes:
    path = i["path"]
    line_num = i["line_num"]
    file_from = i["from"]
    try:
        with open(path, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} failed to read include file \"{path}\" on line {line_num} in file \"{file_from}\"!\n{e}")
        quit()
    try:
        arr = json.loads(content)
    except Exception as e:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} failed parse included json file \"{path}\" on line {line_num} in file \"{file_from}\"!\n{e}")
        quit()
    try:
        for i in arr:
            for j in i:
                if j not in list("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"):
                    print(f"{Fore.RED}FAILED:{Style.RESET_ALL} incorrect variable name \"{i}\" in included json file \"{path}\" on line {line_num} in file \"{file_from}\"!")
                    quit()
            if i not in vars:
                value = arr[i]
                if value == "":
                    print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no value presented for ${i} in file \"{path}\"!")
                    quit()
                if type(value) == str:
                    vars[i] = {"value": arr[i], "line_num": None, "from": path}
                else:
                    print(f"{Fore.RED}FAILED:{Style.RESET_ALL} value type must be str in included json file \"{path}\" on line {line_num} in file \"{file_from}\"!")
                    quit()
            else:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant redefine ${i} from {vars[i]['from']} in included json file \"{path}\" on line {line_num} in file \"{file_from}\"!")
                quit()
    except Exception as e:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} failed to parse (internal exception) included json file \"{path}\" on line {line_num} in file \"{file_from}\"!\n{e}")
        quit()


"""
======== READING DATA ========
"""
for i in range(len(code_wo_comments["data"])):
    line_data = code_wo_comments["data"][i]
    line = line_data["line"]
    line_num = line_data["line_num"]
    file_from = line_data["from"]

    arr = line.split("=")
    if len(arr) == 2:
        name = arr[0].strip()
        value = arr[1].strip()
        for i in name:
            if i not in list("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"):
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} incorrect variable name \"{name}\" on line {line_num} in file \"{file_from}\"!")
                quit()
        if name not in vars:
            if value == "":
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no value presented for ${name} on line {line_num} in file \"{file_from}\"!")
                quit()
            vars[name] = {"value": value, "line_num": line_num, "from": file_from}
        else:
            print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant redefine ${name} from {vars[name]['from']} on line {line_num} in file \"{file_from}\"!")
            quit()
        
    else:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} failed to parse variable (should contain \"name = value\") on line {line_num} in file \"{file_from}\"!")
        quit()

"""
======== FIRST PROG READ (pointers stuff) ========
"""
instr_to_size = {
    "ld": 1,
    "st": 1,
    "ild": 1,
    "ist": 1,
    "sw": 3,
    "wr": 3,
    "cpy": 2,
    "shl": 1,
    "shr": 1,
    "mem": 1,
    "not": 2,
    "and": 2,
    "or": 2,
    "xor": 2,
    "sum": 2,
    "sub": 2,
    "mul": 2,
    "div": 2,
    "jmp": 1,
    "jc": 1,
    "je": 2,
    "jl": 2,
    "jg": 2,
    "jle": 2,
    "jge": 2,
    "nop": 1,
    "hlt": 1,
}
size = 0
prog_wo_pointers = []
for i in range(len(code_wo_comments["prog"])):
    line_data = code_wo_comments["prog"][i]
    line = line_data["line"]
    line_num = line_data["line_num"]
    file_from = line_data["from"]
    
    if line[0] == "#":
        name = line[1:].strip()
        for i in name:
            if i not in list("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"):
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} incorrect pointer name \"{name}\" on line {line_num} in file \"{file_from}\"!")
                quit()
        pointers[name] = {"value": size, "line_num": line_num, "from": file_from}
    else:
        name = line.split()[0].lower()
        if name in instr_to_size:
            prog_wo_pointers.append({"line": line, "line_num": line_num, "from": file_from})
            size += instr_to_size[name]
        else:
            print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no instruction named \"{line.split()[0]}\" on line {line_num} in file \"{file_from}\"!")
            quit()
code_wo_comments["prog"] = prog_wo_pointers


"""
======== SETTING PROPER VARS VALUES ========
"""
new_vars = {}
for i in vars:
    var_data = vars[i]
    value = var_data["value"]
    line_num = var_data["line_num"]
    file_from = var_data["from"]
    if len(value) > 4:
        if value[:4] == "fmem":
            num = value[4:]
            try:
                num = int(num)
                if num > 65535:
                    print(f"{Fore.YELLOW}WARNING:{Style.RESET_ALL} ${i} exceeds max 16-bit value {'on line ' if line_num != None else ''}{f'{line_num} ' if line_num != None else ''}in file \"{file_from}\"!")
            except Exception as e:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant parse int fmem value in ${i} {'on line ' if line_num != None else ''}{f'{line_num} ' if line_num != None else ''}in file \"{file_from}\"!")
                quit()
            new_vars[i] = {"value": num + size, "line_num": line_num, "from": file_from}
            continue
    if value[0] == "b":
        num = value[1:]
        try:
            num = bin2dec(num)
            if num > 65535:
                print(f"{Fore.YELLOW}WARNING:{Style.RESET_ALL} ${i} exceeds max 16-bit value {'on line ' if line_num != None else ''}{f'{line_num} ' if line_num != None else ''}in file \"{file_from}\"!")
        except Exception as e:
            print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant parse int fmem value in ${i} {'on line ' if line_num != None else ''}{f'{line_num} ' if line_num != None else ''}in file \"{file_from}\"!")
            quit()
        new_vars[i] = {"value": num, "line_num": line_num, "from": file_from}
        continue
    try:
        num = int(value)
        if num > 65535:
            print(f"{Fore.YELLOW}WARNING:{Style.RESET_ALL} ${i} exceeds max 16 bit value {'on line ' if line_num != None else ''}{f'{line_num} ' if line_num != None else ''}in file \"{file_from}\"!")
    except Exception as e:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant parse int fmem value in ${i} {'on line ' if line_num != None else ''}{f'{line_num} ' if line_num != None else ''}in file \"{file_from}\"!")
        quit()
    new_vars[i] = {"value": num, "line_num": line_num, "from": file_from}
vars = new_vars


"""
======== SECOND PROG READ (checking expected arguments) ========
"""
excepted_size = {
    "ld": [3],
    "st": [3],
    "ild": [3],
    "ist": [3],
    "sw": [3, 3],
    "wr": [3, 16],
    "cpy": [3, 3],
    "shl": [3],
    "shr": [3],
    "mem": [3],
    "not": [3, 3],
    "and": [3, 3, 3],
    "or": [3, 3, 3],
    "xor": [3, 3, 3],
    "sum": [3, 3, 3],
    "sub": [3, 3, 3],
    "mul": [3, 3, 3],
    "div": [3, 3, 3],
    "jmp": [],
    "jc": [],
    "je": [3, 3],
    "jl": [3, 3],
    "jg": [3, 3],
    "jle": [3, 3],
    "jge": [3, 3],
    "nop": [],
    "hlt": [],
}
excepted_size_to_string = {
    3: "%",
    16: "$, binary value, decimal value or #"
}

for i in range(len(code_wo_comments["prog"])):
    line_data = code_wo_comments["prog"][i]
    line = line_data["line"]
    line_num = line_data["line_num"]
    file_from = line_data["from"]
    
    name = line.split()[0].lower()
    if name not in excepted_size:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no instruction named \"{line.split()[0]}\" on line {line_num} in file \"{file_from}\"!")
        quit()
    str_args = line[len(name) + 1:]
    args = [j.strip() for j in str_args.split(",")]
    if args == [""]:
        args = []
    if len(args) != len(excepted_size[name]):
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} instruction \"{name}\" takes {len(excepted_size[name])} arguments, but only {len(args)} were given {line_num} in file \"{file_from}\"!")
        quit()

    for j in range(len(args)):
        arg = args[j]
        arg_size = 0
        if len(arg) > 4:
            if arg[:4] == "fmem":
                arg_size = 16
        if arg[0] == "%":
            arg_size = 3
        if arg[0] in ["#", "$", "b"]:
            arg_size = 16
        try:
            int(arg)
            arg_size = 16
        except ValueError:
            pass
        if arg_size != excepted_size[name][j]:
            print(f"{Fore.RED}FAILED:{Style.RESET_ALL} expected {excepted_size_to_string[arg_size]} as argument number {j + 1}, but got {excepted_size_to_string[arg_size] if arg_size in excepted_size_to_string else 'unknown'} on line {line_num} in file \"{file_from}\"!")
            quit()


"""
======== THIRD PROG READ (assembling) ========
"""
output = []
instruction_to_opcode = {
    "ld": 1,
    "st": 2,
    "ild": 3,
    "ist": 4,
    "sw": 5,
    "wr": 6,
    "cpy": 7,
    "shl": 8,
    "shr": 9,
    "mem": 10,
    "not": 11,
    "and": 12,
    "or": 13,
    "xor": 14,
    "sum": 15,
    "sub": 16,
    "mul": 17,
    "div": 18,
    "jmp": 19,
    "jc": 20,
    "je": 21,
    "jl": 22,
    "jg": 23,
    "jle": 24,
    "jge": 25,
    "nop": 26,
    "hlt": 0,
}
register_to_num = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}
for i in range(len(code_wo_comments["prog"])):
    line_data = code_wo_comments["prog"][i]
    line = line_data["line"]
    line_num = line_data["line_num"]
    file_from = line_data["from"]
    
    name = line.split()[0].lower()
    str_args = line[len(name) + 1:]
    args = [j.strip() for j in str_args.split(",")]
    if args == [""]:
        args = []
    asm_line = ""
    asm_line += dec2bin(instruction_to_opcode[name], 5)
    for j in range(len(args)):
        arg = args[j]
        if len(arg) > 4:
            if arg[:4] == "fmem":
                try:
                    asm_line += dec2bin(int(arg[4:]), 16)
                except ValueError:
                    print(f"{Fore.RED}FAILED:{Style.RESET_ALL} incorrect fmem value in argument number {j + 1} on line {line_num} in file \"{file_from}\"!")
                    quit()
        if arg[0] == "b":
            try:
                num = bin2dec(arg[1:])
                if num > 65535:
                    print(f"{Fore.YELLOW}WARNING:{Style.RESET_ALL} binary value exceeds max 16-bit value on line {line_num} in file \"{file_from}\"!")
                asm_line += dec2bin(num, 16)
            except Exception as e:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} incorrect binary value in argument number {j + 1} on line {line_num} in file \"{file_from}\"!")
                quit()
        elif arg[0] == "#":
            pointer = arg[1:].strip()
            if pointer not in pointers:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no pointer named \"{pointer}\" in argument number {j + 1} on line {line_num} in file \"{file_from}\"!")
                quit()
            asm_line += dec2bin(pointers[pointer]["value"], 16)
        elif arg[0] == "$":
            var = arg[1:].strip()
            if var not in vars:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no variable named \"{var}\" in argument number {j + 1} on line {line_num} in file \"{file_from}\"!")
                quit()
            asm_line += dec2bin(vars[var]["value"], 16)
        elif arg[0] == "%":
            reg = arg[1:].strip().lower()
            if reg not in register_to_num:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} no register named \"{arg[1:].strip()}\" in argument number {j + 1} on line {line_num} in file \"{file_from}\"!")
                quit()
            asm_line += dec2bin(register_to_num[reg], 3)
        else:
            try:
                asm_line += dec2bin(int(arg), 16)
            except ValueError:
                print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant parse argument number {j + 1} on line {line_num} in file \"{file_from}\"!")
                quit()
    try:
        asm_line += "0" * (instr_to_size[name] * 8 - len(asm_line))
    except Exception as e:
        print(f"{Fore.RED}FAILED:{Style.RESET_ALL} cant complete instruction on line {line_num} in file \"{file_from}\"!")
        quit()
    output.append(asm_line)

try:
    with open(output_path, "w") as f:
        f.write("\n".join(output))
except Exception as e:
    print(f"{Fore.RED}FAILED:{Style.RESET_ALL} failed to save output to \"{output_path}\"!")
    quit()


print(f"{Fore.GREEN}Build finished with no errors!{Style.RESET_ALL}\nOutput file: \"{output_path}\"")
print(f"Size: {size} bytes")
print(f"Reserved RAM: {0} bytes")