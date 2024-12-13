from kivy.uix.label import Label
import re
from utils import data_manager as dm


def process_data(data):
    tmp_data = []
    a_pattern = r"Button A: X\+(\d+), Y\+(\d+)"
    b_pattern = r"Button B: X\+(\d+), Y\+(\d+)"
    prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
    i = 0
    while i < len(data) - 2:
        a_match = re.match(a_pattern, data[i])
        b_match = re.match(b_pattern, data[i + 1])
        prize_match = re.match(prize_pattern, data[i + 2])
        result = {
            "a": {"x": int(a_match.group(1)), "y": int(a_match.group(2))},
            "b": {"x": int(b_match.group(1)), "y": int(b_match.group(2))},
            "prize": {"x": int(prize_match.group(1)), "y": int(prize_match.group(2))}
        }
        tmp_data.append(result)
        i += 4

    return tmp_data

def find_path_cost(machine, unit_conversion = False):
    if(unit_conversion):
        machine['prize']['x'] = 10000000000000 + machine['prize']['x']
        machine['prize']['y'] = 10000000000000 + machine['prize']['y']
    times_b = (machine['prize']['y'] * machine['a']['x'] - machine['prize']['x'] * machine['a']['y']) / (machine['b']['y'] *  machine['a']['x'] - machine['b']['x'] * machine['a']['y'])
    times_a = (machine['prize']['x'] - machine['b']['x'] * times_b) / machine['a']['x']

    if times_a.is_integer() and times_b.is_integer():
        if(unit_conversion or 100 >= times_a >= 0 and 100 >= times_b >= 0):
            return int(times_a) * 3 + int(times_b)

def handle_day(layout, sample=False):
    data = dm.read_data(13, sample, False)
    answer = ""
    data = process_data(data)

    # * Part one
    coins = 0
    for machine in data:
        cost = find_path_cost(machine)
        if cost:
            coins += cost
    print(coins)
    answer += f"Part one: {coins}\n"

    # * Part two
    coins = 0
    for machine in data:
        cost = find_path_cost(machine, True)
        if cost:
            coins += cost
    print(coins)
    answer += f"Part two: {coins}"

    dm.write_data(13, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
