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

NUMBER_OF_ITERATIONS = 25
STONE_MULTIPLIER = 2024

cached_result_after_iterations = {}

for stone in stone_numbers:
    # print(stone)
    initial_stone_number = stone.number
    if stone.generation >= NUMBER_OF_ITERATIONS:
        continue

    for current_generation in range(NUMBER_OF_ITERATIONS - stone.generation):        
        if stone.number == 0:
            stone.number = 1
            continue

        number_of_digits_stone = number_of_digits(stone.number)
        if number_of_digits_stone % 2 == 0:
            lhs_number, rhs_number = split_number(stone.number, number_of_digits_stone)
            stone.number = lhs_number
            stone_numbers.append(Stone(rhs_number, stone.generation + current_generation + 1))
            
        else:
            stone.number = stone.number * STONE_MULTIPLIER
    
    stone.generation = NUMBER_OF_ITERATIONS



print(stone_numbers)
print(len(stone_numbers))