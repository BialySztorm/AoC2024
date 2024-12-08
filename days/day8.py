from kivy.uix.label import Label

from utils import data_manager as dm

def calculate_distance(node1, node2):
    return abs(node1[0] - node2[0]), abs(node1[1] - node2[1])

def create_antinode(node1, node2):
    distance = calculate_distance(node1, node2)
    antinode1 = (node1[0] - distance[0] if node1[0] < node2[0] else node1[0] + distance[0],
                 node1[1] - distance[1] if node1[1] < node2[1] else node1[1] + distance[1])
    antinode2 = (node2[0] + distance[0] if node2[0] > node1[0] else node2[0] - distance[0],
                 node2[1] + distance[1] if node2[1] > node1[1] else node2[1] - distance[1])
    return antinode1, antinode2

def create_antinodes(node1, node2, width, height):
    distance = calculate_distance(node1, node2)
    antinodes = []

    i = 1
    while True:
        antinode1 = (node1[0] - i * distance[0] if node1[0] < node2[0] else node1[0] + i * distance[0],
                     node1[1] - i * distance[1] if node1[1] < node2[1] else node1[1] + i * distance[1])
        antinode2 = (node2[0] + i * distance[0] if node2[0] > node1[0] else node2[0] - i * distance[0],
                     node2[1] + i * distance[1] if node2[1] > node1[1] else node2[1] - i * distance[1])

        if not (0 <= antinode1[0] < height and 0 <= antinode1[1] < width) and not (0 <= antinode2[0] < height and 0 <= antinode2[1] < width):
            break

        if 0 <= antinode1[0] < height and 0 <= antinode1[1] < width:
            antinodes.append(antinode1)
        if 0 <= antinode2[0] < height and 0 <= antinode2[1] < width:
            antinodes.append(antinode2)

        i += 1

    return antinodes

def handle_day(layout, sample=False):
    data = dm.read_data(8, sample, False)
    answer = ""

    # * Part one and two
    coppied_data = [list(row) for row in data]
    width = len(coppied_data[0])
    height = len(coppied_data)
    dict = {}
    for i, row in enumerate(coppied_data):
        for j, char in enumerate(row):
            if(char != '.'):
                if(char in dict):
                    dict[char].append((i,j))
                else:
                    dict[char] = [(i,j)]

    for key in dict:
        if(len(dict[key]) == 1):
            continue
        for i, pos in enumerate(dict[key]):
            for j in range(i+1, len(dict[key])):
                antinode1, antinode2 = create_antinode(pos, dict[key][j])
                if(antinode1[0] >= 0 and antinode1[0] < height and antinode1[1] >= 0 and antinode1[1] < width):
                    coppied_data[antinode1[0]][antinode1[1]] = '#'
                if(antinode2[0] >= 0 and antinode2[0] < height and antinode2[1] >= 0 and antinode2[1] < width):
                    coppied_data[antinode2[0]][antinode2[1]] = '#'
    # for row in coppied_data:
    #     print(row)

    sum = 0
    for row in coppied_data:
        for char in row:
            if(char == '#'):
                sum += 1

    answer += f"Part one: {sum}\n"

    # * Part two
    for key in dict:
        if(len(dict[key]) == 1):
            continue
        for i, pos in enumerate(dict[key]):
            coppied_data[pos[0]][pos[1]] = '#'
            for j in range(i+1, len(dict[key])):
                antinodes = create_antinodes(pos, dict[key][j], width, height)
                for antinode in antinodes:
                    coppied_data[antinode[0]][antinode[1]] = '#'

    sum = 0
    for row in coppied_data:
        for char in row:
            if(char == '#'):
                sum += 1

    # for row in coppied_data:
    #     print(row)


    answer += f"\nPart two: {sum}"


    dm.write_data(8, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




