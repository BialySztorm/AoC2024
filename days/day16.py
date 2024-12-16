from kivy.uix.label import Label
import heapq

from days.day14 import print_maps
from utils import data_manager as dm

def find_cheapest_path(data, start, end):
    rows, cols = len(data), len(data[0])
    pq = [(0, start[0], start[1], 1, 0)]
    visited = set()

    while pq:
        cost, x, y, dx, dy = heapq.heappop(pq)
        if (x, y) == end:
            return cost
        if (x, y, dx, dy) in visited:
            continue
        visited.add((x, y, dx, dy))

        for new_dx, new_dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + new_dx, y + new_dy
            if 0 <= new_x < cols and 0 <= new_y < rows and data[new_y][new_x] != '#':
                new_cost = cost + 1 + (1000 if (new_dx, new_dy) != (dx, dy) else 0)
                heapq.heappush(pq, (new_cost, new_x, new_y, new_dx, new_dy))

    return float('inf')


def find_all_cheapest_paths(data, start, end, min_cost):
    rows, cols = len(data), len(data[0])
    pq = [(0, start[0], start[1], 1, 0, [(start[0], start[1])])]  # (cost, x, y, dx, dy, path)
    paths = []
    min_cost_dict = {(start[0], start[1], 1, 0): 0}

    while pq:
        cost, x, y, dx, dy, path = heapq.heappop(pq)

        if (x, y) == end and cost == min_cost:
            paths.append(path)
            continue

        if cost > min_cost:
            continue

        for new_dx, new_dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + new_dx, y + new_dy

            if 0 <= new_y < rows and 0 <= new_x < cols and data[new_y][new_x] != '#' and (new_x, new_y) not in path:
                new_cost = cost + 1 + (1000 if (new_dx, new_dy) != (dx, dy) else 0)
                if new_cost <= min_cost and new_cost <= min_cost_dict.get((new_x, new_y, new_dx, new_dy), float('inf')):
                    min_cost_dict[(new_x, new_y, new_dx, new_dy)] = new_cost
                    heapq.heappush(pq, (new_cost, new_x, new_y, new_dx, new_dy, path + [(new_x, new_y)]))

    for path in paths:
        for x, y in path:
            data[y][x] = "O"

    for row in data:
        print("\t".join(row))



def handle_day(layout, sample=False):
    data = [list(row) for row in dm.read_data(16, sample, False)]
    answer = ""

    # * Part one
    for i in range(len(data)):
        for j, cell in enumerate(data[i]):
            if cell == "E":
                end = (j,i)
            elif cell == "S":
                start = (j,i)
                break
    cheapest_path = find_cheapest_path(data, start, end)
    answer += f"Part one: {cheapest_path}\n"

    # * Part two
    find_all_cheapest_paths(data, start, end, cheapest_path)

    sum = 0
    for row in data:
        for cell in row:
            if cell == "O":
                sum += 1

    answer += f"Part two: {sum}\n"

    dm.write_data(16, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




