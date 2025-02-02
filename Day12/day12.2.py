import os
import copy
from enum import Enum
import queue

print(os.getcwd())

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'( {self.y}, {self.x} )' 

input_file = open('./day12/input.txt', 'r', encoding='utf-8')

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
    plants_to_iterate.put(plant_position)
    used_plants_for_region[plant_position.y][plant_position.x] = True

    while not plants_to_iterate.empty():
        current_plant_iteration = plants_to_iterate.get()

        for addition_y in range(-1, 2):
            for addition_x in range(-1, 2):
                if addition_x == 0 and addition_y == 0:
                    continue
                if addition_x != 0 and addition_y != 0:
                    continue

                adjacent_position = Position(current_plant_iteration.x + addition_x, current_plant_iteration.y + addition_y) 
                if adjacent_position.y < 0 or adjacent_position.y >= PLANTS_MAP_ROW_SIZE or \
                    adjacent_position.x < 0 or adjacent_position.x >= PLANTS_MAP_COL_SIZE or \
                    plants_map[adjacent_position.y][adjacent_position.x] != plant_symbol or \
                    used_plants_for_region[adjacent_position.y][adjacent_position.x]:
                        continue
                
                used_plants_for_region[adjacent_position.y][adjacent_position.x] = True
                plants_to_iterate.put(adjacent_position)
                region.append(adjacent_position)

    return region

def visit_of_walls_in_line(wall_position, used_positions):
    walls_to_visit = queue.Queue()
    walls_to_visit.put(wall_position)
    used_positions[wall_position.y][wall_position.x] = True

    while not walls_to_visit.empty():
        current_wall = walls_to_visit.get()

        for addition_y in range(-1, 2):
            for addition_x in range(-1, 2):
                if addition_x == 0 and addition_y == 0:
                    continue
                if addition_x != 0 and addition_y != 0:
                    continue

                adjacent_position = Position(current_wall.x + addition_x, current_wall.y + addition_y) 
                if adjacent_position.y < 0 or adjacent_position.y >= PLANTS_MAP_ROW_SIZE or \
                    adjacent_position.x < 0 or adjacent_position.x >= PLANTS_MAP_COL_SIZE or \
                    plants_map[adjacent_position.y][adjacent_position.x] != '#' or \
                    used_positions[adjacent_position.y][adjacent_position.x]:
                        continue
                
                used_positions[adjacent_position.y][adjacent_position.x] = True
                walls_to_visit.put(adjacent_position)

plant_regions = []

for y, current_plant_line in enumerate(plants_map):
    for x, current_plant_symbol in enumerate(current_plant_line):
        if used_plants_for_region[y][x]:
            continue

        initial_plant_position = Position(x, y) 
        current_plant_region = get_plant_region(initial_plant_position, current_plant_symbol)
        plant_regions.append(current_plant_region)

for current_region in plant_regions:
    print(f'Current plant symbol {plants_map[current_region[0].y][current_region[0].x]} ')
    for current_plant in current_region:
        print(current_plant, end = '')

    print()

total_price = 0
for current_region in plant_regions:
    area = 0
    perimeter = 0
    current_region_symbol = plants_map[current_region[0].y][current_region[0].x]
    positions_visited = set()
    positions_changed = dict()
    # get the changed positions
    # iterate over the changed positions and get the walls 
    # revert the changed positions
    for current_plant_position in current_region:
        area+= 1
        if current_plant_position.y - 1 < 0 and Position(0, -1) not in positions_visited:
            perimeter+=1
            positions_visited.add(Position(0, -1))
        elif current_plant_position.y + 1 == PLANTS_MAP_ROW_SIZE and Position(0, PLANTS_MAP_ROW_SIZE) not in positions_visited:
            perimeter+=1
            positions_visited.add(Position(0, PLANTS_MAP_ROW_SIZE))
        elif current_plant_position.x - 1 < 0 and Position(-1, 0) not in positions_visited:
            perimeter+=1
            positions_visited.add(Position(-1, 0))
        elif current_plant_position.x + 1 == PLANTS_MAP_COL_SIZE and Position(PLANTS_MAP_COL_SIZE, 0) not in positions_visited:
            perimeter+=1
            positions_visited.add(Position(PLANTS_MAP_COL_SIZE, 0))

        # for adjacent_position in [Position(-1, 0), Position(1, 0), Position(0, -1), Position(0, 1)]:
        #     adjacent_plant_block = Position(current_plant_position.x + adjacent_position.x, current_plant_position.y + adjacent_position.y)
        #     if adjacent_plant_block.x > 0 and adjacent_plant_block.x < PLANTS_MAP_COL_SIZE and \
        #         adjacent_plant_block.y > 0 and adjacent_plant_block.y < PLANTS_MAP_ROW_SIZE and \
        #         adjacent_plant_block not in current_region:    
    
    print(f'Symbol: {current_region_symbol}; Area: {area}; Perimeter: {perimeter};')
    total_price += area * perimeter

print(total_price)