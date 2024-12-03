from kivy.uix.label import Label
from numpy.ma.core import append

from utils import data_manager as dm
import re


def extract_mul_expressions(text):
    pattern = r'mul\(([\d,]+)\)'
    matches = re.finditer(pattern, text)
    result = []
    for match in matches:
        numbers = list(map(int, match.group(1).split(',')))
        position = match.span()
        result.append((numbers, position))
    print(result)
    return result


def extract_valid_ranges(data):
    on_pattern = r'don\'t\(\)'
    off_pattern = r'do\(\)'
    on_matches = list(re.finditer(on_pattern, data))
    off_matches = list(re.finditer(off_pattern, data))
    off_matches.append(re.search(r'$', data))
    result = []
    current_on = current_off = last_off = 0

    while current_on < len(on_matches) and current_off < len(off_matches):
        if (off_matches[current_off].start() < on_matches[current_on].start()):
            current_off += 1
        elif (last_off > on_matches[current_on].start()):
            current_on += 1
        else:
            result.append((on_matches[current_on].start(), off_matches[current_off].start()))
            last_off = off_matches[current_off].start()
            current_on += 1
            current_off += 1

    return result


def check_valid(data, multiplication):
    ranges = extract_valid_ranges(data)
    result = []
    for mul in multiplication:
        is_on = True
        for start, end in ranges:
            if start <= mul[1][0] and mul[1][0] <= end:
                is_on = False
                break
        if is_on:
            result.append(mul)
    return result


def handle_day(layout, sample=False):
    data = dm.read_data(3, sample, False)
    answer = ""
    data = "".join(data)

    # * Part one
    p1_sum = 0
    p1_multiplication = extract_mul_expressions(data)
    for item in p1_multiplication:
        if (len(item[0]) == 2):
            p1_sum += item[0][0] * item[0][1]

    answer += f"Part one: {p1_sum}\n"

    # * Part two
    p2_sum = 0
    p2_multiplication = check_valid(data, p1_multiplication)

    for item in p2_multiplication:
        if (len(item[0]) == 2):
            p2_sum += item[0][0] * item[0][1]

    answer += f"Part two: {p2_sum}\n"

    dm.write_data(3, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
