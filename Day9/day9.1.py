import os
import copy
from enum import Enum
import queue

print(os.getcwd())

input_file = open('./day9/input.txt', 'r', encoding='utf-8')

FREE_SPACE_CODE = -1

current_id = 0
is_reading_file_block = True
disk_space = []
disk_information = input_file.readline().strip()
free_spaces = queue.Queue()
file_locations = []

for digit in disk_information:
    if is_reading_file_block:
        for i in range(int(digit)):
            file_locations.append(len(disk_space))
            disk_space.append(current_id)
        
        current_id = current_id + 1
    else:
        for i in range(int(digit)):
            free_spaces.put(len(disk_space))
            disk_space.append(FREE_SPACE_CODE)

    is_reading_file_block = not is_reading_file_block
    
input_file.close()

print(disk_space)

def swap_locations(lhs_index, rhs_index):
    disk_space[lhs_index] ^= disk_space[rhs_index]
    disk_space[rhs_index] ^= disk_space[lhs_index]
    disk_space[lhs_index] ^= disk_space[rhs_index]


while file_locations:
    current_file_location = file_locations.pop()
    current_free_space_location = free_spaces.get()

    if current_free_space_location >= current_file_location:
        break

    free_spaces.put(current_file_location)

    swap_locations(current_file_location, current_free_space_location)

print(disk_space)

disk_space_assessment = 0
for i, value in enumerate(disk_space):
    if value == -1:
        break
    
    disk_space_assessment = disk_space_assessment + value * i

print(disk_space_assessment)
