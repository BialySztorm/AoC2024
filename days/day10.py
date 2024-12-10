from kivy.uix.label import Label

from utils import data_manager as dm


def find_starting_pos(data):
    pos = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "0":
                pos.append((x, y))
    return pos


def find_trail(data, pos, current_height=0):
    x, y = pos
    trail_ends = []
    if (current_height == 9):
        return [(x, y)]
    if (x - 1 >= 0 and data[y][x - 1] == str(current_height + 1)):
        trail_ends.extend(find_trail(data, (x - 1, y), current_height + 1))
    if (x + 1 < len(data[y]) and data[y][x + 1] == str(current_height + 1)):
        trail_ends.extend(find_trail(data, (x + 1, y), current_height + 1))
    if (y - 1 >= 0 and data[y - 1][x] == str(current_height + 1)):
        trail_ends.extend(find_trail(data, (x, y - 1), current_height + 1))
    if (y + 1 < len(data) and data[y + 1][x] == str(current_height + 1)):
        trail_ends.extend(find_trail(data, (x, y + 1), current_height + 1))
    return trail_ends


def remove_duplcates(trails):
    for i in range(len(trails)):
        for j in range(i + 1, len(trails)):
            if trails[i] == trails[j]:
                trails.pop(j)
                return remove_duplcates(trails)
    return trails


def handle_day(layout, sample=False):
    data = [list(row) for row in dm.read_data(10, sample, False)]
    answer = ""

    # * Part one and two
    starting_pos = find_starting_pos(data)
    trails = 0
    trails_score = 0
    for pos in starting_pos:
        trails_ends = find_trail(data, pos)
        trails_score += len(trails_ends)
        trails += len(remove_duplcates(trails_ends))

    answer += f"Part one: {trails}\n"
    answer += f"Part two: {trails_score}\n"

    dm.write_data(10, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
