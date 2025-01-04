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

class StoneCache:
    def __init__(self, number, rhs_list):
        self.number = number
        self.rhs_list = rhs_list

input_file = open('./day11/example_input.txt', 'r', encoding='utf-8')

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

NUMBER_OF_ITERATIONS = 25
STONE_MULTIPLIER = 2024

cached_result_after_iterations = {}

for stone in stone_numbers:
    initial_stone_number = stone.number
    if stone.generation >= NUMBER_OF_ITERATIONS:
        continue

    if stone.number in cached_result_after_iterations:
        # you have already iterated those generation, add the rhs stones and change the value to the generation that is remaining
        size_of_cached_result = len(cached_result_after_iterations[stone.number])
        iterate_until = NUMBER_OF_ITERATIONS - stone.generation \
            if size_of_cached_result >= NUMBER_OF_ITERATIONS - stone.generation \
            else size_of_cached_result
        stone_value_before_change = stone.number
        for previous_generation_index, previous_stone_number_generation in enumerate(cached_result_after_iterations[stone_value_before_change][:iterate_until]):
            if len(previous_stone_number_generation) > 1:
                stone_numbers.append(Stone(previous_stone_number_generation[1], stone.generation + 1))
            stone.number = previous_stone_number_generation[0]
            stone.generation += 1

    else:
        cached_result_after_iterations[stone.number] = []    
        print(f'Currently {len(stone_numbers)}')
    
    for current_generation in range(NUMBER_OF_ITERATIONS - stone.generation):
        if stone.number == 0:
            stone.number = 1
            cached_result_after_iterations[initial_stone_number].append([1])
            continue

        lhs, rhs = try_splitting_number(stone.number)
        if rhs is None:
            stone.number *= STONE_MULTIPLIER
            cached_result_after_iterations[initial_stone_number].append([stone.number])
        else:
            stone.number = lhs
            stone_numbers.append(Stone(rhs, stone.generation + current_generation + 1))
            cached_result_after_iterations[initial_stone_number].append([lhs, rhs])

        # number_of_digits_stone = number_of_digits(stone.number)
        # if number_of_digits_stone % 2 == 0:
        #     lhs_number, rhs_number = split_number(stone.number, number_of_digits_stone)
        #     stone.number = lhs_number
        #     stone_numbers.append(Stone(rhs_number, stone.generation + current_generation + 1))
        #     cached_result_after_iterations[initial_stone_number].append([lhs_number, rhs_number])

        # else:
        #     stone.number = stone.number * STONE_MULTIPLIER
        #     cached_result_after_iterations[initial_stone_number].append([stone.number])
    
    stone.generation = NUMBER_OF_ITERATIONS


print(stone_numbers)
print(len(stone_numbers))