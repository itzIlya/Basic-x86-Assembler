INVALID_SYNTAX = 69

reg32 = {
    "eax" : "000",
    "ecx" : "001",
    "edx" : "010",
    "ebx" : "011",
    "esp" : "100",
    "esi" : "110",
    "edi" : "111",
    "ebp" : "101"
}

reg16 = {
    "ax" : "000",
    "cx" : "001",
    "dx" : "010",
    "bx" : "011",
    "sp" : "100",
    "si" : "110",
    "di" : "111",
    "bp" : "101"
}

reg8 = {
    "al" : "000",
    "cl" : "001",
    "dl" : "010",
    "bl" : "011",
    "ah" : "100",
    "ch" : "101",
    "dh" : "110",
    "bh" : "111"
}

rd = {
    "eax" : 0,
    "ecx" : 1,
    "edx" : 2,
    "ebx" : 3,
    "esp" : 4,
    "ebp" : 5,
    "esi" : 6,
    "edi" : 7
}
rw = {
    "ax" : 0,
    "cx" : 1,
    "dx" : 2,
    "bx" : 3,
    "sp" : 4,
    "bp" : 5,
    "si" : 6,
    "di" : 7
}

registers32 = ["eax", "ecx", "edx", "ebx", "esp", "esi", "edi", "ebp"]

registers16 = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"]

registers8 = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]

def main():
    inputFile = open("tmp.txt", "r")
    outputFile = open("output.txt", "w")
    stack = []
    
    i =0
    memoryindex =0
    labels = {}
    lines =[0] * sum(1 for _ in open('tmp.txt'))

    for line in inputFile:
        
        line = line.rstrip()
        if line == '':
            continue
        line = line.replace(",", " ")
        line = line.replace("  ", " ")
        line = line.replace("   ", " ")
        line = line.replace("    ", " ")
        splitLine = line.split(" ")
        f=0
        while f < len(splitLine):
            if ',' == splitLine[f][0]:
                splitLine[f] = splitLine[f][1:]
            elif ',' == splitLine[f][-1]:
                splitLine[f] = splitLine[f][:-1]
            f+=1
        
        
        if (splitLine[0][-1] == ':'):
            labels[splitLine[0][:-1]] = memoryindex
            if len(splitLine) > 1:
                splitLine = splitLine[1:]
            else : 
                
                continue

        if splitLine[0].lower() == 'add':
            result = assemblyADD(splitLine[1], splitLine [2])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split())
            

        elif splitLine[0].lower() == 'or':
            result = assemblyOR(splitLine[1], splitLine [2])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split())

        elif splitLine[0].lower() == 'xor':
            result = assemblyXOR(splitLine[1], splitLine [2])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split()) 

        elif splitLine[0].lower() == 'and':
            result = assemblyAND(splitLine[1], splitLine [2])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split()) 

        elif splitLine[0].lower() == 'sub':
            result = assemblySUB(splitLine[1], splitLine [2])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split()) 
            
        elif splitLine[0].lower() == 'inc':
            result = assemblyINC(splitLine[1])
            lines[i]=  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split())

        elif splitLine[0].lower() == 'dec':
            result = assemblyDEC(splitLine[1])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split())

        elif splitLine[0].lower() == 'pop':
            ## pop kardane 4 ta byte az stack
            del stack[-1]
            del stack[-1]
            del stack[-1]
            del stack[-1]
            result = assemblyPOP(splitLine[1])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split())

        elif splitLine[0].lower() == 'push':
            # gozashtane esm ya meghdare parametere push(num8,num16,num32) tu stack array
            if splitLine[1] in registers32:
                stack += [splitLine[1]] * 4
            elif splitLine[1] in registers16:
                stack += [splitLine[1]] * 2 + ["MM"] *2
            elif isImmediate(splitLine[1]):
                if int(splitLine[1]) <2**8:
                    stack += ["num8"]  + ["MM"] *3 
                elif int(splitLine[1]) < 2**16:
                    stack +=  ["num16"] * 2 + ["MM"] *2
                else :
                    stack += ["num32"] * 4

            else:
                ## agar immediate nabod, register ham nabod pas hatman indirect address bode
                stack += ["MM"] * 4

            result = assemblyPUSH(splitLine[1])
            lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            memoryindex += len(result.split())
        elif splitLine[0].lower() == 'jmp':
            if splitLine[1] in labels:
                result = assemblyJMP(splitLine[1],labels,memoryindex+2)
                lines[i] =  "0x" + "0" * (16-len(str((hex(memoryindex))[2:]))) + (hex(memoryindex))[2:] + "  " + result
            
            else:
                lines[i] = "jmp " + splitLine[1] + " " + str(memoryindex)

            memoryindex += 2
        else:
            
            exit(69)
        i+=1
    line = 0
    while line < len(lines):
        if lines[line] == 0:
            line+=1
            continue
        tmp = lines[line].split()
        if tmp[0] == 'jmp':
            if tmp[1] in labels:
                result = assemblyJMP(tmp[1],labels,int(tmp[2])+2)
                lines[line] = "0x" + "0" * (16-len(str(tmp[2]))) + (hex(int(tmp[2])))[2:] + "  " + result
            else:
                exit(69)

        line+=1
    outputFile.seek(0)
    for line in lines:
        if line != 0:
            print(line, file=outputFile)


    outputFile.close()
    red = open("output.txt","r")
    codeSeg = []
    for line in red:
        splitLine = line.split()
        for i in range(len(splitLine)-1,0,-1):
            codeSeg += [splitLine[i]]
        if len(codeSeg)%2 == 1:
            codeSeg += ["MM"]
    
    print("code segment:",codeSeg) 
            
    print(stack)
    return stack, codeSeg
        
    
