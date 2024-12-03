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

lhsList.sort()
rhsList.sort()

result = [abs(a - b) for a, b in zip(lhsList, rhsList)]
print(sum(result))