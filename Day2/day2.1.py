import os

print(os.getcwd())

inputFile = open('./day2/day2.txt', 'r', encoding='utf-8')

listOfLevels = []

for line in inputFile:
    currentListOfLevels = []
    for currentLevel in line.split():
        currentListOfLevels.append(int(currentLevel))
    listOfLevels.append(currentListOfLevels)

inputFile.close()

safeLines = 0

for currentLineOfLevel in listOfLevels:
    if len(currentLineOfLevel) == 0:
        safeLines = safeLines + 1

    currentDiff = currentLineOfLevel[0]
    isIncreasing = True
    isDecreasing = True
    for currentLevel in range(len(currentLineOfLevel) - 1):
        adjacentDifference = currentLineOfLevel[currentLevel + 1] - currentLineOfLevel[currentLevel]
        isIncreasing = isIncreasing and adjacentDifference > 0 
        isDecreasing = isDecreasing and adjacentDifference < 0

        absoluteDifference = abs(adjacentDifference)
        if absoluteDifference < -3 or absoluteDifference > 3:
            isIncreasing = False
            isDecreasing = False
            break

    if isIncreasing != isDecreasing:
        safeLines = safeLines + 1

print(safeLines)