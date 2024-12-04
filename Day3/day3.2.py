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

def isReadingDo(brokenInstruction, currentIndex, size):
    return currentIndex + 4 < size and brokenInstruction[currentIndex] == 'd' and \
        brokenInstruction[currentIndex + 1] == 'o' and brokenInstruction[currentIndex + 2] == '(' \
        and brokenInstruction[currentIndex + 3] == ')'

def isReadingDont(brokenInstruction, currentIndex, size):
    return currentIndex + 7 < size and brokenInstruction[currentIndex] == 'd' and \
        brokenInstruction[currentIndex + 1] == 'o' and brokenInstruction[currentIndex + 2] == 'n' \
        and brokenInstruction[currentIndex + 3] == '\'' and brokenInstruction[currentIndex + 4] == 't' \
        and brokenInstruction[currentIndex + 5] == '(' and brokenInstruction[currentIndex + 6] == ')'

def isReadingMul(brokenInstruction, currentIndex, size):
    return i + 4 < size and brokenInstruction[currentIndex] == 'm' and brokenInstruction[currentIndex + 1] == 'u' \
        and brokenInstruction[currentIndex + 2] == 'l' and brokenInstruction[currentIndex + 3] == '('


inputFile = open('./day3/day3.txt', 'r', encoding='utf-8')

result = 0
isMulAllowed = True

for line in inputFile:
    sizeOfLine = len(line)
    i = 0
    while i < sizeOfLine:
        hasReadDo = isReadingDo(line, i, sizeOfLine)
        if hasReadDo:
            i =  i + 4
            isMulAllowed = True

        hasReadDont = isReadingDont(line, i, sizeOfLine)
        if hasReadDont:
            i = i + 7
            isMulAllowed = False

        hasDetectedMulOperation = isReadingMul(line, i, sizeOfLine)
        if not hasDetectedMulOperation:
            i = i + 1
            continue

        if hasDetectedMulOperation and not isMulAllowed:
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
