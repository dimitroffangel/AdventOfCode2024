import os
import copy
from enum import Enum
import queue

print(os.getcwd())

input_file = open('./day11/example_input.txt', 'r', encoding='utf-8')

stone_numbers = []

stone_numbers = list(map(int, input_file.readline().strip().split(' ')))

print(stone_numbers)

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

for i in range(NUMBER_OF_ITERATIONS):
    stone_next_generation = []
    for stone_number in stone_numbers:
        if stone_number == 0:
            stone_next_generation.append(1)
            continue
        
        lhs_number, rhs_number = try_splitting_number(stone_number)
        if rhs_number is None:
            stone_next_generation.append(stone_number * STONE_MULTIPLIER)
        else:
            stone_next_generation.append(lhs_number)
            stone_next_generation.append(rhs_number)
        # elif number_of_digits(stone_number) % 2 == 0:
        #     lhs_number, rhs_number = split_number(stone_number)
        #     stone_next_generation.append(lhs_number)
        #     stone_next_generation.append(rhs_number)
        # else:
        #     stone_next_generation.append(stone_number * STONE_MULTIPLIER)
    stone_numbers = stone_next_generation

print(stone_next_generation)
print(len(stone_next_generation))