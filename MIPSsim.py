
#MIPS simulator
#Vinicius Muller Silveira 26/04/24

from datetime import datetime

fileName = "program.txt"
supportedIntructions = ["addi","add","sub","halt","noop","beq"]
instructionMem = []
fillValues = {}
labelValues = {}
programCounter = 0
PC = 0
register = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


class instructionStruct:
    def __init__(self,OpCode, Op1, Op2, Op3, Temp1, Temp2, Temp3):
        self.OpCode = OpCode
        self.Op1 = Op1
        self.Op2 = Op2
        self.Op3 = Op3
        self.Temp1 = Temp1
        self.Temp2 = Temp2
        self.Temp3 = Temp3


IF_ID = instructionStruct("","","","","","","")
ID_EX = instructionStruct("","","","","","","")
EX_MEM = instructionStruct("","","","","","","")
MEM_WB = instructionStruct("","","","","","","")

def readFile():
    f = open(fileName, "r")
    lines = f.readlines()
    for line in lines:
        # print(line, end="")
        # print(line.split(" ")[0])
        if(".fill" in line):
            fillValues[line.split(" ")[0]] = int(line.split(" ")[2])
        elif(line.split(" ")[0].strip() in supportedIntructions):
            instructionMem.append(line.rstrip('\n'))
        else:
            labelValues[line.split(" ")[0]] = len(instructionMem)
            instructionMem.append(line.rstrip('\n').replace(line.split(" ")[0] + " ",""))
    print(instructionMem)
    print(fillValues)
    print(labelValues)

def executeStage1():
    # read instruction mem and fill IF/ID
    print("Stage 1: " + instructionMem[programCounter])
    IF_ID.OpCode = instructionMem[programCounter].split(" ")[0]
    IF_ID.Op1 = instructionMem[programCounter].split(" ")[1] if len(instructionMem[programCounter].split(" "))>1 else ""
    IF_ID.Op2 = instructionMem[programCounter].split(" ")[2] if len(instructionMem[programCounter].split(" "))>1 else ""
    IF_ID.Op3 = instructionMem[programCounter].split(" ")[3] if len(instructionMem[programCounter].split(" "))>1 else ""

def executeStage2():
    print("Stage 2: " + str(IF_ID.OpCode) + " " + str(IF_ID.Op1) + " " + str(IF_ID.Op2) + " " + str(IF_ID.Op3))
    ID_EX.OpCode = IF_ID.OpCode
    ID_EX.Op1 = IF_ID.Op1
    ID_EX.Op2 = IF_ID.Op2
    ID_EX.Op3 = IF_ID.Op3

def addi():
    if("R" in ID_EX.Op1):
        ID_EX.Op1 = ID_EX.Op1.replace("R","")
    
    if("R" in ID_EX.Op2):
        ID_EX.Op2 = ID_EX.Op2.replace("R","")
    
    if(ID_EX.Op3 in fillValues):
        ID_EX.Op3 = fillValues[ID_EX.Op3]

    ID_EX.Temp1 = register[int(ID_EX.Op1)] + int(ID_EX.Op3)

def add():
    ID_EX.Temp1 = register[int(ID_EX.Op1)] + register[int(ID_EX.Op2)]

def beq():
    if(register[int(EX_MEM.Op1)] == register[int(EX_MEM.Op2)]):
        globals()["programCounter"] = labelValues[EX_MEM.Op3]
        

def executeStage3():
    print("Stage 3: " + str(ID_EX.OpCode) + " " + str(ID_EX.Op1) + " " + str(ID_EX.Op2) + " " + str(ID_EX.Op3))
    
    if(ID_EX.OpCode == "addi"):
        addi()
    if(ID_EX.OpCode == "add"):
        add()

    EX_MEM.OpCode = ID_EX.OpCode
    EX_MEM.Op1 = ID_EX.Op1
    EX_MEM.Op2 = ID_EX.Op2
    EX_MEM.Op3 = ID_EX.Op3
    EX_MEM.Temp1 = ID_EX.Temp1
    

def executeStage4():
    print("Stage 4: " + str(EX_MEM.OpCode) + " " + str(EX_MEM.Op1) + " " + str(EX_MEM.Op2) + " " + str(EX_MEM.Op3))
    
    if(EX_MEM.OpCode == "beq"):
        beq()

    MEM_WB.OpCode = EX_MEM.OpCode
    MEM_WB.Op1 = EX_MEM.Op1
    MEM_WB.Op2 = EX_MEM.Op2
    MEM_WB.Op3 = EX_MEM.Op3
    MEM_WB.Temp1 = EX_MEM.Temp1

def executeStage5():
    print("Stage 5: " + str(MEM_WB.OpCode) + " " + str(MEM_WB.Op1) + " " + str(MEM_WB.Op2) + " " + str(MEM_WB.Op3))
    if(MEM_WB.OpCode == "addi"):
        register[int(MEM_WB.Op2)] = MEM_WB.Temp1
    if(MEM_WB.OpCode == "add"):
        register[int(MEM_WB.Op3)] = MEM_WB.Temp1


readFile()

print("LOOP PRINCIPAL")
while(True):
    input()
    print("-------")
    print("PC: " + str(programCounter) + " | r0-r31: " + str(register))
    if(MEM_WB.OpCode != ""):
        executeStage5()
    if(EX_MEM.OpCode != ""):
        executeStage4()
    if(ID_EX.OpCode != ""):
        executeStage3()
    if(IF_ID.OpCode != ""):
        executeStage2()
    if(programCounter < len(instructionMem)):
        executeStage1()
        programCounter += 1
    else:
        print("fim do código")
        break
