import sys
import math

compiler_version = "0.0.1"
cpu_ver = "V1"

argv = sys.argv

interptreter_path = argv[0]

compmode = ""
outputfile = ""

print(f"Version: {compiler_version}\nCPUVER: {cpu_ver}")

try:
    file_path = argv[1]
except IndexError:
    print("No file presented!")
    quit()

try:
    outputfile = argv[2]
except IndexError:
    print("Invalid output file!")
    quit()

try:
    compmode_ = argv[3]
    if compmode_ == "ezbinread":
        compmode = "ezbinread"
    elif compmode_ == "wiremod":
        compmode = "wiremod"
    else:
        print("Invalid compmode!")
        quit()
except IndexError:
    compmode = "ezbinread"

content = ""
with open(file_path, "r") as f:
    content = str(f.read())

def error(lines, i, desc):
    print(f"An error occured on line {i + 1}!")
    print(desc)
    print(f"{lines[i]} <--")
    print()
    quit()

lines = content.split("\n")
data_lines = []
prog_lines = []
mode = ""
vars = {}
pointers = {}

addr = 0
for i in range(len(lines)):
    l = lines[i]
    if len(l) > 0:
        while l[-1] == " ":
            l = l[:-1]
            if len(l) == 0:
                break
        if len(l) != 0:
            while l[0] == " ":
                l = l[1:]
            if l[-1] == ":":
                if l[:-1] == "DATA":
                    mode = "data"
                elif l[:-1] == "PROG":
                    mode = "prog"
                else:
                    error(lines, i, f"No mode named \"{l[:-1]}\"")
            elif l[0] == "#":
                p = l[1:]
                if p in pointers:
                    error(lines, i, f"Cant rewrite pointer!")
                elif p == "":
                    error(lines, i, f"Invalid pointer name!")
                elif " " in list(p):
                    error(lines, i, f"Pointer cant contain spaces!")
                else:
                    pointers[p] = addr + 3
            else:
                if mode == "data":
                    data_lines.append({"l": l, "i": i})
                elif mode == "prog":
                    prog_lines.append({"l": l, "i": i})
                addr += 3
prog_mem_size = (len(prog_lines) + 1) * 24

print(f"Program takes {prog_mem_size} bits ({int(prog_mem_size / 8)} bytes) of ROM")

def decode_val(val, enablevars, enablepointers):
    global vars
    start = 0
    if len(val) > 4:
        if val[:4] == "fmem":
            start = int(prog_mem_size / 8) + 1
            val = val[4:]
    if val[0] == "b":
        val = list(val[1:-1])
        val.reverse()
        a = 0
        for i in range(len(val)):
            if val[i] == "1":
                a += 2**i
        return start + a
    elif val[0] in [ str(i) for i in range(0, 10) ]:
        val = int(val)
        return start + val
    elif val[0] == "$":
        if enablevars:
            return start + vars[val[1:]]
        else:
            return "var"
    elif val[0] == "#":
        if enablepointers:
            try:
                return start + pointers[val[1:]]
            except Exception as e:
                return "pnf"
        else:
            return "p"

def encode_dec2bin(val:int, bits):
    return ("{:0>" + str(bits) + "b}").format(val)

for i in data_lines:
    l = i["l"]
    a = l.split(" ")
    if len(a) == 2:
        key = a[0]
        val = a[1]
        try:
            val = decode_val(val, False, False)
            print(val)
            if val == "var":
                error(lines, i["i"], f"Cant define variable using variable in data mode!")
            elif val == "p":
                error(lines, i["i"], f"Cant use pointers in data mode!")
        except Exception as e:
            error(lines, i["i"], f"Invalid value (decoder error)")
        if key != "":
            if key[0] in [ str(i) for i in range(0, 10) ]:
                error(lines, i["i"], f"Invalid variable name (cant start with number)")
            else:
                vars[key] = val
        else:
            error(lines, i["i"], f"Invalid variable name")
    else:
        error(lines, i["i"], f"Syntax error")

instr = [
    [31, int(prog_mem_size / 8), 0]
]

def decode_bin(val):
    val = list(val)
    val.reverse()
    a = 0
    for i in range(len(val)):
        if val[i] == "1":
            a += 2**i
    return a

