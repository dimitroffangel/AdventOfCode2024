import os
import copy

print(os.getcwd())

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
class PositionInformation:
    def __init__(self, previous_position, current_symbol):
        self.previous_position = previous_position
        self.current_symbol = current_symbol

input_file = open('./day6/example_input.txt', 'r', encoding='utf-8')
GUARD_SYMBOL = '^'
OBSTACLE_SYMBOL = '#'
ADDITONAL_OBSTACLE_SYMBOL = 'O'
FREE_SYMBOL = '.'
guard_map = [line for line in input_file]

# find the guard position first
guard_position = Position(0, 0)
current_guard_symbol = copy.copy(GUARD_SYMBOL)

has_guard_position_reached = False
for current_y, current_y_line in enumerate(guard_map):
    for current_x, current_symbol in enumerate(current_y_line):
        if current_symbol == GUARD_SYMBOL:
            guard_position = Position(current_x, current_y)
            has_guard_position_reached = True
            break
    if has_guard_position_reached:
        break

initial_guard_position = copy.copy(guard_position)

def move_guard(current_guard_symbol):
    match current_guard_symbol:
        case '^':
            return Position(0, -1)
        case '>':
            return Position(1, 0)
        case 'v':
            return Position(0, 1)
        case '<':
            return Position(-1, 0)
        
    print("move_guard() -> That shouldn't have happened")
    return Position(-1, -1)

def rotate_guard_direction(current_guard_symbol):
    match current_guard_symbol:
        case '^':
            return '>'
        case '>':
            return 'v'
        case 'v':
            return '<'
        case '<':
            return '^'
        
    print("rotate_guard_direction() -> That shouldn't have happened")
    return GUARD_SYMBOL

# iterate over the map
has_guard_reached_border = False
guard_map_size = len(guard_map)
guard_map_line_size = len(guard_map[0])
used_positions = [ [PositionInformation(Position(x, y), value) for x, value in enumerate(line)] for y, line in enumerate(guard_map) ]

while not has_guard_reached_border:

    next_guard_position = move_guard(current_guard_symbol) + guard_position
    if ((next_guard_position.y == 0 and current_guard_symbol == '^') or \
        (next_guard_position.y == guard_map_size - 1 and current_guard_symbol == 'v') or \
        (next_guard_position.x == 0 and current_guard_symbol == '<') or \
        (next_guard_position.x == guard_map_line_size - 1 and current_guard_symbol == '>')) and \
            guard_map[next_guard_position.y][next_guard_position.x] != OBSTACLE_SYMBOL:
         used_positions[next_guard_position.y][next_guard_position.x].current_symbol = current_guard_symbol
         used_positions[next_guard_position.y][next_guard_position.x].previous_position = guard_position
         has_guard_reached_border = True
        
    if guard_map[next_guard_position.y][next_guard_position.x] == OBSTACLE_SYMBOL:
        current_guard_symbol = rotate_guard_direction(current_guard_symbol)
    else:
        used_positions[next_guard_position.y][next_guard_position.x].previous_position = guard_position
        used_positions[next_guard_position.y][next_guard_position.x].current_symbol = current_guard_symbol

        guard_position = next_guard_position

number_of_entered_positions = 0

obstacle_positions = []

for y, map_line in enumerate(guard_map):
    for x, symbol in enumerate(map_line):
        if symbol == OBSTACLE_SYMBOL:
            obstacle_positions.append(Position(x, y))


def try_creating_cycle(cycle_position, guard_position, current_guard_symbol):
    guard_map_size = len(guard_map)
    guard_map_line_size = len(guard_map[0])

    start = copy.copy(guard_position)
    has_guard_reached_border = False
    has_entered_cycle = False

    used_map_directions = [ [x for x in line] for line in guard_map]
    
    while not has_guard_reached_border and not has_entered_cycle:
        next_guard_position = move_guard(current_guard_symbol) + guard_position
        if ((next_guard_position.y == 0 and current_guard_symbol == '^') or \
            (next_guard_position.y == guard_map_size - 1 and current_guard_symbol == 'v') or \
            (next_guard_position.x == 0 and current_guard_symbol == '<') or \
            (next_guard_position.x == guard_map_line_size - 1 and current_guard_symbol == '>')) and \
                guard_map[next_guard_position.y][next_guard_position.x] != OBSTACLE_SYMBOL and (next_guard_position.y != cycle_position.y or next_guard_position.x != cycle_position.x):
             has_guard_reached_border = True

        if guard_map[next_guard_position.y][next_guard_position.x] == OBSTACLE_SYMBOL or (next_guard_position.y == cycle_position.y and next_guard_position.x == cycle_position.x):
            current_guard_symbol = rotate_guard_direction(current_guard_symbol)
        else:
            guard_position = next_guard_position

        if used_map_directions[guard_position.y][guard_position.x] == current_guard_symbol:
            has_entered_cycle = True
        used_map_directions[guard_position.y][guard_position.x] = current_guard_symbol

    if has_entered_cycle:
        print("status for {} {}", cycle_position.x, cycle_position.x )
        for y, line in enumerate(used_map_directions):
            for x, value in enumerate(line):
                if x == start.x and y == start.y:
                    print('1', end='')
                elif x == cycle_position.x and y == cycle_position.y:
                    print('0', end='')
                else:
                    print(value, end='')
            print()

    return has_entered_cycle

number_cycles_found = 0

for current_y, line in enumerate(used_positions):
    for current_x, has_guard_been_there_initially in enumerate(line):
        if current_y == initial_guard_position.y and current_x == initial_guard_position.x:
            break

        if has_guard_been_there_initially.current_symbol != OBSTACLE_SYMBOL and has_guard_been_there_initially.current_symbol != FREE_SYMBOL and \
            has_guard_been_there_initially.current_symbol != '\n' :
            for obstacle in obstacle_positions:
                if abs(obstacle.y - current_y) != 1 and abs(obstacle.x - current_x) != 1:
                    continue
                current_guard_position = has_guard_been_there_initially.previous_position
                current_guard_symbol = used_positions[current_guard_position.y][current_guard_position.x].current_symbol
                number_cycles_found = number_cycles_found + try_creating_cycle(Position(current_x, current_y), current_guard_position, current_guard_symbol)
                break

print(number_cycles_found)