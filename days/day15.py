from kivy.uix.label import Label

from utils import data_manager as dm

def try_move1(map, robot, dx, dy):
    x, y = robot

    if map[y+dy][x+dx] == "#":
        return robot
    elif map[y+dy][x+dx] == ".":
        map[y][x] = "."
        map[y+dy][x+dx] = "@"
        return (x+dx, y+dy)
    while map[y+dy][x+dx] == "O":
        x += dx
        y += dy
    if map[y+dy][x+dx] == "#":
        return robot
    map[y+dy][x+dx] = "O"
    map[robot[1]][robot[0]] = "."
    map[robot[1]+dy][robot[0]+dx] = "@"
    return (robot[0]+dx, robot[1]+dy)

def move_box(map,box, dy):
    x1,y1,x2,y2 = box
    if map[y2+dy][x2] == "#" or map[y1+dy][x1] == "#":
        return False
    if map[y1+dy][x1] == "]":
        tmp_box = (x1-1, y1+dy, x1, y1+dy)
        if(move_box(map, tmp_box, dy) == False):
            return False
    if map[y2+dy][x2] == "[":
        tmp_box = (x2, y2+dy, x2+1, y2+dy)
        if(move_box(map, tmp_box, dy) == False):
            return False
    if map[y1+dy][x1] == "[":
        tmp_box = (x1, y1+dy, x1+1, y1+dy)
        if(move_box(map, tmp_box, dy) == False):
            return False
    map[y1][x1] = "."
    map[y2][x2] = "."
    map[y1+dy][x1] = "["
    map[y2+dy][x2] = "]"
    return True




def try_move2(map, robot, dx, dy):
    x,y = robot
    if map[y+dy][x+dx] == "#":
        return robot
    elif map[y+dy][x+dx] == ".":
        map[y][x] = "."
        map[y+dy][x+dx] = "@"
        return (x+dx, y+dy)
    if dx != 0:
        boxes = 0
        while map[y][x+dx] == "[" or map[y][x+dx] == "]":
            x += 2*dx
            boxes += 1
        x +=dx
        if map[y][x] == "#":
            return robot
        for i in range(boxes):
            if dx < 0:
                map[y][x-i*dx*2] = "["
                map[y][x+1-i*dx*2] = "]"
            else:
                map[y][x-i*dx*2] = "]"
                map[y][x-1-i*dx*2] = "["
        # print(f"Boxes: {boxes}")
        map[robot[1]][robot[0]] = "."
        map[robot[1]][robot[0]+dx] = "@"
        return (robot[0]+dx, robot[1])
    if map[y+dy][x] == "[":
        box = (x, y+dy, x+1, y+dy)
    else:
        box = (x-1, y+dy, x, y+dy)
    map_copy = [row.copy() for row in map]
    if(move_box(map_copy, box, dy) == False):
        return robot
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j] = map_copy[i][j]
    map[robot[1]][robot[0]] = "."
    map[robot[1]+dy][robot[0]] = "@"
    return (robot[0], robot[1]+dy)



def handle_day(layout, sample=False):
    data = dm.read_data(15, sample, False)
    answer = ""
    for i in range(len(data)):
        if data[i] == "":
            map = [list(row) for row in data[:i]]
            movements = list("".join(data[i+1:]))

    p2_map = []
    for row in map:
        tmp_row = []
        for cell in row:
            if cell == "O":
                tmp_row.extend(["[", "]"])
            elif cell == "@":
                tmp_row.extend(["@", "."])
            elif cell == "#":
                tmp_row.extend(["#", "#"])
            else:
                tmp_row.extend([".", "."])
        p2_map.append(tmp_row)

    # * Part one

    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell == "@":
                robot = (j, i)
                break

    for move in movements:
        if move == '^':
            robot = try_move1(map, robot, 0, -1)
        elif move == 'v':
            robot = try_move1(map, robot, 0, 1)
        elif move == '<':
            robot = try_move1(map, robot, -1, 0)
        elif move == '>':
            robot = try_move1(map, robot, 1, 0)
        # print(f"Move: {move}")
        # for row in map:
        #     print(row)

    sum = 0
    for i in range(len(map)):
        for j, cell in enumerate(map[i]):
            if cell == "O":
                sum += 100* i + j

    answer += f"Part one: {sum}"

    # * Part two
    # for row in p2_map:
    #     print(row)

    for i, row in enumerate(p2_map):
        for j, cell in enumerate(row):
            if cell == "@":
                robot = (j, i)
                break

    for move in movements:
        if move == '^':
            robot = try_move2(p2_map, robot, 0, -1)
        elif move == 'v':
            robot = try_move2(p2_map, robot, 0, 1)
        elif move == '<':
            robot = try_move2(p2_map, robot, -1, 0)
        elif move == '>':
            robot = try_move2(p2_map, robot, 1, 0)
        # print(f"Move: {move}")
        # for row in p2_map:
        #     print("\t".join(row))

    sum = 0
    for i in range(len(p2_map)):
        for j, cell in enumerate(p2_map[i]):
            if cell == "[":
                sum += 100* i + j

    answer += f"\nPart two: {sum}"

    dm.write_data(15, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