for i in prog_lines:
    l = i["l"]
    ins = l.split(" ")
    name = ins[0]
    arg = None
    flags = 0
    if len(ins) == 2:
        try:
            arg = decode_val(ins[1], True, True)
            if arg == "pnf":
                error(lines, i["i"], f"No pointer named \"{val[1:]}\"!")
        except Exception as e:
            print(e)
            error(lines, i["i"], f"Invalid instruction argument")
    if len(ins) == 3:
        """try:
            flags = decode_val(ins[2], True, True)
        except Exception as e:
            error(lines, i["i"], f"Invalid instruction flags")"""
        error(lines, i["i"], f"Flags not implemented!")
    # LDA (1)
    if name == "LDA":
        if arg == None:
            error(lines, i["i"], f"LDA requires address as argument")
        else:
            instr.append([1, arg, flags])
    # LDB (2)
    elif name == "LDB":
        if arg == None:
            error(lines, i["i"], f"LDB requires address as argument")
        else:
            instr.append([2, arg, flags])
    # LDC (3)
    elif name == "LDC":
        if arg == None:
            error(lines, i["i"], f"LDC requires address as argument")
        else:
            instr.append([3, arg, flags])
    # STA (4)
    elif name == "STA":
        if arg == None:
            error(lines, i["i"], f"STA requires address as argument")
        else:
            instr.append([4, arg, flags])
    # STB (5)
    elif name == "STB":
        if arg == None:
            error(lines, i["i"], f"STB requires address as argument")
        else:
            instr.append([5, arg, flags])
    # STC (6)
    elif name == "STC":
        if arg == None:
            error(lines, i["i"], f"STC requires address as argument")
        else:
            instr.append([6, arg, flags])
    # SWAB (7)
    elif name == "SWAB":
        instr.append([7, 0, flags])
    # SWAC (8)
    elif name == "SWAC":
        instr.append([8, 0, flags])
    # SWBC (9)
    elif name == "SWBC":
        instr.append([9, 0, flags])
    # WRA (10)
    elif name == "WRA":
        if arg == None:
            error(lines, i["i"], f"WRA requires value as argument")
        else:
            instr.append([10, arg, flags])
    # WRB (11)
    elif name == "WRB":
        if arg == None:
            error(lines, i["i"], f"WRB requires value as argument")
        else:
            instr.append([11, arg, flags])
    # WRC (12)
    elif name == "WRC":
        if arg == None:
            error(lines, i["i"], f"WRC requires value as argument")
        else:
            instr.append([12, arg, flags])
    # WREXP (13)
    elif name == "WREXP":
        instr.append([13, 0, flags])
    # RDEXP (14)
    elif name == "RDEXP":
        instr.append([14, 0, flags])
    # SUM (15)
    elif name == "SUM":
        instr.append([15, 0, flags])
    # SUB (16)
    elif name == "SUB":
        instr.append([16, 0, flags])
    # MUL (17)
    elif name == "MUL":
        instr.append([17, 0, flags])
    # DIV (18)
    elif name == "DIV":
        instr.append([18, 0, flags])
    # JMP (19)
    elif name == "JMP":
        if arg == None:
            error(lines, i["i"], f"JMP requires address as argument")
        else:
            instr.append([19, arg, flags])
    # JMPE (20)
    elif name == "JMPE":
        if arg == None:
            error(lines, i["i"], f"JMPE requires address as argument")
        else:
            instr.append([20, arg, flags])
    # JMPC (21)
    elif name == "JMPC":
        if arg == None:
            error(lines, i["i"], f"JMPC requires address as argument")
        else:
            instr.append([21, arg, flags])
    # HLT (22)
    elif name == "HLT":
        instr.append([22, 0, flags])
    # LIM (31)
    elif name == "LIM":
        if arg == None:
            error(lines, i["i"], f"WRC requires address as argument")
        else:
            instr.append([31, arg, flags])
    else:
        error(lines, i["i"], f"Unknown instruction: \"{name}\"")

result = ""
if compmode == "ezbinread":
    for i in instr:
        result += "".join([encode_dec2bin(i[0], 5), encode_dec2bin(i[1], 16), encode_dec2bin(i[2], 3)]) + "\n"
elif compmode == "wiremod":
    arr = []
    for i in instr:
        Str = "".join([encode_dec2bin(i[0], 5), encode_dec2bin(i[1], 16), encode_dec2bin(i[2], 3)])
        a = Str[0:8]
        b = Str[8:16]
        c = Str[16:24]
        a = str(decode_bin(a))
        b = str(decode_bin(b))
        c = str(decode_bin(c))
        arr.append(a)
        arr.append(b)
        arr.append(c)
    result = "\n".join(arr)

with open(outputfile, "w") as f:
    f.write(result)