def getopcode(operand1, operand2):
    mode = 0
    
    opcode = ""
    opcodeD = ""
    opcodeS = ""
    mod = ""
    reg = ""
    rm = ""

    firstOperandIndirect = False
    secondOperandIndirect = False
    prefix16 = "66" 

    # Checking for indirect addresses
    if ("[" in operand1):
        firstOperandIndirect = True
        operand1 = operand1[1:-1]
    if ("[" in operand2):
        secondOperandIndirect = True
        operand2 = operand2[1:-1]

    # Error checking
    if (secondOperandIndirect and firstOperandIndirect):
        exit(INVALID_SYNTAX) 


    # Checking for 16 bit operands to add prefix
    if (operand1 in registers16 or operand2 in registers16): # Agar yeki az operand ha check beshe dovomi ham hamon size hast pas okaye
        opcode += prefix16 + " "
        opcodeS = "1"
        mode = 16
    elif (operand1 in registers32):
        opcodeS = "1"
        mode = 32
    else :
        opcodeS = "0"
        mode = 8
    

    # MOD REG R/M
    if (secondOperandIndirect):
        opcodeD = "1" # add RM to REG (az indirect address beriz toye register)
        mod="00" # RM is a zero byte displacement (dovomin operand indirect address hast (bedone displacement) pas mod 00)
        if mode==32:
            reg = reg32[operand1]
            rm = reg32[operand2]
        elif mode ==16:
            reg = reg16[operand1]
            rm = reg16[operand2]
        else:
            reg = reg8[operand1]
            rm = reg8[operand2]
            
    elif (firstOperandIndirect):
        opcodeD = "0" # Migim ke alan source toye Reg hast va destination toye RM
        mod = "00" #RM is a zero byte displacement . (avalin operand indirect address hast pas bayad bezarimesh toye rm va begim ke indirect hast va displacement ham nadarim)
        if mode==32:
            reg = reg32[operand2]
            rm = reg32[operand1]
        elif mode ==16:
            reg = reg16[operand2]
            try:
                rm = reg16[operand1]
            except:
                rm = reg32[operand1]
        else:
            reg = reg8[operand2]
            rm = reg8[operand1]

    else :
        opcodeD = "0"
        mod = "11" # RM is a register (hardota operand register hastand)
        if mode==32:
            reg = reg32[operand2]
            rm = reg32[operand1]
        elif mode ==16:
            reg = reg16[operand2]
            rm = reg16[operand1]
        else:
            reg = reg8[operand2]
            rm = reg8[operand1]
    return opcode,mod,reg,rm,opcodeD,opcodeS

