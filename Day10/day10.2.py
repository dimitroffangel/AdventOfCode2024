import os
import copy
from enum import Enum
import queue

print(os.getcwd())

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VertexInformation:
    def __init__(self, number_of_paths, is_used):
        self.number_of_paths = number_of_paths
        self.is_used = is_used

input_file = open('./day10/input.txt', 'r', encoding='utf-8')

STARTING_POSITION = 0
FINISH_POSITION = 9

map = []
used_map = []
vertices_to_iterate = queue.Queue()
starting_positions = []

for row, line in enumerate(input_file):
    map.append([])
    used_map.append([])
    for column, height_symbol in enumerate(line.strip()):
        height = ord(height_symbol) - ord('0')
        map[row].append(height)
        used_map[row].append(VertexInformation(0, False))
        
        if height == STARTING_POSITION:
            starting_positions.append(Position(column, row))

MAP_ROW_SIZE = len(map)
MAP_COL_SIZE = len(map[0])

def check_adjacent_position(adjacent_position, current_vertex, initial_position):
    if adjacent_position.x < 0 or adjacent_position.x >= MAP_COL_SIZE or adjacent_position.y < 0 or adjacent_position.y >= MAP_ROW_SIZE:
        return

    if map[current_vertex.y][current_vertex.x] + 1 == map[adjacent_position.y][adjacent_position.x]:
        vertices_to_iterate.put(adjacent_position)

        if map[adjacent_position.y][adjacent_position.x] == FINISH_POSITION:
            used_map[initial_position.y][initial_position.x].number_of_paths = used_map[initial_position.y][initial_position.x].number_of_paths + 1

def BFS(initial_position):
    vertices_to_iterate.put(initial_position)
    used_map[initial_position.y][initial_position.x].is_used = True

    while not vertices_to_iterate.empty():
        current_vertex = vertices_to_iterate.get()

        up_position = Position(current_vertex.x, current_vertex.y - 1)
        right_position = Position(current_vertex.x + 1, current_vertex.y)
        down_position = Position(current_vertex.x, current_vertex.y + 1)
        left_position = Position(current_vertex.x - 1, current_vertex.y)

        check_adjacent_position(up_position, current_vertex, initial_position)
        check_adjacent_position(right_position, current_vertex, initial_position)
        check_adjacent_position(down_position, current_vertex, initial_position)
        check_adjacent_position(left_position, current_vertex, initial_position) 




number_of_paths_found = 0

for starting_position in starting_positions:
    BFS(starting_position)
    print(used_map[starting_position.y][starting_position.x].number_of_paths)
    number_of_paths_found = number_of_paths_found + used_map[starting_position.y][starting_position.x].number_of_paths

print(number_of_paths_found)