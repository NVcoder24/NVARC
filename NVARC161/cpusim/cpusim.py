"""
NVARC161 CPU SIMULATOR
BY NVcoder
"""

# BASE VARS
VERSION = "0.0.1"
conf_name = "cpusim_conf.json"

# WELCOME SCREEN
print("========== INFO ==========")
print("NVARC161 CPU SIMULATOR")
print(f"VERSION: {VERSION}")

# PREINIT
print("========== PREINIT ==========")

print("LOADING LIBS...")
try:
    import json
    import time
    import numpy as np
    import argparse
    import sys
except Exception as e:
    print(f"FAILED!\n{e}")
    quit()
print("LIBS VERSIONS:")
print(f"[1] json: {json.__version__}")
print(f"[2] numpy: {np.__version__}")
print(f"[3] argparse: {argparse.__version__}")
print(f"[4] time: UNKNOWN")
print(f"[5] sys: UNKNOWN")

print("PARSING ARGS...")
try:
    prog_path = sys.argv[1]
except Exception as e:
    print(f"FAILED!\n{e}")
    quit()

# INIT
print("========== INIT ==========")

print(f"LOADING CONFIG \"{conf_name}\"...")
conf = {}
try:
    with open("cpusim_conf.json", "r") as f:
        conf = json.loads(f.read())
except Exception as e:
    print(f"Failed to open {conf_name}")
    quit()

