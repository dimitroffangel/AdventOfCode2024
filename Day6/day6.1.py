import os
import copy

print(os.getcwd())

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

input_file = open('./day6/example_input.txt', 'r', encoding='utf-8')
GUARD_SYMBOL = '^'
OBSTACLE_SYMBOL = '#'
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


def move_guard():
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

def rotate_guard_direction():
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
used_positions = [ [False for _ in range(guard_map_line_size)] for _ in guard_map ]

while not has_guard_reached_border:
    used_positions[guard_position.y][guard_position.x] = True

    next_guard_position = move_guard() + guard_position
    if ((next_guard_position.y == 0 and current_guard_symbol == '^') or \
        (next_guard_position.y == guard_map_size - 1 and current_guard_symbol == 'v') or \
        (next_guard_position.x == 0 and current_guard_symbol == '<') or \
        (next_guard_position.x == guard_map_line_size - 1 and current_guard_symbol == '>')) and \
            guard_map[next_guard_position.y][next_guard_position.x] != OBSTACLE_SYMBOL:
         used_positions[next_guard_position.y][next_guard_position.x] = True
         has_guard_reached_border = True
        
    if guard_map[next_guard_position.y][next_guard_position.x] == OBSTACLE_SYMBOL:
        current_guard_symbol = rotate_guard_direction()
    else:
        guard_position = next_guard_position

number_of_entered_positions = 0

for line in used_positions:
    for has_been_there in line:
         number_of_entered_positions = number_of_entered_positions + has_been_there

print(number_of_entered_positions)