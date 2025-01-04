import os
import copy
from enum import Enum
import queue

print(os.getcwd())

input_file = open('./day11/input.txt', 'r', encoding='utf-8')

stone_numbers = []

stone_numbers = list(map(int, input_file.readline().strip().split(' ')))

print(stone_numbers)

def number_of_digits(number):
    number_of_digits = 0
    while number > 0:
        number = number // 10
        number_of_digits = number_of_digits + 1
    return number_of_digits

def combine_list_digits_to_number(digits):
    number = 0
    for digit in digits:
        number = number * 10 + digit
    return number

def split_number(number):
    digits = []
    while number > 0:
        digits.append(number % 10)
        number = number // 10
    number_of_digits = len(digits)
    lhs_digits = digits[(number_of_digits // 2):]
    rhs_digits = digits[:(number_of_digits // 2)]
    lhs_digits.reverse()
    rhs_digits.reverse()
    return combine_list_digits_to_number(lhs_digits), combine_list_digits_to_number(rhs_digits)

NUMBER_OF_ITERATIONS = 25
STONE_MULTIPLIER = 2024

for i in range(NUMBER_OF_ITERATIONS):
    stone_next_generation = []
    for stone_number in stone_numbers:
        if stone_number == 0:
            stone_next_generation.append(1)
        elif number_of_digits(stone_number) % 2 == 0:
            lhs_number, rhs_number = split_number(stone_number)
            stone_next_generation.append(lhs_number)
            stone_next_generation.append(rhs_number)
        else:
            stone_next_generation.append(stone_number * STONE_MULTIPLIER)
    stone_numbers = stone_next_generation

print(stone_next_generation)
print(len(stone_next_generation))