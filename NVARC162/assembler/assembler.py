import sys
import math

compiler_version = "0.0.1"
cpu_ver = "NVARC162"

argv = sys.argv

interptreter_path = argv[0]

print(f"Version: {compiler_version}\nArc: {cpu_ver}")

# get input file
try:
    inputfile = argv[1]
except IndexError:
    print("No input file presented!")
    quit()

# get output file
try:
    outputfile = argv[2]
except IndexError:
    print("No output file presented!")
    quit()

# get input file content
try:
    with open(inputfile, "r") as f:
        inputcontent = str(f.read())
except Exception as e:
    print(f"Failed to read input file: {e}")
    quit()

reg_to_dec = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0,
    "E": 0,
    "F": 0,
    "G": 0,
    "H": 0,
    "JR": 0,
    "MEM": 0,
    "AALU": 0,
    "BALU": 0,
    "CALU": 0,
}

instr_to_dec = {
    "MOV": 1,
    "SWAP": 2,
    "CPY": 3,
    "WR": 4,
    "SHL": 5,
    "SHR": 6,
    "ST": 7,
    "LD": 8,
    "SUM": 9,
    "SUB": 10,
    "MUL": 11,
    "DIV": 12,
    "JMP": 13,
    "JC": 14,
    "JZ": 15,
    "JE": 16,
    "JL": 17,
    "JG": 18,
    "JLE": 19,
    "JGE": 20,
    "NOP": 21,
    "HLT": 22,
    "OR": 23,
    "AND": 24,
    "XOR": 25,
}

expected = {
    "MOV": ["r", "r"],
    "SWAP": ["r", "r"],
    "CPY": ["r", "r"],
    "WR": ["r", "v"],
    "SHL": ["r", "r"],
    "SHR": ["r", "r"],
    "ST": ["f", "r", "r"],
    "LD": ["f", "r", "r"],
    "SUM": [], 
    "SUB": [],
    "MUL": [],
    "DIV": [],
    "JMP": ["r"],
    "JC": ["r"],
    "JZ": ["r", "r"],
    "JE": ["r", "r"],
    "JL": ["r", "r"],
    "JG": ["r", "r"],
    "JLE": ["r", "r"],
    "JGE": ["r", "r"],
    "NOP": [],
    "HLT": [],
    "OR": ["r", "r", "r"],
    "AND": ["r", "r", "r"],
    "XOR": ["r", "r", "r"],
}

expected_to_string = {
    "f": "flag",
    "r": "register",
    "v": "number or binary value",
    "n": "unknown",
}

numbers = [ str(i) for i in range(0, 10) ]

def remove_spaces_front(string):
    while True:
        if len(string) > 0:
            if (string[-1] == " "):
                string = string[:-1]
            else:
                return string
        else:
            return ""

def remove_spaces_back(string):
    while True:
        if len(string) > 0:
            if (string[0] == " "):
                string = string[1:]
            else:
                return string
        else:
            return ""

def remove_spaces_front_back(string):
    return remove_spaces_front(remove_spaces_back(string))

def dec2bin(value, nums):
    return ("{:0>" + str(nums) + "b}").format(value)

def bin2dec(value):
    value = list(value)
    value.reverse()
    a = 0
    for i in range(len(value)):
        if value[i] == "1":
            a += 2**i
        elif value[i] == "0":
            pass
        else:
            return "error"
    return a

def decode_dec(value, line_num, line):
    try:
        value = int(value)
    except Exception as e:
        error(line_num, line, f"Invalid number!")
    return value

def decode_bin(value, line_num, line):
    value = bin2dec(value)
    if value == "error":
        error(line_num, line, f"Invalid binary value!")

def decode_bin_or_dec(value, line_num, line):
    if value[0] == "b":
        return decode_bin(value[1:], line_num, line)
    else:
        return decode_dec(value, line_num, line)