print("CHECKING CONFIG...")
check = ""
check_num = 1
try:
    # check data_encodings
    check = "data_encodings"
    print(f"[{check_num}] check: {check}")
    if "data_encodings" not in conf:
        print(f"FAILED!\nfailed on {check}")
        quit()
    if type(conf["data_encodings"]) != dict:
        print(f"FAILED!\nfailed on {check}")
        quit()
    check_num += 1

    # check data_encodings > UIO
    check = "data_encodings > UIO"
    print(f"[{check_num}] check: {check}")
    if "UIO" not in conf["data_encodings"]:
        print(f"FAILED!\nfailed on {check}")
        quit()
    if type(conf["data_encodings"]["UIO"]) != dict:
        print(f"FAILED!\nfailed on {check}")
        quit()
    check_num += 1
    
    # check data_encodings > UIO > values
    check = "data_encodings > UIO > values"
    print(f"[{check_num}] check: {check}")
    for i in conf["data_encodings"]["UIO"]:
        if (type(i) != str):
            print(f"FAILED!\nfailed on {check}: invalid key")
            quit()
        if (type(conf["data_encodings"]["UIO"][i]) != int):
            print(f"FAILED!\nfailed on {check}: invalid value")
            quit()
    check_num += 1

    # check data_encodings > display
    check = "data_encodings > display"
    print(f"[{check_num}] check: {check}")
    if "display" not in conf["data_encodings"]:
        print(f"FAILED!\nfailed on {check}")
        quit()
    if type(conf["data_encodings"]["display"]) != list:
        print(f"FAILED!\nfailed on {check}")
        quit()
    check_num += 1

    # check data_encodings > display > values
    check = "data_encodings > display > values"
    print(f"[{check_num}] check: {check}")
    for i in conf["data_encodings"]["display"]:
        if (type(i) != str):
            print(f"FAILED!\nfailed on {check}: invalid key")
            quit()
    check_num += 1
    
    # check RAM
    check = "RAM"
    print(f"[{check_num}] check: {check}")
    if "RAM" not in conf:
        print(f"FAILED!\nfailed on {check}")
        quit()
    if type(conf["RAM"]) != dict:
        print(f"FAILED!\nfailed on {check}")
        quit()
    check_num += 1
    
    # check RAM > amount
    check = "RAM > amount"
    print(f"[{check_num}] check: {check}")
    if "amount" not in conf["RAM"]:
        print(f"FAILED!\nfailed on {check}")
        quit()
    if type(conf["RAM"]['amount']) != int:
        print(f"FAILED!\nfailed on {check}")
        quit()
    check_num += 1

    # check RAM > max_prog_mem
    check = "RAM > max_prog_mem"
    print(f"[{check_num}] check: {check}")
    if "max_prog_mem" not in conf["RAM"]:
        print(f"FAILED!\nfailed on {check}")
        quit()
    if type(conf["RAM"]['max_prog_mem']) != int:
        print(f"FAILED!\nfailed on {check}")
        quit()
    check_num += 1
    
    # check RAM > UIO_loc
    check = "RAM > UIO_loc"
    print(f"[{check_num}] check: {check}")
    if "UIO_loc" not in conf["RAM"]:
        print(f"FAILED!\nfailed on {check}")
        quit()
    if type(conf["RAM"]['UIO_loc']) != int:
        print(f"FAILED!\nfailed on {check}")
        quit()
    check_num += 1
    
    # check RAM > display_loc
    check = "RAM > display_loc"
    print(f"[{check_num}] check: {check}")
    if "display_loc" not in conf["RAM"]:
        print(f"FAILED!")
        quit()
    if type(conf["RAM"]['display_loc']) != list:
        print(f"FAILED!")
        quit()
    check_num += 1
    
    # check RAM > display_loc > values
    check = "RAM > display_loc > values"
    print(f"[{check_num}] check: {check}")
    if len(conf["RAM"]['display_loc']) != 2:
        print(f"FAILED!")
        quit()
    if type(conf["RAM"]['display_loc'][0]) != int or type(conf["RAM"]['display_loc'][1]) != int:
        print(f"FAILED!")
        quit()
    check_num += 1
    
    # check CPU
    check = "CPU"
    print(f"[{check_num}] check: {check}")
    if "CPU" not in conf:
        print(f"FAILED!")
        quit()
    if type(conf["CPU"]) != dict:
        print(f"FAILED!")
        quit()
    check_num += 1
    
    # check CPU > tps
    check = "CPU > tps"
    print(f"[{check_num}] check: {check}")
    if "tps" not in conf["CPU"]:
        print(f"FAILED!")
        quit()
    if type(conf["CPU"]['tps']) != int:
        print(f"FAILED!")
        quit()
    check_num += 1
    
    # check display
    check = "display"
    print(f"[{check_num}] check: {check}")
    if "display" not in conf:
        print(f"FAILED!")
        quit()
    if type(conf["display"]) != dict:
        print(f"FAILED!")
        quit()
    check_num += 1
    
    # check display > enabled
    check = "display > enabled"
    print(f"[{check_num}] check: {check}")
    if "enabled" not in conf["display"]:
        print(f"FAILED!")
        quit()
    if type(conf["display"]['enabled']) != bool:
        print(f"FAILED!")
        quit()
    check_num += 1
    
    # check display > resolution
    check = "display > resolution"
    print(f"[{check_num}] check: {check}")
    if "resolution" not in conf["display"]:
        print(f"FAILED!")
        quit()
    if type(conf["display"]["resolution"]) != list:
        print(f"FAILED!")
        quit()
    check_num += 1
    
    # check display > resolution > values
    check = "display > resolution > values"
    print(f"[{check_num}] check: {check}")
    if len(conf["display"]['resolution']) != 2:
        print(f"FAILED!")
        quit()
    if type(conf["display"]['resolution'][0]) != int or type(conf["display"]['resolution'][1]) != int:
        print(f"FAILED!")
        quit()
    check_num += 1

    # check sim
    check = "sim"
    print(f"[{check_num}] check: {check}")
    if "sim" not in conf:
        print(f"FAILED!")
        quit()
    if type(conf["sim"]) != dict:
        print(f"FAILED!")
        quit()
    check_num += 1

    # check sim > debug_level
    check = "sim > debug_level"
    print(f"[{check_num}] check: {check}")
    if "debug_level" not in conf["sim"]:
        print(f"FAILED!")
        quit()
    if type(conf["sim"]["debug_level"]) != int:
        print(f"FAILED!")
        quit()
    if conf["sim"]["debug_level"] not in [0, 1, 2, 3]:
        print(f"FAILED!")
        quit()
    check_num += 1

    # check sim > program_type
    check = "sim > program_type"
    print(f"[{check_num}] check: {check}")
    if "program_type" not in conf["sim"]:
        print(f"FAILED!")
        quit()
    if type(conf["sim"]["program_type"]) != str:
        print(f"FAILED!")
        quit()
    if conf["sim"]["program_type"] not in ["ezbinread", "wiremod", "truebin"]:
        print(f"FAILED!")
        quit()
    check_num += 1
except Exception as e:
    print(f"FAILED (Exception)!\n{e}")
    quit()

