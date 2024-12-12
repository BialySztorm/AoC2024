from kivy.uix.label import Label

from utils import data_manager as dm

def flood_fill(field, start_pos):
    stack = [start_pos]
    subfield = []

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while stack:
        pos = stack.pop()
        if pos in field:
            field.remove(pos)
            subfield.append(pos)
            for dx, dy in directions:
                new_pos = (pos[0] + dx, pos[1] + dy)
                stack.append(new_pos)

    return subfield

def calculate_field_and_fences(subfields, discount=False):
    def get_fences(subfield):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        fences = 0
        fences1 = []
        subfield_set = set(subfield)
        for pos in subfield:
            for dx, dy in directions:
                new_pos = (pos[0] + dx, pos[1] + dy)
                if new_pos not in subfield_set:
                    fences += 1
                    if(discount):
                        tmp_pos = (new_pos[0], new_pos[1],dx,dy)
                        fences1.append(tmp_pos)
                        pos_min = (new_pos[0] - dy, new_pos[1] - dx,dx,dy)
                        pos_max = (new_pos[0] + dy, new_pos[1] + dx,dx,dy)
                        if pos_min in fences1:
                            fences -= 1
                        if pos_max in fences1:
                            fences -= 1

        return fences

    results = []
    for subfield in subfields:
        field = len(subfield)
        fences = get_fences(subfield)
        results.append({'field': field, 'fences': fences})
    return results

def handle_day(layout, sample=False):
    data = dm.read_data(12, sample, False)
    answer = ""

    # * Part one and two
    fields = {}
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if(c not in fields):
                fields[c] = []
            fields[c].append((x, y))
    subfields = []
    for field in fields:
        while fields[field]:
            start_pos = fields[field][0]
            subfield = flood_fill(fields[field], start_pos)
            subfields.append(subfield)
    # print(subfields)

    sum = 0
    results = calculate_field_and_fences(subfields)
    for result in results:
        sum += result['field'] * result['fences']

    answer += f"Part one: {sum}\n"

    sum = 0
    results = calculate_field_and_fences(subfields, True)
    for result in results:
        sum += result['field'] * result['fences']

    answer += f"Part two: {sum}"


    dm.write_data(12, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




