import os
import math

print(os.getcwd())


class InstructionNumber:
    def __init__(self, number, offset):
        self.number = number
        self.offset = offset

def readNumber(brokenInstruction):
    if not brokenInstruction[0].isdigit():
        return InstructionNumber(math.nan, 0)
    
    currentInstructionIndex = 0
    currentNumber = 0
    while currentInstructionIndex < len(brokenInstruction) and brokenInstruction[currentInstructionIndex].isdigit():
        currentNumber = currentNumber * 10 + ord(brokenInstruction[currentInstructionIndex]) - ord('0')
        currentInstructionIndex = currentInstructionIndex + 1
    
    return InstructionNumber(currentNumber, currentInstructionIndex)


inputFile = open('./day3/day3.txt', 'r', encoding='utf-8')

result = 0

for line in inputFile:
    sizeOfLine = len(line)
    i = 0
    while i < sizeOfLine:
        hasDetectedMulOperation = i + 4 < sizeOfLine and line[i] == 'm' and line[i + 1] == 'u' and line[i+2] == 'l' and line[i + 3] == '('
        if not hasDetectedMulOperation:
            i = i + 1
            continue

        lhsInstruction = readNumber(line[i + 4:])
        if math.isnan(lhsInstruction.number):
            i = i + 4 + lhsInstruction.offset
            continue

        i = i + 4 + lhsInstruction.offset 
        if i >= sizeOfLine or line[i] != ',':
            continue
        
        rhsInstruction = readNumber(line[i +1:])
        if math.isnan(rhsInstruction.number):
            continue
        
        i = i + 1 + rhsInstruction.offset
        if i >= sizeOfLine or line[i] != ')':
            continue

        i = i + 1
        result = result + lhsInstruction.number * rhsInstruction.number

inputFile.close()

print(result)