def assemblyADD(operand1, operand2):
    opcode, mod,reg,rm,opcodeD,opcodeS = getopcode(operand1,operand2)
    output = opcode + bin2Hex("000000" + opcodeD + opcodeS) +" "+ bin2Hex(mod + reg + rm)
    return output


def assemblySUB(operand1, operand2):
    opcode, mod, reg,rm,opcodeD,opcodeS = getopcode(operand1,operand2)
 
    output = opcode + bin2Hex("001010" + opcodeD + opcodeS) +" "+ bin2Hex(mod + reg + rm)
    return output

def assemblyAND(operand1, operand2):
    opcode, mod, reg,rm,opcodeD,opcodeS = getopcode(operand1,operand2)

    output = opcode + bin2Hex("001000" + opcodeD + opcodeS) +" "+ bin2Hex(mod + reg + rm)
    return output

def assemblyOR(operand1, operand2):
    opcode, mod, reg,rm,opcodeD,opcodeS = getopcode(operand1,operand2)

    output = opcode + bin2Hex("000010" + opcodeD + opcodeS) +" "+ bin2Hex(mod + reg + rm)
    return output

def assemblyXOR(operand1, operand2):
    opcode, mod, reg,rm,opcodeD,opcodeS = getopcode(operand1,operand2)

    output = opcode + bin2Hex("001100" + opcodeD + opcodeS) +" "+ bin2Hex(mod + reg + rm)
    return output


def assemblyPOP(operand1):
    value = ""
    if (operand1 in rd):
        value = hex(int("58",16) + rd[operand1])[2:]
    elif (operand1 in rw):
        value = "66 " + hex(int("58",16) + rw[operand1])[2:]
    else:
        print("This assembler only accepts register operands for the POP instruction")
        exit(69)
    return value

def assemblyPUSH(operand1):
    value = ""
    if (operand1 in rd):
        value = hex(int("50",16) + rd[operand1])[2:]
    elif (operand1 in rw):
        value = "66 " + hex(int("50",16) + rw[operand1])[2:]
    elif(isImmediate(operand1)):
        if operand1[-1] == 'h' or operand1[-1] == 'H':
            operand1 = operand1[:-1]
            if (int(operand1,16) < 2**8):
                value = "6A " + operand1
            elif (int(operand1,16) < 2**16):
                value = "68 " + toLittleEndian32(operand1)
            elif (int(operand1,16) < 2**32):
                value = "68 " + toLittleEndian32(operand1)
        else:
            sth = hex(int(operand1))[2:]
            if (len(hex(int(operand1))[2:])) == 1:
                sth = "0" + sth
            if (int(operand1) < 2**8):
                value = "6A " + sth
            elif (int(operand1) < 2**16):
                value = "68 " + toLittleEndian32(sth)
            elif (int(operand1) < 2**32):
                value = "68 " + toLittleEndian32(sth)

    return value

def assemblyINC(operand1):
    value = ""
    if (operand1 in rd):
        value = hex(int("40",16) + rd[operand1])[2:]
    elif (operand1 in rw):
        value = "66 " + hex(int("40",16) + rw[operand1])[2:]
    elif (operand1 in reg8):
        value = "fe " + hex(int("11" + "000" + reg8[operand1],2))[2:]
    else:
        print("This assembler only accepts register operands for the INC instruction")
        exit(69)
    return value

def assemblyDEC(operand1):
    value = ""
    if (operand1 in rd):
        value = hex(int("48",16) + rd[operand1])[2:]
    elif (operand1 in rw):
        value = "66 " + hex(int("48",16) + rw[operand1])[2:]
    elif (operand1 in reg8):
        value = "fe " + hex(int("11" + "001" + reg8[operand1],2))[2:]
    else:
        print("This assembler only accepts register operands for the INC instruction")
        exit(69)
    return value

def assemblyJMP(operand1,labels,memoryindex):
    distance = labels[operand1] -memoryindex
    if distance <0:
        if distance >= -128:
            return "eb " + twos_complement_hex(distance)
    elif distance >= 0 and distance<= 127:
        return "eb " + "0" * (2- len(twos_complement_hex(distance))) + twos_complement_hex(distance)

    
