from kivy.uix.label import Label
from collections import deque

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

def handle_day(layout, sample=False):
    data = [list(row) for row in dm.read_data(20, sample, False)]
    answer = ""

    # * Part one and two
    start = (0, 0)
    end = (0, 0)
    walls = []
    for i in range(len(data)):
        for j  in range(len(data[i])):
            if data[i][j] == "S":
                start = (i,j)
            elif data[i][j] == "E":
                end = (i,j)
            elif data[i][j] == "#":
                paths_around_count = 0
                paths_around = [(0,1), (1,0), (0,-1), (-1,0)]
                for path in paths_around:
                    if 0 <= i + path[1] < len(data) and 0 <= j + path[0] < len(data[i]):
                        if data[i + path[1]][j + path[0]] == "." or data[i + path[1]][j + path[0]] == "S" or data[i + path[1]][j + path[0]] == "E":
                            paths_around_count += 1
                if paths_around_count >=2:
                    walls.append((i,j))

    normal_path_size = len(find_path(data, start, end)) - 1
    count = 0
    if sample:
        limit = 30
    else:
        limit = 100
    for wall in walls:
        data[wall[0]][wall[1]] = "."
        tmp = len(find_path(data, start, end)) - 1
        if normal_path_size - tmp >= limit:
            count += 1
        data[wall[0]][wall[1]] = "#"
    answer += f"Part one: {count}\n"

    dm.write_data(20, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




