import os
import copy
import sys

print(os.getcwd())

class Calibration:
    def __init__(self, target_value, operands):
        self.target_value = target_value
        self.operands = operands


input_file = open('./day7/example_input.txt', 'r', encoding='utf-8')
calibrations = []

for line in input_file:
    splitted_line = line.split(':')
    operands = splitted_line[1].split(' ')[1:]
    int_operands = [ int(operand.strip()) for operand in operands]
    calibrations.append(Calibration(int(splitted_line[0]), int_operands))

def concantenate_numbers(lhs_number, rhs_number):
    if rhs_number == 0:
        return lhs_number * 10

    x = lhs_number
    a = rhs_number

    reversed_rhs_number = 0
    number_of_final_zeroes = 0
    is_divisible_by_zero = rhs_number % 10 == 0
    while rhs_number != 0:
        reversed_rhs_number = reversed_rhs_number * 10 + rhs_number % 10
        is_divisible_by_zero = is_divisible_by_zero and rhs_number % 10 == 0
        if is_divisible_by_zero:
            number_of_final_zeroes = number_of_final_zeroes + int(rhs_number % 10 == 0)
        rhs_number = rhs_number // 10

    b = reversed_rhs_number

    while reversed_rhs_number != 0:
        lhs_number = lhs_number * 10 + reversed_rhs_number % 10
        reversed_rhs_number = reversed_rhs_number // 10

    lhs_number = lhs_number * pow(10, number_of_final_zeroes)

    return lhs_number


def is_target_value_reachable(target_value, operands, result):
    if result > target_value:
        return False
    if not operands and target_value == result:
        return True
    elif not operands:
        return False
    
    if result <= 0 or operands[0] <= 0:
        print(f'{operands[0]} something is wrong')

    return is_target_value_reachable(target_value, operands[1:], result * operands[0]) or \
          is_target_value_reachable(target_value, operands[1:], result + operands[0]) or \
          is_target_value_reachable(target_value, operands[1:], concantenate_numbers(result, operands[0]))

sum_of_calibration_targets = 0
count = 0

for calibration in calibrations:
    if is_target_value_reachable(calibration.target_value, calibration.operands[1:], calibration.operands[0]):
        # print(f'{calibration.target_value} is reachable')
        sum_of_calibration_targets = sum_of_calibration_targets + calibration.target_value
        count = count + 1
        if sum_of_calibration_targets < 0:
            print('Overflow')
            break

print(sum_of_calibration_targets)
print(count)

# print(concantenate_numbers(105, 206))