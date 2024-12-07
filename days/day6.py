from kivy.uix.label import Label

from utils import data_manager as dm

def is_patrol_inside(size, pos):
    if pos[0] < 0 or pos[0] >= size[0]:
        return False
    if pos[1] < 0 or pos[1] >= size[1]:
        return False
    return True

def simulate_patrol(data, patrol_pos, new_barrier_pos):
    copied_patrol_pos = [patrol_pos[0], patrol_pos[1]]
    copied_data = [row.copy() for row in data]
    copied_data[new_barrier_pos[1]][new_barrier_pos[0]] = '#'

    print("\n")
    visited = {}
    patrol_dx = 0
    patrol_dy = 1
    size = [len(data[0]), len(data)]

    def mark_visited(pos, dir):
        pos = tuple(pos)
        if pos not in visited:
            visited[pos] = set()
        dir = tuple(dir)
        visited[pos].add(dir)

    def is_visited(pos, dir):
        pos = tuple(pos)
        dir = tuple(dir)
        return pos in visited and dir in visited[pos]

    while True:
        if (not is_patrol_inside(size, [copied_patrol_pos[0] + patrol_dx, copied_patrol_pos[1] - patrol_dy])):
            return False
        if patrol_dx == 0:
            if(copied_data[copied_patrol_pos[1]-patrol_dy][copied_patrol_pos[0]] == '#'):
                patrol_dx = patrol_dy
                patrol_dy = 0
            else:
                copied_patrol_pos[1] -= patrol_dy
        elif patrol_dy == 0:
            if(copied_data[copied_patrol_pos[1]][copied_patrol_pos[0]+patrol_dx] == '#'):
                patrol_dy = -patrol_dx
                patrol_dx = 0
            else:
                copied_patrol_pos[0] += patrol_dx
        if is_visited([copied_patrol_pos[0],copied_patrol_pos[1]], (patrol_dx, patrol_dy)):
            return True
        mark_visited([copied_patrol_pos[0],copied_patrol_pos[1]], (patrol_dx, patrol_dy))

    return False



def handle_day(layout, sample=False):
    raw_data = [list(row) for row in dm.read_data(6, sample, False)]
    answer = ""
    data = [row[:] for row in raw_data]

    # * Part one
    patrol_pos = [0,0]
    starting_pos = [0,0]
    x_pos = []
    patrol_dx = 0
    patrol_dy = 1
    pos_visited = 0
    size = [len(data[0]), len(data)]
    for i in range(len(data)):
        position = ''.join(data[i]).find('^')
        if position != -1:
            starting_pos = [position, i]
            patrol_pos = [position, i]
            break
    data[patrol_pos[1]][patrol_pos[0]] = 'X'
    while True:
        if(not is_patrol_inside(size,[patrol_pos[0]+patrol_dx,patrol_pos[1]-patrol_dy])):
            break
        if patrol_dx == 0:
            if(data[patrol_pos[1]-patrol_dy][patrol_pos[0]] == '#'):
                patrol_dx = patrol_dy
                patrol_dy = 0
                continue
            patrol_pos[1] -= patrol_dy
            data[patrol_pos[1]][patrol_pos[0]] = 'X'
        elif patrol_dy == 0:
            if(data[patrol_pos[1]][patrol_pos[0]+patrol_dx] == '#'):
                patrol_dy = -patrol_dx
                patrol_dx = 0
                continue
            patrol_pos[0] += patrol_dx
            data[patrol_pos[1]][patrol_pos[0]] = 'X'

    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if(item == 'X'):
                pos_visited += 1
                if(i != starting_pos[1] or j != starting_pos[0]):
                    x_pos.append([j,i])

    answer += f"Part one: {pos_visited}\n"

    # * Part two
    valid_barriers = 0
    for x in x_pos:
        if(simulate_patrol(raw_data, starting_pos, x)):
            valid_barriers += 1

    answer += f"Part two: {valid_barriers}"


    dm.write_data(6, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




