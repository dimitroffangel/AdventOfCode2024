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
    
class Region:
    def __init__(self):
        self.plants = []
        self.number_of_sides = 0

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
    area = len(current_region)
    current_region_symbol = plants_map[current_region[0].y][current_region[0].x]
    
    print(f'Symbol: {current_region_symbol}; Area: {area}; Number of sides: {current_region.number_of_sides};')
    total_price += area * current_region.number_of_sides

print(total_price)