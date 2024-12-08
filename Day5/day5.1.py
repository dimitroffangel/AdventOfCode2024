import os
import math
import statistics

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

average_page_from_correct_page_update = 0
for current_page_update in page_update_list:
    is_order_correct = True
    for page_index, current_page in enumerate(current_page_update):
        for current_other_page in current_page_update[page_index + 1:]:
            if current_page == current_other_page:
                continue

            if not are_pages_in_order(current_page, current_other_page):
                is_order_correct = False
                break
        if not is_order_correct:
            break
    if is_order_correct:
        average_page_from_correct_page_update = average_page_from_correct_page_update + current_page_update[math.floor(len(current_page_update) / 2)]

print(average_page_from_correct_page_update)
