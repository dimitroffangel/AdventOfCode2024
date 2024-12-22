import os
import math
import copy

print(os.getcwd())

class PageOrder:
    def __init__(self, lhs_page, rhs_page):
        self.lhs_page = lhs_page
        self.rhs_page = rhs_page

input_file = open('./day5/input.txt', 'r', encoding='utf-8')

page_order_list = []

page_update_list = []

for line in input_file:
    line = line.strip()

    if not line:
        break

    line_split = line.split('|')
    page_order_list.append(PageOrder(int(line_split[0]), int(line_split[1])))


for line in input_file:
    line = [int(page_number) for page_number in line.strip().split(',')]
    page_update_list.append(line)

input_file.close()

def are_pages_in_order(lhs_page, rhs_page):
    for current_page_order in page_order_list:
        if current_page_order.lhs_page == rhs_page and current_page_order.rhs_page == lhs_page:
            return False
        
    return True


def is_update_correct(page_update):
    for page_index, current_page in enumerate(page_update):
        for other_index, current_other_page in enumerate(page_update[page_index + 1:]):
            if current_page == current_other_page:
                continue
            if not are_pages_in_order(current_page, current_other_page):
                return page_index
    return -1

def main():
    average_page_from_correct_page_update = 0
    for current_page_update in page_update_list:
        result = is_update_correct(current_page_update)
        if result == -1:
            continue
        copy_current_page_update = copy.copy(current_page_update)
        while result != -1: 
            offset_index = result + 1
            for page_index, current_page in enumerate(current_page_update[offset_index:]):
                if not are_pages_in_order(current_page_update[result], current_page_update[page_index + offset_index]):
                    current_page_update[result] ^= current_page_update[page_index + offset_index]
                    current_page_update[page_index + offset_index] ^= current_page_update[result]
                    current_page_update[result] ^= current_page_update[page_index + offset_index]
                    update_result = is_update_correct(current_page_update[result:])
                    if update_result != -1:
                        result = update_result + result
                    else:
                        result = update_result
                    break

        average_page_from_correct_page_update = average_page_from_correct_page_update + current_page_update[math.floor(len(copy_current_page_update) / 2)]
    print(average_page_from_correct_page_update)

main()

# current_page_update = [1,2,3]
# permutation_list = [0 for x in current_page_update]
# i = 0
# while i < len(permutation_list):
#     if permutation_list[i] < i:
#         if i % 2 == 0:
#             current_page_update[0] ^= current_page_update[i]
#             current_page_update[i] ^= current_page_update[0]
#             current_page_update[0] ^= current_page_update[i]
#         else:
#             current_page_update[permutation_list[i]] ^= current_page_update[i]
#             current_page_update[i] ^= current_page_update[permutation_list[i]]
#             current_page_update[permutation_list[i]] ^= current_page_update[i]
#         print(current_page_update)
#         permutation_list[i] = permutation_list[i] + 1
#         i = 1
#     else:
#         permutation_list[i] = 0
#         i = i + 1
