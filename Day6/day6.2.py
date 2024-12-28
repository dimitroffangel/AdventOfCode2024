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

class CachedNearestObstacle:
    def __init__(self, lhs_position, rhs_position, up_position, down_position):
        self.lhs_position = lhs_position
        self.rhs_position = rhs_position
        self.up_position = up_position
        self.down_position = down_position

input_file = open('./day6/input.txt', 'r', encoding='utf-8')
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
guard_map_line_size = len(guard_map[0]) - 1
used_positions = [ [PositionInformation(Position(x, y), value) for x, value in enumerate(line)] for y, line in enumerate(guard_map) ]
cached_closest_obstacle_distance = []
outside_map_position = Position(-2, -2)

for y, line in enumerate(guard_map):
    cached_closest_obstacle_distance.append([])
    for x, symbol in enumerate(line):
        if symbol == '\n':
            continue

        if symbol == OBSTACLE_SYMBOL:
            nearestObstacles = CachedNearestObstacle(Position(-10, -10), Position(-10, -10), Position(-10, -10), Position(-10, -10))
            cached_closest_obstacle_distance[y].append(nearestObstacles)
            continue
        
        nearestObstacles = CachedNearestObstacle(Position(-1, y), Position(guard_map_line_size, y), Position(x, -1), Position(x, guard_map_size))

        # calculate the distance for this
        for adjacent_x in range(guard_map_line_size):
            if x - adjacent_x >= 0 and guard_map[y][x - adjacent_x] == OBSTACLE_SYMBOL and x - adjacent_x > nearestObstacles.lhs_position.x:
                nearestObstacles.lhs_position = Position(x - adjacent_x + 1, y)
            
            if x + adjacent_x < guard_map_line_size and guard_map[y][x + adjacent_x] == OBSTACLE_SYMBOL and x + adjacent_x < nearestObstacles.rhs_position.x:
                nearestObstacles.rhs_position = Position(x + adjacent_x - 1, y)
        
        for adjacent_y in range(guard_map_size):
            if y - adjacent_y >= 0 and guard_map[y - adjacent_y][x] == OBSTACLE_SYMBOL and y - adjacent_y > nearestObstacles.up_position.y:
                nearestObstacles.up_position = Position(x, y - adjacent_y + 1)
            
            if y + adjacent_y < guard_map_size and guard_map[y + adjacent_y][x] == OBSTACLE_SYMBOL and y + adjacent_y < nearestObstacles.down_position.y:
                nearestObstacles.down_position = Position(x, y + adjacent_y - 1)

        if nearestObstacles.lhs_position.x == -1 and nearestObstacles.lhs_position.y == y:
            nearestObstacles.lhs_position = outside_map_position
        if nearestObstacles.rhs_position.x == guard_map_line_size and nearestObstacles.rhs_position.y == y:
            nearestObstacles.rhs_position = outside_map_position
        if nearestObstacles.up_position.x == x and nearestObstacles.up_position.y == -1:
            nearestObstacles.up_position = outside_map_position
        if nearestObstacles.down_position.x == x and nearestObstacles.down_position.y == guard_map_size:
            nearestObstacles.down_position = outside_map_position
        cached_closest_obstacle_distance[y].append(nearestObstacles)

number_of_cycles_found = 0

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

# number_of_entered_positions = 0

obstacle_positions = []

for y, map_line in enumerate(guard_map):
    for x, symbol in enumerate(map_line):
        if symbol == OBSTACLE_SYMBOL:
            obstacle_positions.append(Position(x, y))

def find_next_obstacle(position, direction):
    match direction:
        case '^':
            return cached_closest_obstacle_distance[position.y][position.x].up_position
        case 'v':
            return cached_closest_obstacle_distance[position.y][position.x].down_position
        case '<':
            return cached_closest_obstacle_distance[position.y][position.x].lhs_position
        case '>':
            return cached_closest_obstacle_distance[position.y][position.x].rhs_position
    
    print("find_next_obstacle() -> That shouldn't have happened")
    return Position(-2, -2)
        
        

def try_creating_cycle(cycle_position, guard_position, current_guard_symbol):
    guard_map_size = len(guard_map)
    guard_map_line_size = len(guard_map[0]) - 1

    has_guard_position_reached = False
    has_entered_cycle = False

    used_map_directions = [ [x for x in line ] for line in guard_map]

    while not has_guard_position_reached and not has_entered_cycle:
        next_position = find_next_obstacle(guard_position, current_guard_symbol)

        if next_position.x == outside_map_position.x and next_position.y == outside_map_position.y:
            has_guard_position_reached = True
            
        current_guard_symbol = rotate_guard_direction(current_guard_symbol)
        guard_position = next_position

        if used_map_directions[guard_position.y][guard_position.x] == current_guard_symbol:
            has_entered_cycle = True

        used_map_directions[guard_position.y][guard_position.x] = current_guard_symbol

    return has_entered_cycle

