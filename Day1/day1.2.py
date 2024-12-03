import os

print(os.getcwd())

inputFile = open('./day1/day1.txt', 'r', encoding='utf-8')

lhsList = []
rhsList = []

for line in inputFile:
    lhs, rhs = map(int, line.split())
    lhsList.append(lhs)
    rhsList.append(rhs)

inputFile.close()

rhsListLength = len(rhsList)

result = [ 
    (currentList.count(currentList[rhsListLength]) - 1) * currentList[rhsListLength] 
          for currentList in [ rhsList + [lhs] for lhs in lhsList] 
    ]
print(sum(result))