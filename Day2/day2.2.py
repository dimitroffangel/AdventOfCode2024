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
    sizeOfCurrentLineOfLevel = len(currentLineOfLevel)
    if sizeOfCurrentLineOfLevel == 0:
        safeLines = safeLines + 1


    for indexOfRemovedElement in range(sizeOfCurrentLineOfLevel):
        currentList = currentLineOfLevel[:indexOfRemovedElement] + currentLineOfLevel[indexOfRemovedElement + 1:]
        isIncreasing = True
        isDecreasing = True
        for currentLevel in range(len(currentList) - 1):
            adjacentDifference = currentList[currentLevel + 1] - currentList[currentLevel]
            isIncreasing = isIncreasing and adjacentDifference > 0 
            isDecreasing = isDecreasing and adjacentDifference < 0

            absoluteDifference = abs(adjacentDifference)
            if absoluteDifference < -3 or absoluteDifference > 3:
                isIncreasing = False
                isDecreasing = False
                break

        if isIncreasing != isDecreasing:
            safeLines = safeLines + 1
            break

print(safeLines)