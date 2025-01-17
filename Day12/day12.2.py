import os
import copy
from enum import Enum
import queue

print(os.getcwd())

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    NONE = 5

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'( {self.y}, {self.x} )' 

class PlantNode:
    def __init__(self, position, previous_direction, is_lhs_side_marked = False, is_rhs_side_marked = False, is_up_side_marked = False, is_down_side_marked = False):
        self.position = position
        self.previos_direction = previous_direction
        self.is_rhs_side_marked = is_rhs_side_marked
        self.is_lhs_side_marked = is_lhs_side_marked
        self.is_up_side_marked = is_up_side_marked
        self.is_down_side_marked = is_down_side_marked

class Region:
    def __init__(self, plants, number_of_sides):
        self.plants = plants
        self.number_of_sides = number_of_sides



input_file = open('./day12/example_input.txt', 'r', encoding='utf-8')

plants_map = []
used_plants_for_region = []

for line in input_file:
    line = line.strip()
    plants_map.append(line)
    used_plants_for_region.append([False for _  in line])

PLANTS_MAP_ROW_SIZE = len(plants_map)
PLANTS_MAP_COL_SIZE = len(plants_map[0])

def get_plant_region(plant_position, plant_symbol):
    region = [plant_position]
    plants_to_iterate = queue.Queue()
    plants_to_iterate.put(PlantNode(plant_position, Direction.NONE))
    used_plants_for_region[plant_position.y][plant_position.x] = True

    number_of_sides = 0

    while not plants_to_iterate.empty():
        current_plant_iteration = plants_to_iterate.get()
        current_plant_position = current_plant_iteration.position
        current_plant_previous_direction = current_plant_iteration.previos_direction        

        for addition_y in range(-1, 2):
            for addition_x in range(-1, 2):
                if addition_x == 0 and addition_y == 0:
                    continue
                if addition_x != 0 and addition_y != 0:
                    continue

                adjacent_position = Position(current_plant_position.x + addition_x, current_plant_position.y + addition_y) 
                if adjacent_position.y < 0:
                    if current_plant_previous_direction == Direction.UP or current_plant_previous_direction == Direction.NONE:
                        current_plant_iteration.is_up_side_marked = True
                        number_of_sides+= 1
                    continue
                if adjacent_position.y >= PLANTS_MAP_ROW_SIZE:
                    if current_plant_previous_direction == Direction.DOWN or current_plant_previous_direction == Direction.NONE:
                        current_plant_iteration.is_down_side_marked = True
                        number_of_sides+= 1
                    continue
                if adjacent_position.x < 0:
                    if current_plant_previous_direction == Direction.LEFT or current_plant_previous_direction == Direction.NONE:
                        current_plant_iteration.is_left_side_marked = True
                        number_of_sides+= 1
                    continue
                if adjacent_position.x >= PLANTS_MAP_COL_SIZE:
                    if current_plant_previous_direction == Direction.RIGHT or current_plant_previous_direction == Direction.NONE:
                        current_plant_iteration.is_rhs_side_marked = True
                        number_of_sides+=1
                    continue 
                
                current_direction = Direction.NONE
                if x == -1:
                    current_direction = Direction.LEFT
                elif x == 1:
                    current_direction = Direction.RIGHT
                elif y == -1:
                    current_direction = Direction.UP
                else:
                    current_direction = Direction.DOWN

                if plants_map[adjacent_position.y][adjacent_position.x] != plant_symbol:
                    if current_plant_previous_direction == Direction.NONE:
                        if current_direction == Direction.UP:
                            current_plant_iteration.is_up_side_marked = True
                        if current_direction == Direction.DOWN:
                            current_plant_iteration.is_down_side_marked = True
                        if current_direction == Direction.RIGHT:
                            current_plant_iteration.is_rhs_side_marked = True
                        if current_direction == Direction.LEFT:
                            current_plant_iteration.is_left_side_marked = True
                            
                        number_of_sides+=1
                    else:
                        if current_direction == Direction.UP:
                            if current_plant_previous_direction == Direction.UP:
                                number_of_sides+=1
                            elif (current_plant_previous_direction == Direction.LEFT or current_plant_previous_direction == Direction.RIGHT):
                                if not current_plant_iteration.is_lhs_side_marked:
                                    current_plant_iteration.is_lhs_side_marked = True
                                if not current_plant_iteration.is_rhs_side_marked:
                                    current_plant_iteration.is_rhs_side_marked = True
                        if current_direction == Direction.DOWN:
                            if current_plant_previous_direction == Direction.DOWN:
                                number_of_sides+=1
                            elif (current_plant_previous_direction == Direction.LEFT or current_plant_previous_direction == Direction.RIGHT):
                                if not current_plant_iteration.is_lhs_side_marked:
                                    current_plant_iteration.is_lhs_side_marked = True
                                if not current_plant_iteration.is_rhs_side_marked:
                                    current_plant_iteration.is_rhs_side_marked = True
                        if current_direction == Direction.LEFT:
                            if current_plant_previous_direction == Direction.LEFT:
                                number_of_sides+=1
                            elif (current_plant_previous_direction == Direction.UP or current_plant_previous_direction == Direction.DOWN):
                                if not current_plant_iteration.is_up_side_marked:
                                    current_plant_iteration.is_up_side_marked = True
                                if not current_plant_iteration.is_down_side_marked:
                                    current_plant_iteration.is_down_side_marked = True
                        if current_direction == Direction.RIGHT:
                            if current_plant_previous_direction == Direction.RIGHT:
                                number_of_sides+=1
                            elif (current_plant_previous_direction == Direction.UP or current_plant_previous_direction == Direction.DOWN):
                                if not current_plant_iteration.is_up_side_marked:
                                    current_plant_iteration.is_up_side_marked = True
                                if not current_plant_iteration.is_down_side_marked:
                                    current_plant_iteration.is_down_side_marked = True
                    continue

                if used_plants_for_region[adjacent_position.y][adjacent_position.x]:
                    continue 

                is_lhs_side_marked = current_plant_iteration.is_lhs_side_marked
                is_rhs_side_marked = current_plant_iteration.is_rhs_side_marked
                is_up_side_marked = current_plant_iteration.is_up_side_marked
                is_down_side_marked = current_plant_iteration.is_down_side_marked
                if (current_direction == Direction.RIGHT or current_direction == Direction.LEFT) and \
                    (current_plant_previous_direction == Direction.UP or current_plant_previous_direction == Direction.DOWN):
                    is_lhs_side_marked = False
                    is_rhs_side_marked = False

                if  (current_direction == Direction.UP or current_direction == Direction.DOWN) and \
                    (current_plant_previous_direction == Direction.LEFT or current_plant_previous_direction == Direction.RIGHT):
                    is_up_side_marked = False
                    is_down_side_marked = False

                used_plants_for_region[adjacent_position.y][adjacent_position.x] = True
                plants_to_iterate.put(
                    PlantNode(adjacent_position, current_direction, 
                              is_lhs_side_marked, is_rhs_side_marked, 
                              is_up_side_marked, is_down_side_marked))
                region.append(adjacent_position)

    return Region(region, number_of_sides)

plant_regions = []

for y, current_plant_line in enumerate(plants_map):
    for x, current_plant_symbol in enumerate(current_plant_line):
        if used_plants_for_region[y][x]:
            continue

        initial_plant_position = Position(x, y) 
        current_plant_region = get_plant_region(initial_plant_position, current_plant_symbol)
        plant_regions.append(current_plant_region)

for current_region in plant_regions:
    print(f'Current plant symbol {plants_map[current_region.plants[0].y][current_region.plants[0].x]} ')
    for current_plant in current_region.plants:
        print(current_plant, end = '')

    print()

total_price = 0
for current_region in plant_regions:
    area = len(current_region.plants)
    current_region_symbol = plants_map[current_region.plants[0].y][current_region.plants[0].x]

    print(f'Symbol: {current_region_symbol}; Area: {area}; Number of sides: {current_region.number_of_sides};')
    total_price += area * current_region.number_of_sides

print(total_price)