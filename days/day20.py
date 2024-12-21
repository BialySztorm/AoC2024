from kivy.uix.label import Label
from collections import deque, defaultdict

from utils import data_manager as dm

def find_path(grid, start, end):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        if current == end:
            return path


        for direction in directions:
            new_row, new_col = current[0] + direction[0], current[1] + direction[1]
            neighbor = (new_row, new_col)

            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] != '#' and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

def use_cheats(path, cheats, limit):
    results = defaultdict(int)
    for i in range(len(path) - 2):
        s = path[i]
        for j in range(i + 2, len(path)):
            e = path[j]
            distance = abs(s[0] - e[0]) + abs(s[1] - e[1])
            if distance <= cheats:
                gain = j - i - distance
                if gain >= limit:
                    results[gain] += 1
    return sum(results.values())

def handle_day(layout, sample=False):
    data = [list(row) for row in dm.read_data(20, sample, False)]
    answer = ""

    # * Part one and two
    start = (0, 0)
    end = (0, 0)
    for i in range(len(data)):
        for j  in range(len(data[i])):
            if data[i][j] == "S":
                start = (i,j)
            elif data[i][j] == "E":
                end = (i,j)
            if start != (0,0) and end != (0,0):
                break
        if start != (0,0) and end != (0,0):
            break

    path = find_path(data, start, end)
    limit = 30 if sample else 100
    result = use_cheats(path, 2, limit)
    answer += f"Part one: {result}\n"

    # * Part two
    limit = 50 if sample else 100
    result = use_cheats(path, 20, limit)

    answer += f"Part two: {result}\n"

    dm.write_data(20, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




