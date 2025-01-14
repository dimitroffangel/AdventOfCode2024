import os
import copy
from enum import Enum
import queue

print(os.getcwd())

class Stone:
    def __init__(self, number, generation):
        self.number = number
        self.generation = generation
    def __repr__(self):
        return f'Number: {self.number}, Generation: {self.generation}'

NOT_ITERATED_STONE_GENERATION_INDEX = 0

class StoneCache:
    def __init__(self, lhs_list, rhs_list, number_of_max_generations):
        self.lhs_list = lhs_list
        self.rhs_list = rhs_list
        self.cache_stones_result = [NOT_ITERATED_STONE_GENERATION_INDEX for _ in range(number_of_max_generations)]

input_file = open('./day11/input.txt', 'r', encoding='utf-8')

stone_numbers = []

stone_numbers = [Stone(number, 0) for number in list(map(int, input_file.readline().strip().split(' ')))]

print(stone_numbers)

def number_of_digits(number):
    number_of_digits = 0
    while number > 0:
        number = number // 10
        number_of_digits = number_of_digits + 1
    return number_of_digits

def combine_list_digits_to_number(digits):
    number = 0
    for digit_place_index, digit in enumerate(digits):
        number = number + digit * (10 ** digit_place_index)
    return number

def split_number(number, number_of_digits):
    digits = []
    while number > 0:
        digits.append(number % 10)
        number = number // 10
    lhs_digits = digits[(number_of_digits // 2):]
    rhs_digits = digits[:(number_of_digits // 2)]
    return combine_list_digits_to_number(lhs_digits), combine_list_digits_to_number(rhs_digits)

def try_splitting_number(number):
    digits = []
    while number > 0:
        digits.append(number % 10)
        number = number // 10
    number_of_digits_on_stone = len(digits)
    if number_of_digits_on_stone % 2 == 0:      
        lhs_digits = digits[(number_of_digits_on_stone // 2):]
        rhs_digits = digits[:(number_of_digits_on_stone // 2)]
        return combine_list_digits_to_number(lhs_digits), combine_list_digits_to_number(rhs_digits)
    else:
        return 0, None

NUMBER_OF_ITERATIONS = 75
STONE_MULTIPLIER = 2024

cached_result_after_iterations = {}

def mutate_stone(stone):
    if stone.generation == NUMBER_OF_ITERATIONS:
        return 1
    
    if cached_result_after_iterations[stone.number].cache_stones_result[stone.generation] != NOT_ITERATED_STONE_GENERATION_INDEX:
        return cached_result_after_iterations[stone.number].cache_stones_result[stone.generation]
    
    if stone.number == 0:
        if 1 not in cached_result_after_iterations:
            cached_result_after_iterations[1] = StoneCache([], [], NUMBER_OF_ITERATIONS) 

        stone_children = mutate_stone(Stone(1, stone.generation + 1))
        cached_result_after_iterations[stone.number].cache_stones_result[stone.generation] = stone_children
        return stone_children
    
    lhs, rhs = try_splitting_number(stone.number)
    if rhs is None:
        child_value = stone.number * STONE_MULTIPLIER
        if child_value not in cached_result_after_iterations:
            cached_result_after_iterations[child_value] = StoneCache([], [], NUMBER_OF_ITERATIONS)

        stone_children = mutate_stone(Stone(child_value, stone.generation + 1))
        cached_result_after_iterations[stone.number].cache_stones_result[stone.generation] = stone_children 
        return stone_children
        
    if lhs not in cached_result_after_iterations:
        cached_result_after_iterations[lhs] = StoneCache([], [], NUMBER_OF_ITERATIONS)
    if rhs not in cached_result_after_iterations:
        cached_result_after_iterations[rhs] = StoneCache([], [], NUMBER_OF_ITERATIONS)
        
    lhs_stone_children = mutate_stone(Stone(lhs, stone.generation + 1))
    rhs_stone_children = mutate_stone(Stone(rhs, stone.generation + 1))

    cached_result_after_iterations[stone.number].cache_stones_result[stone.generation] = lhs_stone_children + rhs_stone_children
    return lhs_stone_children + rhs_stone_children

result = 0
for current_stone in stone_numbers:
    if current_stone.number not in cached_result_after_iterations:
        cached_result_after_iterations[current_stone.number] = StoneCache([], [], NUMBER_OF_ITERATIONS)

    result += mutate_stone(current_stone)

print(result)


# for stone in stone_numbers:
#     initial_stone_number = stone.number
#     if stone.generation == NUMBER_OF_ITERATIONS:
#         continue

#     if stone.number in cached_result_after_iterations:
#         # you have already iterated those generation, add the rhs stones and change the value to the generation that is remaining
#         size_of_cached_result = len(cached_result_after_iterations[stone.number].lhs_list)

#         # everything is already calculated, just get it
#         if size_of_cached_result >= NUMBER_OF_ITERATIONS - stone.generation:
#             lhs_index_taken = NUMBER_OF_ITERATIONS - stone.generation - 1
#             for rhs_stone in cached_result_after_iterations[stone.number].rhs_list:
#                 if rhs_stone.generation > lhs_index_taken + 1:
#                     break

#                 stone_numbers.append(Stone(rhs_stone.number, rhs_stone.generation + stone.generation))

#             stone.number = cached_result_after_iterations[stone.number].lhs_list[lhs_index_taken]
#             stone.generation = NUMBER_OF_ITERATIONS

#         else:
#             for rhs_stone in cached_result_after_iterations[stone.number].rhs_list:
#                 stone_numbers.append(Stone(rhs_stone.number, rhs_stone.generation + stone.generation))

#             stone.number = cached_result_after_iterations[stone.number].lhs_list[size_of_cached_result - 1]
#             stone.generation += size_of_cached_result

#     else:
#         cached_result_after_iterations[stone.number] = StoneCache([], [])
    
#     for current_generation in range(NUMBER_OF_ITERATIONS - stone.generation):
#         if stone.number == 0:
#             stone.number = 1
#             cached_result_after_iterations[initial_stone_number].lhs_list.append(1)
#             continue

#         lhs, rhs = try_splitting_number(stone.number)
#         if rhs is None:
#             stone.number *= STONE_MULTIPLIER
#             cached_result_after_iterations[initial_stone_number].lhs_list.append(stone.number)
#         else:
#             stone.number = lhs
#             stone_numbers.append(Stone(rhs, stone.generation + current_generation + 1))
#             cached_result_after_iterations[initial_stone_number].lhs_list.append(lhs)
#             len_foo = len(cached_result_after_iterations[initial_stone_number].lhs_list)
#             cached_result_after_iterations[initial_stone_number].rhs_list.append(Stone(rhs, len_foo))
    
#     stone.generation = NUMBER_OF_ITERATIONS

# print(stone_numbers)
# print(len(stone_numbers))