def decode_variable(value, line_num, line):
    try:
        return vars[value]
    except Exception as e:
        error(line_num, line, f"No variable named \"{value}\"!")

def decode_register(value, line_num, line):
    try:
        return reg_to_dec[value]
    except Exception as e:
        error(line_num, line, f"No register named \"{value}\"!")

def format_expected_string(string):
    try:
        if len(string) == 0:
            return "nothing"
        else:
            return ", ".join( expected_to_string[i] for i in string)
    except Exception as e:
        return "error"

def get_string_type(argument):
    if argument[0] == "$":
        return "v"
    elif argument[0] == "%":
        return "r"
    elif argument[0] == "b":
        return "v"
    elif argument[0] in numbers:
        return "v"
    else:
        return "n"

def get_string_types(arguments):
    return "".join([ get_string_type(i) for i in arguments ])

def decode_arg(value, line_num, line, argnum):
    if value[0] == "$":
        try:
            return vars[value[1:]]
        except Exception as e:
            error(line_num, line, f"No variable named \"{value}\"")
    elif value[0] == "%":
        try:
            return reg_to_dec[value[1:]]
        except Exception as e:
            error(line_num, line, f"No register named \"{value}\"!")
    elif value[0] == "b":
        value = bin2dec(value[1:])
        if value == "error":
            error(line_num, line, f"Invalid binary value in argument {argnum}!")
    elif value[0] == "b":
        value = bin2dec(value[1:])
        if value == "error":
            error(line_num, line, f"Invalid binary value in argument {argnum}!")
    elif value[0] in numbers:
        try:
            value = int(value)
            return value
        except Exception as e:
            error(line_num, line, f"Invalid number in argument {argnum}!")
    else:
        error(line_num, line, f"Invalid argument {argnum}!")

def error(line_num, line, error):
    print(f"Error on line {line_num}:")
    print(f"{line} <-- {error}")
    quit()

vars = {}
var_lines = []
prog_lines = []
lines = inputcontent.split("\n")
formatted_lines = []

# part 1
for i in range(len(lines)):
    temp = remove_spaces_front_back(lines[i])
    if temp != "":
        formatted_lines.append({"i": i, "line": temp})

# part 2
mode = None
for i in range(len(formatted_lines)):
    num = formatted_lines[i]["i"]
    line = formatted_lines[i]["line"]
    if line[-1] == ":":
        mode = line[:-1]
        if mode not in ["VAR", "PROG"]:
            error(num + 1, lines[num], f"No mode named \"{mode}\"")
    else:
        if mode == "VAR":
            var_lines.append({"i": num, "line": line})
        elif mode == "PROG":
            prog_lines.append({"i": num, "line": line})
        else:
            error(num + 1, lines[num], f"Undefined mode!")

# part 3
for i in range(len(var_lines)):
    num = var_lines[i]["i"]
    line = var_lines[i]["line"]
    arr = line.split(" ")
    if len(arr) == 2:
        name = arr[0]
        vars[name] = decode_bin_or_dec(arr[1], num + 1, lines[num])
    else:
        error(num + 1, lines[num], f"Syntax error!")

# part 4
for i in range(len(prog_lines)):
    num = prog_lines[i]["i"]
    line = prog_lines[i]["line"]
    if line[0] == "#":
        print("pointer")
    else:
        arr = line.split(" ")
        if len(arr) == 1:
            name = arr[0]
            args = []
        else:
            name = arr[0]
            args = "".join(arr[1:])
            args = args.split(",")
            args = [ remove_spaces_front_back(i) for i in args]
        try:
            instr_to_dec[name]
        except Exception as e:
            error(f"No instruction named \"{name}\"", num + 1, lines[num])
        _expected = "".join(expected[name])
        got = get_string_types(args)
        if _expected != got:
            error(f"Arguments error!\nExpected: {format_expected_string(_expected)}\nGot: {format_expected_string(got)}", num + 1, lines[num])