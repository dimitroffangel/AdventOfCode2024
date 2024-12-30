import os
import copy

print(os.getcwd())

class Calibration:
    def __init__(self, target_value, operands):
        self.target_value = target_value
        self.operands = operands


input_file = open('./day7/input.txt', 'r', encoding='utf-8')
calibrations = []

for line in input_file:
    splitted_line = line.split(':')
    operands = splitted_line[1].split(' ')[1:]
    int_operands = [ int(operand.strip()) for operand in operands]
    calibrations.append(Calibration(int(splitted_line[0]), int_operands))

def is_target_value_reachable(target_value, operands, result):
    if not operands and target_value == result:
        return True
    elif not operands:
        return False
    
    return is_target_value_reachable(target_value, operands[1:], result * operands[0]) or is_target_value_reachable(target_value, operands[1:], result + operands[0])

sum_of_calibration_targets = 0

for calibration in calibrations:
    if is_target_value_reachable(calibration.target_value, calibration.operands[1:], calibration.operands[0]):
        print(f'{calibration.target_value} is reachable')
        sum_of_calibration_targets = sum_of_calibration_targets + calibration.target_value

print(sum_of_calibration_targets)