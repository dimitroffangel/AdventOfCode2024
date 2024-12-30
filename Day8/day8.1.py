import os
import copy

print(os.getcwd())

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

input_file = open('./day8/example_input.txt', 'r', encoding='utf-8')
map = []
map_of_antinodes = []
types_of_satellites = {}
EMPTY_SYMBOL = '.'
ANTINODE_SYMBOL = '#'


for y, line in enumerate(input_file):
    line = line.strip()
    map_of_antinodes.append(line)
    map.append(line)

    for x, symbol in enumerate(line):
        if symbol != EMPTY_SYMBOL and symbol != ANTINODE_SYMBOL:
            if not types_of_satellites.get(symbol):
                types_of_satellites[symbol] = []
            types_of_satellites[symbol].append(Position(x, y))

input_file.close()


for type_of_satellitie in types_of_satellites:
    print(f'{type_of_satellitie} has {len(types_of_satellites[type_of_satellitie])} satellites')
    for position in types_of_satellites[type_of_satellitie]:
        print(f'x: {position.x}, y: {position.y}')
        for other_position in types_of_satellites[type_of_satellitie]:
            if position == other_position:
                continue
            
            x_difference = abs(other_position.x - position.x)
            y_difference = abs(other_position.y - position.y)

            lhs_position = position if  position.x < other_position.x else other_position
            rhs_position = other_position if position.x < other_position.x else other_position



