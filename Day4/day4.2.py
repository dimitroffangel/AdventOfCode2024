import os
import math

print(os.getcwd())

chrismasCode = 'mas'

inputFile = open('./day4/day4.txt', 'r', encoding='utf-8')

inputMap = [line.lower().strip() for line in inputFile]
inputFile.close()

numberOfRows = len(inputMap)
numberOfColumns = len(inputMap[0])

def find_x_shape_two_mas(christmasMap, row, column):
    if row >= numberOfRows or column >= numberOfColumns or christmasMap[row][column] != 'a':
        return 0

    if row - 1 < 0 or row + 1 >= numberOfRows or column - 1 < 0 or column + 1 >= numberOfColumns:
        return 0
    
    number_of_x_mas = 0
    
    #m s 
    # a
    #m s
    if (christmasMap[row - 1][column - 1] == christmasMap[row + 1][column - 1] and christmasMap[row - 1][column - 1] == chrismasCode[0] and \
        christmasMap[row - 1][column + 1] == christmasMap[row + 1][column + 1] and christmasMap[row - 1][column + 1] == chrismasCode[2]):
        number_of_x_mas = number_of_x_mas + 1
    
    #s m 
    # a
    #s m
    if (christmasMap[row - 1][column - 1] == christmasMap[row + 1][column - 1] and christmasMap[row - 1][column - 1] == chrismasCode[2] and \
        christmasMap[row - 1][column + 1] == christmasMap[row + 1][column + 1] and christmasMap[row - 1][column + 1] == chrismasCode[0]):
        number_of_x_mas = number_of_x_mas + 1

    #m m 
    # a
    #s s
    if (christmasMap[row - 1][column - 1] == christmasMap[row - 1][column + 1] and christmasMap[row - 1][column - 1] == chrismasCode[0] and \
        christmasMap[row + 1][column - 1] == christmasMap[row + 1][column + 1] and christmasMap[row + 1][column + 1] == chrismasCode[2]):
        number_of_x_mas = number_of_x_mas + 1
    
    #s s 
    # a
    #m m
    if (christmasMap[row - 1][column - 1] == christmasMap[row - 1][column + 1] and christmasMap[row - 1][column - 1] == chrismasCode[2] and \
        christmasMap[row + 1][column - 1] == christmasMap[row + 1][column + 1] and christmasMap[row + 1][column - 1] == chrismasCode[0]):
        number_of_x_mas = number_of_x_mas + 1

    return number_of_x_mas
                
result = 0

for currentRow in range(numberOfRows):
    for currentColumn in range(numberOfColumns):
        result = result + find_x_shape_two_mas(inputMap, currentRow, currentColumn)

print(result)
