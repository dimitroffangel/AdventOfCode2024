import os
import copy

print(os.getcwd())

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

input_file = open('./day8/input.txt', 'r', encoding='utf-8')
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

ROW_SIZE = len(map)
COL_SIZE = len(map[0])

added_antinodes = []

for type_of_satellitie in types_of_satellites:
    print(f'{type_of_satellitie} has {len(types_of_satellites[type_of_satellitie])} satellites')
    for position_index, position in enumerate(types_of_satellites[type_of_satellitie]):
        print(f'x: {position.x}, y: {position.y}')
        for other_position in types_of_satellites[type_of_satellitie][position_index + 1:]:
            if position == other_position:
                continue
            
            x_difference = abs(other_position.x - position.x)
            y_difference = abs(other_position.y - position.y)

            lhs_x_offset = 0
            lhs_y_offset = 0
            rhs_x_offset = 0
            rhs_y_offset = 0

            if position.x < other_position.x:
                lhs_x_offset = -1
                rhs_x_offset = 1
            elif position.x > other_position.x:
                lhs_x_offset = 1
                rhs_x_offset = -1

            if position.y < other_position.y:
                lhs_y_offset = -1
                rhs_y_offset = 1
            elif position.y > other_position.y:
                lhs_y_offset = 1
                rhs_y_offset = -1

            left_antipode = Position(position.x + x_difference * lhs_x_offset, position.y + y_difference * lhs_y_offset)
            right_antipode = Position(other_position.x + x_difference * rhs_x_offset, other_position.y + y_difference * rhs_y_offset)

            if left_antipode.x >= 0 and left_antipode.x < COL_SIZE and left_antipode.y >= 0 and left_antipode.y < ROW_SIZE and not added_antinodes.__contains__(left_antipode):
                added_antinodes.append(left_antipode)
                print(f'Added antinode at x: {left_antipode.x}, y: {left_antipode.y}')
                map[left_antipode.y] = map[left_antipode.y][:left_antipode.x] + ANTINODE_SYMBOL + map[left_antipode.y][left_antipode.x + 1:]
            
            if right_antipode.x >= 0 and right_antipode.x < COL_SIZE and right_antipode.y >= 0 and right_antipode.y < ROW_SIZE and not added_antinodes.__contains__(right_antipode):
                added_antinodes.append(right_antipode)
                print(f'Added antinode at x: {right_antipode.x}, y: {right_antipode.y}')
                map[right_antipode.y] = map[right_antipode.y][:right_antipode.x] + ANTINODE_SYMBOL + map[right_antipode.y][right_antipode.x + 1:]


print(f'Number of antinodes added ', len(added_antinodes))

for line in map:
    print(line)