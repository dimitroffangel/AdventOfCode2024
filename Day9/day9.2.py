import os
import copy
from enum import Enum
import queue

print(os.getcwd())

class Interval:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.distance = end - begin + 1

input_file = open('./day9/input.txt', 'r', encoding='utf-8')

FREE_SPACE_CODE = -1

current_id = 0
is_reading_file_block = True
disk_space = []
disk_information = input_file.readline().strip()
free_spaces = []
file_locations = []

for digit in disk_information:
    if is_reading_file_block:
        begin_id = len(disk_space)
        for i in range(int(digit)):
            disk_space.append(current_id)
        end_id = len(disk_space) - 1
        file_locations.append(Interval(begin_id, end_id))
        current_id = current_id + 1
    else:
        begin_free_id = len(disk_space)
        for i in range(int(digit)):
            disk_space.append(FREE_SPACE_CODE)
        end_free_id = len(disk_space) - 1
        free_spaces.append(Interval(begin_free_id, end_free_id))

    is_reading_file_block = not is_reading_file_block
    
input_file.close()

print(disk_space)

def swap_locations(lhs_index, rhs_index):
    disk_space[lhs_index] ^= disk_space[rhs_index]
    disk_space[rhs_index] ^= disk_space[lhs_index]
    disk_space[lhs_index] ^= disk_space[rhs_index]


while file_locations:
    current_file_location = file_locations.pop()
    best_free_space_found = None
    best_free_index = -1

    for current_free_space_index, current_free_space in enumerate(free_spaces):
        if current_free_space.distance >= current_file_location.distance and current_file_location.begin > current_free_space.begin:
                best_free_space_found = current_free_space
                best_free_index = current_free_space_index
                break

    if best_free_space_found is None:
        continue

    for i in range(current_file_location.distance):
        swap_locations(current_file_location.begin + i, best_free_space_found.begin + i)
    
    free_spaces[best_free_index].distance = free_spaces[best_free_index].distance - current_file_location.distance
    if free_spaces[best_free_index].distance == 0:
        del free_spaces[best_free_index]
    else:
        free_spaces[best_free_index].begin = free_spaces[best_free_index].begin + current_file_location.distance


print(disk_space)

disk_space_assessment = 0
for i, value in enumerate(disk_space):
    if value == -1:
        continue
    
    disk_space_assessment = disk_space_assessment + value * i

print(disk_space_assessment)
