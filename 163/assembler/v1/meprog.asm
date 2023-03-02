INCLUDE:
    -- hello, this might fuck me up but it didnt!
    'C:\Users\vnnem\Desktop\NVARC tree\163\assembler\v1\mycfg.json' -- i need that
    "C:\Users\vnnem\Desktop\NVARC tree\163\assembler\v1\othercfg.json"
DATA:
    var2 = b1101
    myvar = 228
    arraymaxindex = 378
PROG:
    WR %C, $finishvalue
    #no -- will point to instruction under (WR %B, 1)
    WR %B, 1
    SUM %A, %B, %A
    WR %D, #yes
    MEM %D
    JE %A, %C
    WR %D, #no
    MEM %D
    JMP
    #yes
    WR %B, 0
    WR %C, 0
    WR %D, 0
    HLT