number_cycles_found = 0

def update_cached_obstacles(obstacle_position):
    for adjacent_x in range(guard_map_line_size)[1:]:
        if obstacle_position.x - adjacent_x > 0 and \
            cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x - adjacent_x].rhs_position.x != -10 and \
            (obstacle_position.x - 1 < cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x - adjacent_x].rhs_position.x or \
                cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x - adjacent_x].rhs_position.x == -2):
            cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x - adjacent_x].rhs_position = obstacle_position + Position(-1, 0)
        
        if obstacle_position.x + adjacent_x < guard_map_line_size and \
            cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x + adjacent_x].lhs_position.x != -10 and \
            (obstacle_position.x + 1 > cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x + adjacent_x].lhs_position.x or \
                cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x + adjacent_x].lhs_position.x == -2):
            cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x + adjacent_x].lhs_position = obstacle_position + Position(1, 0)

    for adjacent_y in range(guard_map_size)[1:]:
        if obstacle_position.y - adjacent_y > 0 and \
            cached_closest_obstacle_distance[obstacle_position.y - adjacent_y][obstacle_position.x].down_position.y != -10 and \
            (obstacle_position.y - 1 < cached_closest_obstacle_distance[obstacle_position.y - adjacent_y][obstacle_position.x].down_position.y or \
                cached_closest_obstacle_distance[obstacle_position.y - adjacent_y][obstacle_position.x].down_position.y == -2):
            cached_closest_obstacle_distance[obstacle_position.y - adjacent_y][obstacle_position.x].down_position = obstacle_position + Position(0, -1)
        
        if obstacle_position.y + adjacent_y < guard_map_size  and \
            cached_closest_obstacle_distance[obstacle_position.y + adjacent_y][obstacle_position.x].up_position.y != -10 and \
            (obstacle_position.y + 1 > cached_closest_obstacle_distance[obstacle_position.y + adjacent_y][obstacle_position.x].up_position.y or \
                cached_closest_obstacle_distance[obstacle_position.y + adjacent_y] == -2):
            cached_closest_obstacle_distance[obstacle_position.y + adjacent_y][obstacle_position.x].up_position = obstacle_position + Position(0, 1)

    cached_closest_obstacle_distance[obstacle_position.y][obstacle_position.x] = CachedNearestObstacle(Position(-10, -10), Position(-10, -10), Position(-10, -10), Position(-10, -10))

for current_y, line in enumerate(used_positions):
    for current_x, has_guard_been_there_initially in enumerate(line):
        if current_y == initial_guard_position.y and current_x == initial_guard_position.x:
            break

        if has_guard_been_there_initially.current_symbol != OBSTACLE_SYMBOL and has_guard_been_there_initially.current_symbol != FREE_SYMBOL and \
            has_guard_been_there_initially.current_symbol != '\n' :
            for obstacle in obstacle_positions:
                if abs(obstacle.y - current_y) != 1 and abs(obstacle.x - current_x) != 1:
                    continue

                if obstacle.y == current_y or obstacle.x == current_x:
                    continue

                changed_vertical_line = []
                changed_horizontal_line = []

                for horizontal in range(guard_map_line_size):
                    changed_horizontal_line.append(copy.deepcopy(cached_closest_obstacle_distance[current_y][horizontal]))
                
                for vertical in range(guard_map_size):
                    changed_vertical_line.append(copy.deepcopy(cached_closest_obstacle_distance[vertical][current_x]))

                update_cached_obstacles(Position(current_x, current_y))

                current_guard_position = copy.deepcopy(initial_guard_position)
                current_guard_symbol = '^'
                has_found_cycle_result = try_creating_cycle(Position(current_x, current_y), current_guard_position, current_guard_symbol)
                number_cycles_found = number_cycles_found + has_found_cycle_result
                for horizontal in range(guard_map_line_size):
                    cached_closest_obstacle_distance[current_y][horizontal].lhs_position = changed_horizontal_line[horizontal].lhs_position
                    cached_closest_obstacle_distance[current_y][horizontal].rhs_position = changed_horizontal_line[horizontal].rhs_position
                
                for vertical in range(guard_map_size):
                    cached_closest_obstacle_distance[vertical][current_x].up_position = changed_vertical_line[vertical].up_position
                    cached_closest_obstacle_distance[vertical][current_x].down_position = changed_vertical_line[vertical].down_position

                if has_found_cycle_result:
                    print("Cycle found at position: ", current_x, current_y)
                break

print(number_cycles_found)