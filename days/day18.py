from kivy.uix.label import Label

from utils import data_manager as dm


def drop_bytes(data, sample):
    if (sample):
        grid_size = 7
        bytes_amount = 12
    else:
        grid_size = 71
        bytes_amount = 1024

    grid = [['.' for i in range(grid_size)] for j in range(grid_size)]
    for i in range(min(len(data), bytes_amount)):
        grid[int(data[i][1])][int(data[i][0])] = '#'

    return grid, bytes_amount

def drop_byte(byte, grid):
    grid[int(byte[1])][int(byte[0])] = '#'
    return grid

from collections import deque


def find_path(map):
    # Znajdź współrzędne startu (0, 0) i celu (end_loc)
    rows = len(map)
    cols = len(map[0])
    start_loc = (0, 0)
    end_loc = (rows - 1, cols - 1)

    # Kierunki poruszania się: góra, dół, lewo, prawo
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Kolejka BFS i zbiór odwiedzonych węzłów
    queue = deque([(start_loc, [start_loc])])  # (bieżąca pozycja, ścieżka)
    visited = set([start_loc])

    while queue:
        (current, path) = queue.popleft()

        # Jeśli dotarliśmy do celu, zwróć ścieżkę
        if current == end_loc:
            return path

        # Przeglądaj sąsiadów
        for direction in directions:
            new_row = current[0] + direction[0]
            new_col = current[1] + direction[1]
            neighbor = (new_row, new_col)

            # Sprawdź, czy sąsiad jest w granicach mapy i nie jest przeszkodą
            if (0 <= new_row < rows and 0 <= new_col < cols and
                    map[new_row][new_col] != '#' and neighbor not in visited):
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    # Jeśli brak ścieżki, zwróć None
    return None


def handle_day(layout, sample=False):
    data = dm.read_data(18, sample, splitter=",")
    answer = ""

    # * Part one
    grid, iter = drop_bytes(data, sample)
    path = find_path(grid)

    answer += f"Part one: {len(path) - 1}\n"

    # * Part two
    while find_path(grid) is not None and iter < len(data):
        iter += 1
        grid = drop_byte(data[iter], grid)

    answer += f"Part two: {data[iter][0]},{data[iter][1]}"

    dm.write_data(18, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))