def isImmediate(operand):
    for i in range(len(operand)):
        if (operand[i] >='0' and operand[i] <='9') or (operand[i]>='A' and operand[i] <= 'F') or (operand[i]>='a' and operand[i]<='f') or (i==len(operand)-1 and (operand[i] == 'h' or operand[i]=='H')):
            continue
        else:
            return False
    return True

def toLittleEndian32(operand):
    if (operand[-1] == 'h' or operand[-1]== 'H'):
        operand= operand[0:-1]

    val = "" + "0" * (8-len(operand)) + operand
    out = ""
    i=0
    while i < (len(val)):
        out = val[i]  + val[i+1] +" " + out
        i+=2
    return out



def bin2Hex(inp):
    x = int(inp[0:4])
    y = (inp[0:4])
    inp1 = hex(int(inp[0:4],2))[2:]
    inp2 = hex(int(inp[4:],2))[2:]

    return inp1 + inp2

def twos_complement_hex(decimal_value):
    bit_width = 8
    # Ensure the decimal value fits within the specified bit width
    max_value = 2**(bit_width - 1) - 1
    min_value = -2**(bit_width - 1)
    
    # Calculate the two's complement
    if decimal_value < 0:
        decimal_value = (1 << bit_width) + decimal_value
    
    # Convert to hexadecimal and return
    return hex(decimal_value)[2:]



def secondMain():
    inpfile = open("input.txt", "r")
    tmp = open("tmp.txt", "w")
    data = []
    codeSegment = dataSegment = False
    for line in inpfile:
        
        if ("stack" in line):
            listline = line.split("(")
            stackPosition = int(listline[1][:-2])
        elif ("data" in line):
            listline = line.split("(")
            dataPosition = int(listline[1][:-2])
            dataSegment = True
            continue
            
        elif ("code" in line):
            listline = line.split("(")
            codePosition = int(listline[1][:-2])
            codeSegment = True
            dataSegment=False
            continue

        if codeSegment:
            print(line, file=tmp) # reads input to tmp file for code segment processing 
        elif dataSegment: # Handles putting the data segment into an array
            
            listline = line.split(" ")
            
            if len(listline)<2:
                continue
            
            if listline[1].lower()[:-1]=="byte":
                
                data += [listline[0]]
            elif listline[1].lower()[:-1]=="word":
                
                data += [listline[0]] * 2 
            elif listline[1].lower()[:-1] == "dword":
                
                data += [listline[0]] * 4
    print(data)
    tmp.close()
    tup = main()
    stack, codeSeg = tup[0],tup[1] ## retrieves the stack segment and data segment from main
    counter = 0
    ## handles the printing of code segment, data segment and stack segment in the correct order
    ## printing the code segment
    for i in range(codePosition):
        print(f"   {counter:03}: |  "+"XX"+"  |")
        counter+=1
    print("CS " + f"{counter:03}: |  "+codeSeg[0]+"  |")
    counter+=1
    for i in range(1,len(codeSeg)):
        print(f"   {counter:03}: |  "+codeSeg[i]+"  |")
        counter+=1
    for i in range(32-len(codeSeg)):
        print(f"   {counter:03}: |  "+"MM"+"  |")
        counter+=1
    for i in range(dataPosition-counter):
        print(f"   {counter:03}: |  "+"XX"+"  |")
        counter+=1
    ## printing the data segment
    print("DS " + f"{counter:03}: |  "+data[0]+"  |")
    counter+=1
    for i in range(1,len(data)):
        print(f"   {counter:03}: |  "+data[i]+"  |")
        counter+=1
    for i in range(32-len(data)):
        print(f"   {counter:03}: |  "+"MM"+"  |")
        counter+=1

    for i in range(stackPosition-counter):
        print(f"   {counter:03}: |  "+"XX"+"  |")
        counter+=1
    ## printing the data the stack segment
    print("SS " + f"{counter:03}: |  "+stack[0]+"  |")
    counter+=1
    for i in range(1,len(data)):
        print(f"   {counter:03}: |  "+stack[i]+"  |")
        counter+=1
    for i in range(32-len(data)):
        print(f"   {counter:03}: |  "+"MM"+"  |")
        counter+=1

    for i in range(256-counter):
        print(f"   {counter:03}: |  "+"XX"+"  |")
        counter+=1
    
secondMain()