print("ASSIGNING CONFIG VALUES...")
try:
    UIO_enc = conf["data_encodings"]["UIO"]
    display_enc = conf["data_encodings"]["display"]
    ram_amount = conf["RAM"]["amount"]
    max_prog_mem = conf["RAM"]["max_prog_mem"]
    UIO_loc = conf["RAM"]["UIO_loc"]
    display_loc = conf["RAM"]["display_loc"]
    tps = conf["CPU"]["tps"]
    display_enable = conf["display"]["enabled"]
    display_resolution = conf["display"]["resolution"]
    debug_level = conf["sim"]["debug_level"]
    program_type = conf["sim"]["program_type"]
except Exception as e:
    print(f"FAILED!\n{e}")
    quit()

print("CHECKING VALUES COMPATIBILITY...")
check_num = 1
try:
    print(f"[{check_num}] checking sim")
    if program_type == "wiremod":
        print(f"FAILED!\nprogram type \"wiremod\" is not supported yet!")
        quit()
    if program_type == "truebin":
        print(f"FAILED!\nprogram type \"truebin\" is not supported yet!")
        quit()
    check_num += 1
    print(f"[{check_num}] checking display")
    if display_resolution[0] < 1 or display_resolution[1] < 1:
        print("display resolution xy should be equal or greater than 1!")
    check_num += 1
    print(f"[{check_num}] checking CPU")
    if tps < 1:
        print("CPU TPS should be equal or greater than 1!")
    check_num += 1
    print(f"[{check_num}] checking RAM")
    if display_loc[1] < display_loc[0]:
        print(f"FAILED!\ndisplay loc address from cant be less than address to!")
        quit()
    if display_loc[1] - display_loc[0] < display_resolution[0] * display_resolution[1]:
        print(f"FAILED!\ndisplay with resolution {display_resolution[0]}x{display_resolution[1]} requires minimum {display_resolution[0] * display_resolution[1]} bytes but only {display_loc[1] - display_loc[0]} were given!")
        quit()
    if UIO_loc in range(display_loc[0], display_loc[1] + 1):
        print(f"FAILED!\nUIO address should not intersect with display addresses!")
        quit()
    if UIO_loc in range(0, max_prog_mem + 1):
        print(f"FAILED!\nUIO address should not intersect with program memory addresses!")
        quit()
    if display_loc[0] <= max_prog_mem:
        print(f"FAILED!\ndisplay addresses should not intersect with program memory addresses!")
        quit()
    if ram_amount > 65535:
        print("FAILED!\nRAM addersses beyond 65535 bytes are inaccessible! (max ram amount)")
        quit()
    if display_loc[1] > ram_amount:
        print(f"FAILED!\ndisplay to address exceeds RAM amount!")
        quit()
    if UIO_loc > ram_amount:
        print(f"FAILED!\nUIO address exceeds RAM amount!")
        quit()
except Exception as e:
    print(f"FAILED!\n{e}")
    quit()

# SETUP
print("========== SETUP ==========")

print(f"ALLOCATING RAM ({ram_amount} bytes)...")
try:
    ram = np.zeros(ram_amount, dtype=np.int16)
except Exception as e:
    print(f"FAILED: {e}")
    quit()

program = ""
print(f"LOADING PROGRAM...")
print(f"[1] opening \"{prog_path}\"")
try:
    with open(prog_path, "r") as f:
        print(f"[1] reading")
        program = str(f.read())
except Exception as e:
    print(f"FAILED!\n{e}")
    quit()
print(f"[3] validating")
try:
    prog_intructions = program.split("\n")
    for i in range(len(prog_intructions)):
        if (len(prog_intructions[i]) != 24):
            print(f"FAILED!\nline: {i + 1}")
            quit()
        for j in prog_intructions[i]:
            if j not in ["0", "1"]:
                print(f"FAILED!\nline: {i + 1}")
                quit()
except Exception as e:
    print(f"FAILED!\n{e}")
    quit()

# EXECUTING
print("========== EXECUTING ==========")
start_input = False
while True:
    nput = input("Do you want to continue? [n/y]: ")
    if nput == "n":
        break
    elif nput == "y":
        start_input = True
        break
    else:
        print("Invalid input! Try again!")
if start_input:
    print()
else:
    quit()