from kivy.uix.label import Label

from utils import data_manager as dm


def generate_sequences(n, p2=False):
    if n == 1:
        return [['+'], ['*'], ['||']] if p2 else [['+'], ['*']]

    smaller_sequences = generate_sequences(n - 1, p2)
    new_sequences = []

    for seq in smaller_sequences:
        new_sequences.append(seq + ['+'])
        new_sequences.append(seq + ['*'])
        if p2:
            new_sequences.append(seq + ['||'])

    return new_sequences

def handle_day(layout, sample=False):
    data = dm.read_data(7, sample)
    for row in data:
        row[0] = row[0][:-1]
    answer = ""

    # * Part one
    sum = 0
    for row in data:
        sequences = generate_sequences(len(row)-2)
        for seq in sequences:
            tmp_sum = int(row[1])
            for i, action in enumerate(seq,1):
                if action == '+':
                    tmp_sum += int(row[i+1])
                else:
                    tmp_sum *= int(row[i+1])
            if tmp_sum == int(row[0]):
                sum += int(row[0])
                break

    answer += f"Part one: {sum}\n"

    # * Part two

    sum = 0
    for row in data:
        sequences = generate_sequences(len(row)-2, True)
        for seq in sequences:
            tmp_sum = int(row[1])
            for i, action in enumerate(seq,1):
                if action == '+':
                    tmp_sum += int(row[i+1])
                elif action == '*':
                    tmp_sum *= int(row[i+1])
                else:
                    tmp_sum = int(str(tmp_sum) + row[i+1])
            if tmp_sum == int(row[0]):
                sum += int(row[0])
                break

    answer += f"Part two: {sum}"


    dm.write_data(3, answer, sample)

    # * Visualization
    layout.add_widget(Label(text=answer, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x": 0.45, "y": 0.45}))




