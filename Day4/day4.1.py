import os
import math

print(os.getcwd())

chrismasCode = 'xmas'

inputFile = open('./day4/day4.txt', 'r', encoding='utf-8')

inputMap = [line.lower().strip() for line in inputFile]
inputFile.close()

numberOfRows = len(inputMap)
numberOfColumns = len(inputMap[0])

def find_christmas(christmasMap, row, column):
    timesEncounteredXMas = 0
    if row >= numberOfRows or column >= numberOfColumns or christmasMap[row][column] != 'x':
        return timesEncounteredXMas

    for row_iterator in range(-1, 2):
        if row + 3 * row_iterator < 0 or row + 3 * row_iterator >= numberOfRows:
            continue 

        for column_iterator in range(-1, 2):
            if row_iterator == 0 and column_iterator == 0:
                continue

            if column + 3 * column_iterator < 0 or column + 3 * column_iterator >= numberOfColumns:
                continue 

            isOnThePath = True
            for currentIndex in range(1, 4):
                if christmasMap[row + row_iterator * currentIndex][column + column_iterator * currentIndex] != chrismasCode[currentIndex]:
                    isOnThePath = False
                    break
            timesEncounteredXMas = timesEncounteredXMas + isOnThePath
        
    return timesEncounteredXMas
                
result = 0

for currentRow in range(numberOfRows):
    for currentColumn in range(numberOfColumns):
        result = result + find_christmas(inputMap, currentRow, currentColumn)


print(result)
