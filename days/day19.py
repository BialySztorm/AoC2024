from kivy.uix.label import Label

from utils import data_manager as dm

def check_possibilities(patterns, design):
    memo = {}

    def can_build(tmp_design):
        sum = 0
        if tmp_design in memo:
            return memo[tmp_design]
        if not tmp_design:
            return 1

        for pattern in patterns:
            if tmp_design.startswith(pattern):
                sum += can_build(tmp_design[len(pattern):])

        memo[tmp_design] = sum
        return sum

    return can_build(design)

def handle_day(layout, sample=False):
    data = dm.split_array_at_empty(dm.read_data(19, sample, False))
    answer = ""

    patterns = data[0][0].split(", ")
    designs = data[1]

    # * Part one and two
    sum_p1 = 0
    sum_p2 = 0
    for design in designs:
        tmp = check_possibilities(patterns, design)
        if tmp:
            sum_p1 += 1
        sum_p2 += tmp

    answer += f"Part one: {sum_p1}\n"
    answer += f"Part two: {sum_p2}"

    dm.write_data(19, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




